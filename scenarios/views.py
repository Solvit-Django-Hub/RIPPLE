from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Scenario
from .serializers import ScenarioSerializer


class ScenarioListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = ScenarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Scenario.objects.all()
        project_id = self.request.query_params.get('project_id')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ScenarioDetailAPIView(generics.RetrieveUpdateDestroyAPIView):


    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'scenario_id'