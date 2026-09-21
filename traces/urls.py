
from django.urls import path
from .views import TraceListCreateAPIView, TraceDetailAPIView

urlpatterns = [
    path('', TraceListCreateAPIView.as_view(), name='trace_list_create'),
    path('<int:trace_id>/', TraceDetailAPIView.as_view(), name='trace_detail'),
]