from django.urls import path
from .views import (
    DecisionListCreateAPIView,
    DecisionDetailAPIView,
    OutcomeListCreateAPIView,
    RecordDecisionAPIView,
    RecordOutcomeAPIView
)

urlpatterns = [
    path('', DecisionListCreateAPIView.as_view(), name='decision_list'),
    path('<int:decision_id>/', DecisionDetailAPIView.as_view(), name='decision_detail'),
    path('<int:decision_id>/record-outcome/', RecordOutcomeAPIView.as_view(), name='record_outcome'),
    path('outcomes/', OutcomeListCreateAPIView.as_view(), name='outcome_list'),
]