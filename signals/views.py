
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Signal
from .serializers import SignalSerializer


class SignalListCreateAPIView(generics.ListCreateAPIView):
  

    serializer_class = SignalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Signal.objects.all()
        project_id = self.request.query_params.get('project_id')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        severity = self.request.query_params.get('severity')
        if severity:
            queryset = queryset.filter(severity=severity)
        return queryset


class SignalDetailAPIView(generics.RetrieveUpdateDestroyAPIView):


    queryset = Signal.objects.all()
    serializer_class = SignalSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'signal_id'