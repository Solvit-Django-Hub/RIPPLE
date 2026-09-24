from django.urls import path
from .views import RecommendationListCreateAPIView, RecommendationDetailAPIView

urlpatterns = [
    path('', RecommendationListCreateAPIView.as_view(), name='recommendation_list_create'),
    path('<int:recommendation_id>/', RecommendationDetailAPIView.as_view(), name='recommendation_detail'),
]