from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Decision, Outcome
from .serializers import DecisionSerializer, OutcomeSerializer


class DecisionListCreateAPIView(generics.ListCreateAPIView):


    serializer_class = DecisionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Decision.objects.all()
        recommendation_id = self.request.query_params.get('recommendation_id')
        if recommendation_id:
            queryset = queryset.filter(recommendation_id=recommendation_id)
        return queryset

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


class OutcomeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):


    queryset = Outcome.objects.all()
    serializer_class = OutcomeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'outcome_id'