
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Trace
from .serializers import TraceSerializer


class TraceListCreateAPIView(generics.ListCreateAPIView):
  

    serializer_class = TraceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Trace.objects.all()
        signal_id = self.request.query_params.get('signal_id')
        if signal_id:
            queryset = queryset.filter(signal_id=signal_id)
        return queryset


class TraceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
   

    queryset = Trace.objects.all()
    serializer_class = TraceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'trace_id'