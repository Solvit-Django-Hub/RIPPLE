from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/signals/', include('signals.urls')),
    path('api/traces/', include('traces.urls')),
    path('api/scenarios/', include('scenarios.urls')),
    path('api/predictions/', include('predictions.urls')),
]