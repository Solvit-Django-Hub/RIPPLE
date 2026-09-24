from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Dataset
from .serializers import DatasetSerializer


class DatasetListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filterset_fields = ['project']
    search_fields = ['name']
    ordering_fields = ['created_at', 'rows']

    def get_queryset(self):
        return Dataset.objects.all()

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class DatasetDetailAPIView(generics.RetrieveDestroyAPIView):


    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'dataset_id'