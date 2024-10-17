from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project

class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%f%z", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%f%z", read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by', 'updated_at']

class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source='client.client_name', read_only=True)
    users = UserNestedSerializer(many=True, read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%f%z", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%f%z", read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_by', 'updated_at']

class ProjectCreateSerializer(serializers.ModelSerializer):
    users = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    client_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Project
        fields = ['project_name', 'client_id', 'users']

    def create(self, validated_data):
        user_ids = validated_data.pop('users', [])
        client_id = validated_data.pop('client_id')
        client = Client.objects.get(id=client_id)
        project = Project.objects.create(client=client, created_by=self.context['request'].user, **validated_data)
        project.users.set(user_ids)
        return project
    
class ProjectSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_name']

class ClientDetailSerializer(serializers.ModelSerializer):
    projects = ProjectSimpleSerializer(many=True, read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%f%z", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%f%z", read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by', 'updated_at']