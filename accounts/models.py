
import random
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):


    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('analyst', 'Analyst'),
        ('decision_maker', 'Decision Maker'),
        ('viewer', 'Viewer'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='viewer'
    )
    is_email_verified = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class VerificationCode(models.Model):


    PURPOSE_CHOICES = [
        ('email_verification', 'Email Verification'),
        ('password_reset', 'Password Reset'),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='verification_codes'
    )
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=25, choices=PURPOSE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def create_code(cls, user, purpose):

        # Invalidate previous unused codes for same user and purpose
        cls.objects.filter(user=user, purpose=purpose, is_used=False).update(is_used=True)

        code = f"{random.randint(100000, 999999)}"
        expires_at = timezone.now() + timedelta(minutes=15)
        return cls.objects.create(
            user=user,
            code=code,
            purpose=purpose,
            expires_at=expires_at
        )

    def is_valid(self):
        return not self.is_used and timezone.now() <= self.expires_at

    def __str__(self):
        return f"{self.purpose} code for {self.user.email}: {self.code}"