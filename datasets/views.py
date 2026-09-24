from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from .models import Dataset
from .serializers import DatasetSerializer
from .services import analyze_dataset_file, auto_detect_signals_from_dataset


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


class DatasetAnalyzeAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id)
        if not dataset.file:
            return Response({"error": "No file attached to this dataset."}, status=status.HTTP_400_BAD_REQUEST)

        stats = analyze_dataset_file(dataset)
        return Response({
            "message": "Dataset analyzed successfully.",
            "dataset_id": dataset.id,
            "name": dataset.name,
            "statistics": stats
        }, status=status.HTTP_200_OK)


class DatasetAutoDetectSignalsAPIView(APIView):


    permission_classes = [IsAuthenticated]

    def post(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id)
        if not dataset.file:
            return Response({"error": "No file attached to this dataset."}, status=status.HTTP_400_BAD_REQUEST)

        signals_found = auto_detect_signals_from_dataset(dataset)
        return Response({
            "message": f"Scan completed. Discovered {len(signals_found)} significant signals.",
            "dataset_id": dataset.id,
            "signals": signals_found
        }, status=status.HTTP_201_CREATED if signals_found else status.HTTP_200_OK)