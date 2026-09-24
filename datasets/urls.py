from django.urls import path
from .views import (
    DatasetListCreateAPIView,
    DatasetDetailAPIView,
    DatasetAnalyzeAPIView,
    DatasetAutoDetectSignalsAPIView,
)

urlpatterns = [
    path('', DatasetListCreateAPIView.as_view(), name='dataset_list_create'),
    path('<int:dataset_id>/', DatasetDetailAPIView.as_view(), name='dataset_detail'),
    path('<int:dataset_id>/analyze/', DatasetAnalyzeAPIView.as_view(), name='dataset_analyze'),
    path('<int:dataset_id>/detect-signals/', DatasetAutoDetectSignalsAPIView.as_view(), name='dataset_detect_signals'),
]