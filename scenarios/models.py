from django.db import models
from django.conf import settings
from projects.models import Project


class Scenario(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='scenarios'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scenarios'
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, default='')
    baseline_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Key-value pairs representing current state (e.g. {'training_sessions': 1})"
    )
    changes = models.JSONField(
        default=dict,
        help_text="Key-value pairs representing simulated changes (e.g. {'training_sessions': 3})"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - Project: {self.project.name}"