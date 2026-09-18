
from django.urls import path
from .views import SignalListCreateAPIView, SignalDetailAPIView

urlpatterns = [
    path('', SignalListCreateAPIView.as_view(), name='signal_list_create'),
    path('<int:signal_id>/', SignalDetailAPIView.as_view(), name='signal_detail'),
]