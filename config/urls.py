from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),


    path('api/auth/', include('accounts.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/datasets/', include('datasets.urls')),
    path('api/signals/', include('signals.urls')),
    path('api/traces/', include('traces.urls')),
    path('api/scenarios/', include('scenarios.urls')),
    path('api/predictions/', include('predictions.urls')),
    path('api/recommendations/', include('recommendations.urls')),
    path('api/decisions/', include('decisions.urls')),
    path('api/dashboard/', include('dashboard.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)