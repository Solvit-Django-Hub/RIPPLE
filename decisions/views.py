from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from recommendations.models import Recommendation
from .models import Decision, Outcome
from .serializers import DecisionSerializer, OutcomeSerializer


class RecordDecisionAPIView(APIView):


    permission_classes = [IsAuthenticated]

    def post(self, request, recommendation_id):
        recommendation = get_object_or_404(Recommendation, id=recommendation_id)
        action = request.data.get('decision', 'approved')
        notes = request.data.get('notes', '')

        decision = Decision.objects.create(
            recommendation=recommendation,
            decided_by=request.user,
            decision=action,
            notes=notes
        )

        return Response(
            {
                "message": f"Decision '{action.upper()}' recorded successfully.",
                "decision_id": decision.id,
                "recommendation": recommendation.title,
                "decided_by": request.user.username,
                "decision": decision.decision,
                "notes": decision.notes,
                "decided_at": decision.decided_at
            },
            status=status.HTTP_201_CREATED
        )


class RecordOutcomeAPIView(APIView):
    

    permission_classes = [IsAuthenticated]

    def post(self, request, decision_id):
        decision = get_object_or_404(Decision, id=decision_id)
        actual_value = request.data.get('actual_value')
        notes = request.data.get('result', '')

        if actual_value is None:
            return Response(
                {"error": "actual_value is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            actual_value = float(actual_value)
        except ValueError:
            return Response({"error": "actual_value must be a number."}, status=status.HTTP_400_BAD_REQUEST)

        # Get predicted value from the scenario's prediction
        prediction = decision.recommendation.scenario.predictions.first()
        predicted_value = prediction.predicted_value if prediction else 0.0

        outcome, created = Outcome.objects.update_or_create(
            decision=decision,
            defaults={
                "predicted_value": predicted_value,
                "actual_value": actual_value,
                "result": notes,
            }
        )

        return Response(
            {
                "message": "Outcome recorded and feedback loop updated.",
                "decision_id": decision.id,
                "action_taken": decision.recommendation.title,
                "predicted_value": outcome.predicted_value,
                "actual_value": outcome.actual_value,
                "difference": outcome.difference,
                "evaluation": outcome.result,
                "recorded_at": outcome.recorded_at
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class DecisionListCreateAPIView(generics.ListCreateAPIView):


    serializer_class = DecisionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Decision.objects.all()

    def perform_create(self, serializer):
        serializer.save(decided_by=self.request.user)


class DecisionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):


    queryset = Decision.objects.all()
    serializer_class = DecisionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'decision_id'


class OutcomeListCreateAPIView(generics.ListCreateAPIView):


    serializer_class = OutcomeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Outcome.objects.all()