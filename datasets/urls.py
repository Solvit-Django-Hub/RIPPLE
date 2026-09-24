from django.urls import path
from .views import DatasetListCreateAPIView, DatasetDetailAPIView

urlpatterns = [
    path('', DatasetListCreateAPIView.as_view(), name='dataset_list_create'),
    path('<int:dataset_id>/', DatasetDetailAPIView.as_view(), name='dataset_detail'),
]