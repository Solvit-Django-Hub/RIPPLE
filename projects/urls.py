from django.urls import path
from .views import ProjectListCreateAPIView, ProjectDetailAPIView

urlpatterns = [
    path('', ProjectListCreateAPIView.as_view(), name='project_list_create'),
    path('<int:project_id>/', ProjectDetailAPIView.as_view(), name='project_detail'),
]