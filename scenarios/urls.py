from django.urls import path
from .views import ScenarioListCreateAPIView, ScenarioDetailAPIView, ScenarioCompareAPIView

urlpatterns = [
    path('', ScenarioListCreateAPIView.as_view(), name='scenario_list_create'),
    path('compare/', ScenarioCompareAPIView.as_view(), name='scenario_compare'),
    path('<int:scenario_id>/', ScenarioDetailAPIView.as_view(), name='scenario_detail'),
]