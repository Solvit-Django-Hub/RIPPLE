from rest_framework import serializers
from decisions.serializers import DecisionSerializer
from .models import Recommendation


class RecommendationSerializer(serializers.ModelSerializer):
    decisions = DecisionSerializer(many=True, read_only=True)
    scenario_name = serializers.ReadOnlyField(source='scenario.name')

    class Meta:
        model = Recommendation
        fields = (
            'id',
            'scenario',
            'scenario_name',
            'title',
            'explanation',
            'expected_impact',
            'risk_level',
            'score',
            'decisions',
            'created_at'
        )
        read_only_fields = ('id', 'scenario_name', 'decisions', 'created_at')