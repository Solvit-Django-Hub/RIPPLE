
from django.db import models
from signals.models import Signal


class Trace(models.Model):
    """Represents a contributing factor associated with a detected signal."""

    signal = models.ForeignKey(
        Signal,
        on_delete=models.CASCADE,
        related_name='traces'
    )
    factor = models.CharField(max_length=150)
    importance_score = models.FloatField(
        help_text="Relative factor weight/importance between 0.0 and 1.0 (or percentage 0-100)"
    )
    explanation = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-importance_score']

    def __str__(self):
        return f"{self.factor} ({self.importance_score})"