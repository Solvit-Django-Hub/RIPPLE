from django.db import models
from django.conf import settings
from recommendations.models import Recommendation


class Decision(models.Model):
   

    STATUS_CHOICES = [
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('DEFERRED', 'Deferred'),
        ('IMPLEMENTED', 'Implemented'),
    ]

    recommendation = models.ForeignKey(
        Recommendation,
        on_delete=models.CASCADE,
        related_name='decisions'
    )
    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='decisions'
    )
    decision = models.CharField(max_length=30, choices=STATUS_CHOICES, default='APPROVED')
    notes = models.TextField(blank=True, default='')
    decided_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-decided_at']

    def __str__(self):
        return f"Decision: {self.decision} on '{self.recommendation.title}' by {self.decided_by.username}"


class Outcome(models.Model):
   

    decision = models.OneToOneField(
        Decision,
        on_delete=models.CASCADE,
        related_name='outcome'
    )
    predicted_value = models.FloatField()
    actual_value = models.FloatField()
    difference = models.FloatField(blank=True, null=True, help_text="Actual minus Predicted")
    result = models.TextField(blank=True, default='', help_text="Qualitative observation or evaluation")
    recorded_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-recorded_at']

    def save(self, *args, **kwargs):
        self.difference = round(self.actual_value - self.predicted_value, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Outcome for Decision #{self.decision_id}: Diff = {self.difference}"