from rest_framework import serializers
from .models import Decision, Outcome


class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = ('id', 'decision', 'predicted_value', 'actual_value', 'difference', 'result', 'recorded_at')
        read_only_fields = ('id', 'difference', 'recorded_at')


class DecisionSerializer(serializers.ModelSerializer):
    outcome = OutcomeSerializer(read_only=True)
    decided_by_username = serializers.ReadOnlyField(source='decided_by.username')
    recommendation_title = serializers.ReadOnlyField(source='recommendation.title')

    class Meta:
        model = Decision
        fields = (
            'id',
            'recommendation',
            'recommendation_title',
            'decided_by',
            'decided_by_username',
            'decision',
            'notes',
            'outcome',
            'decided_at'
        )
        read_only_fields = ('id', 'decided_by', 'decided_by_username', 'recommendation_title', 'outcome', 'decided_at')