from rest_framework import serializers
from predictions.serializers import PredictionSerializer
from .models import Scenario


class ScenarioSerializer(serializers.ModelSerializer):
    predictions = PredictionSerializer(many=True, read_only=True)
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    project_name = serializers.ReadOnlyField(source='project.name')

    class Meta:
        model = Scenario
        fields = (
            'id',
            'project',
            'project_name',
            'created_by',
            'created_by_username',
            'name',
            'description',
            'baseline_data',
            'changes',
            'predictions',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'created_by', 'created_by_username', 'project_name', 'predictions', 'created_at', 'updated_at')