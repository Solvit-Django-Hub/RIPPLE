from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Recommendation
from .serializers import RecommendationSerializer


class RecommendationListCreateAPIView(generics.ListCreateAPIView):


    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Recommendation.objects.all()
        scenario_id = self.request.query_params.get('scenario_id')
        if scenario_id:
            queryset = queryset.filter(scenario_id=scenario_id)
        return queryset


class RecommendationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'recommendation_id'