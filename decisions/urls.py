from django.urls import path
from .views import (
    DecisionListCreateAPIView,
    DecisionDetailAPIView,
    OutcomeListCreateAPIView,
    OutcomeDetailAPIView
)

urlpatterns = [
    path('', DecisionListCreateAPIView.as_view(), name='decision_list_create'),
    path('<int:decision_id>/', DecisionDetailAPIView.as_view(), name='decision_detail'),
    path('outcomes/', OutcomeListCreateAPIView.as_view(), name='outcome_list_create'),
    path('outcomes/<int:outcome_id>/', OutcomeDetailAPIView.as_view(), name='outcome_detail'),
]