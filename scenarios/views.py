from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Scenario
from .serializers import ScenarioSerializer
from predictions.models import Prediction
from recommendations.models import Recommendation


class ScenarioListCreateAPIView(generics.ListCreateAPIView):
    

    serializer_class = ScenarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Scenario.objects.all()
        project_id = self.request.query_params.get('project_id')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        scenario = serializer.save(created_by=request.user)

        # 1. Read baseline and simulated changes
        baseline = scenario.baseline_data or {}
        changes = scenario.changes or {}

        # 2. Simulation engine calculation (Domain: Performance Decision-Support)
        # Baseline score defaults to 60.0 if not specified
        base_score = float(baseline.get('expected_score', baseline.get('score', 62.0)))

        # Simulate positive/negative delta based on input variable shifts
        delta = 0.0
        for key, new_val in changes.items():
            old_val = baseline.get(key, 0)
            try:
                numeric_change = float(new_val) - float(old_val)
                # Example: each added tutoring/training session or study hour adds ~3.2%
                delta += numeric_change * 3.2
            except (ValueError, TypeError):
                delta += 2.5

        delta = round(delta, 2)
        predicted_value = round(min(100.0, max(0.0, base_score + delta)), 2)
        confidence = 0.84

        # 3. Automatically record the Prediction
        prediction = Prediction.objects.create(
            scenario=scenario,
            model_name="RIPPLE Simulation Engine v1",
            predicted_value=predicted_value,
            confidence=confidence,
            notes=f"Simulated change impact: {'+' if delta >= 0 else ''}{delta}% from baseline."
        )

        # 4. Automatically generate a Recommendation option for the decision maker
        risk = "low" if abs(delta) < 10 else ("medium" if delta > 0 else "high")
        rec = Recommendation.objects.create(
            scenario=scenario,
            title=f"Implement: {scenario.name}",
            explanation=f"Based on simulated variables, this action is forecasted to shift performance by {'+' if delta >= 0 else ''}{delta}%.",
            expected_impact=delta,
            risk_level=risk,
            score=round(max(0.0, (delta * 0.7) + (confidence * 10)), 2)
        )

        return Response(
            {
                "scenario_id": scenario.id,
                "name": scenario.name,
                "project": scenario.project_id,
                "baseline_score": base_score,
                "predicted_value": prediction.predicted_value,
                "expected_change": delta,
                "confidence": prediction.confidence,
                "recommendation_id": rec.id,
                "risk_level": rec.risk_level,
                "created_at": scenario.created_at
            },
            status=status.HTTP_201_CREATED
        )


class ScenarioDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a scenario."""

    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'scenario_id'


class ScenarioCompareAPIView(APIView):
    """Compares multiple scenarios side-by-side for the decision maker."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        ids_param = request.query_params.get('ids', '')
        if not ids_param:
            return Response(
                {"error": "Please provide comma-separated scenario IDs, e.g. ?ids=1,2,3"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            scenario_ids = [int(i.strip()) for i in ids_param.split(',') if i.strip()]
        except ValueError:
            return Response({"error": "Invalid IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

        scenarios = Scenario.objects.filter(id__in=scenario_ids).prefetch_related('predictions', 'recommendations')
        comparison = []
        for s in scenarios:
            pred = s.predictions.first()
            rec = s.recommendations.first()
            comparison.append({
                "scenario_id": s.id,
                "name": s.name,
                "changes": s.changes,
                "predicted_value": pred.predicted_value if pred else None,
                "confidence": pred.confidence if pred else None,
                "expected_impact": rec.expected_impact if rec else None,
                "risk_level": rec.risk_level if rec else None,
                "recommendation_score": rec.score if rec else None,
            })

        # Rank options from best to worst score
        comparison.sort(key=lambda x: (x['recommendation_score'] or 0), reverse=True)
        return Response({"ranked_scenarios": comparison})