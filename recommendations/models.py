from django.db import models
from scenarios.models import Scenario


class Recommendation(models.Model):

    RISK_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    scenario = models.ForeignKey(
        Scenario,
        on_delete=models.CASCADE,
        related_name='recommendations'
    )
    title = models.CharField(max_length=200)
    explanation = models.TextField()
    expected_impact = models.FloatField(help_text="Expected numerical delta/improvement, e.g. +9.0")
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, default='low')
    score = models.FloatField(default=0.0, help_text="Priority ranking score (higher is better)")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-score', '-expected_impact']

    def __str__(self):
        return f"{self.title} (Score: {self.score})"