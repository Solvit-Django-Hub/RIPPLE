from rest_framework import serializers
from .models import Prediction


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = (
            'id',
            'scenario',
            'model_name',
            'predicted_value',
            'probability',
            'confidence',
            'notes',
            'created_at'
        )
        read_only_fields = ('id', 'created_at')