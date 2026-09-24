from rest_framework import serializers
from .models import Dataset


class DatasetSerializer(serializers.ModelSerializer):
    uploaded_by_username = serializers.ReadOnlyField(source='uploaded_by.username')
    project_name = serializers.ReadOnlyField(source='project.name')

    class Meta:
        model = Dataset
        fields = (
            'id',
            'project',
            'project_name',
            'name',
            'file',
            'rows',
            'columns',
            'uploaded_by',
            'uploaded_by_username',
            'created_at'
        )
        read_only_fields = ('id', 'rows', 'columns', 'uploaded_by', 'uploaded_by_username', 'project_name', 'created_at')