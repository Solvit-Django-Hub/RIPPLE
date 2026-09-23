from django.db import models
from scenarios.models import Scenario


class Prediction(models.Model):


    scenario = models.ForeignKey(
        Scenario,
        on_delete=models.CASCADE,
        related_name='predictions'
    )
    model_name = models.CharField(
        max_length=100,
        default='Baseline Regressor',
        help_text="Name or version of model/algorithm producing this prediction"
    )
    predicted_value = models.FloatField(
        help_text="The numerical or regression outcome predicted"
    )
    probability = models.FloatField(
        blank=True,
        null=True,
        help_text="Classification probability if applicable (0.0 to 1.0)"
    )
    confidence = models.FloatField(
        default=0.80,
        help_text="Confidence rating (e.g. 0.85 = 85% confidence)"
    )
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Prediction for '{self.scenario.name}': {self.predicted_value} (conf: {self.confidence})"