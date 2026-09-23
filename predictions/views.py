from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Prediction
from .serializers import PredictionSerializer


class PredictionListCreateAPIView(generics.ListCreateAPIView):


    serializer_class = PredictionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Prediction.objects.all()
        scenario_id = self.request.query_params.get('scenario_id')
        if scenario_id:
            queryset = queryset.filter(scenario_id=scenario_id)
        return queryset


class PredictionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):


    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'prediction_id'