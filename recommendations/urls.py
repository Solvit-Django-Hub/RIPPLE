from django.urls import path
from .views import RecommendationListCreateAPIView, RecommendationDetailAPIView
from decisions.views import RecordDecisionAPIView

urlpatterns = [
    path('', RecommendationListCreateAPIView.as_view(), name='recommendation_list_create'),
    path('<int:recommendation_id>/', RecommendationDetailAPIView.as_view(), name='recommendation_detail'),
    path('<int:recommendation_id>/decide/', RecordDecisionAPIView.as_view(), name='recommendation_decide'),
]