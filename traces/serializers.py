
from rest_framework import serializers
from .models import Trace


class TraceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trace
        fields = ('id', 'signal', 'factor', 'importance_score', 'explanation', 'created_at')
        read_only_fields = ('id', 'created_at')