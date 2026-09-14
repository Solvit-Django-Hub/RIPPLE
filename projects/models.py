"""Project models for RIPPLE platform."""
from django.db import models
from django.conf import settings


class Project(models.Model):
    

    DOMAIN_CHOICES = [
        ('education', 'Education'),
        ('healthcare', 'Healthcare'),
        ('agriculture', 'Agriculture'),
        ('business', 'Business'),
        ('finance', 'Finance'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, default='')
    domain = models.CharField(max_length=50, choices=DOMAIN_CHOICES, default='education')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name}"