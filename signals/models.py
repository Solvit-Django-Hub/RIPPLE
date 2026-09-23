
from django.db import models
from projects.models import Project


class Signal(models.Model):
   

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('resolved', 'Resolved'),
        ('ignored', 'Ignored'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='signals'
    )
    metric = models.CharField(max_length=120)
    previous_value = models.FloatField()
    current_value = models.FloatField()
    change_percentage = models.FloatField(blank=True, null=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='low')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.previous_value != 0:
            diff = self.current_value - self.previous_value
            self.change_percentage = round((diff / abs(self.previous_value)) * 100, 2)
        else:
            self.change_percentage = 0.0

        # Auto-compute severity if default 'low'
        if self.severity == 'low' and self.change_percentage is not None:
            abs_change = abs(self.change_percentage)
            if abs_change >= 25:
                self.severity = 'critical'
            elif abs_change >= 15:
                self.severity = 'high'
            elif abs_change >= 8:
                self.severity = 'medium'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.metric}: {self.previous_value} -> {self.current_value} ({self.severity.upper()})"