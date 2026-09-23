from django.urls import path
from .views import ScenarioListCreateAPIView, ScenarioDetailAPIView

urlpatterns = [
    path('', ScenarioListCreateAPIView.as_view(), name='scenario_list_create'),
    path('<int:scenario_id>/', ScenarioDetailAPIView.as_view(), name='scenario_detail'),
]