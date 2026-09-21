
from rest_framework import serializers
from traces.serializers import TraceSerializer
from .models import Signal


class SignalSerializer(serializers.ModelSerializer):
    traces = TraceSerializer(many=True, read_only=True)
    project_name = serializers.ReadOnlyField(source='project.name')

    class Meta:
        model = Signal
        fields = (
            'id',
            'project',
            'project_name',
            'metric',
            'previous_value',
            'current_value',
            'change_percentage',
            'severity',
            'status',
            'traces',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'change_percentage', 'created_at', 'updated_at', 'traces')