from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'owner', 'created_at')
    list_filter = ('domain', 'created_at')
    search_fields = ('name', 'description', 'owner__username')