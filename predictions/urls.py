
from django.urls import path
from .views import PredictionListCreateAPIView, PredictionDetailAPIView

urlpatterns = [
    path('', PredictionListCreateAPIView.as_view(), name='prediction_list_create'),
    path('<int:prediction_id>/', PredictionDetailAPIView.as_view(), name='prediction_detail'),
]