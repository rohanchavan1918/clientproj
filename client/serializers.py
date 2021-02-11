from rest_framework import serializers
from . import models
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'first_name')
        model = User


class ClientSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()

    class Meta:
        fields = ['id', 'client_name', 'created_at',
                  'updated_at', 'created_by']
        model = models.Client


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'project_name']
        model = models.Project


class ClientUpdateDeleteSerializer(serializers.ModelSerializer):
    '''
        Serializer which can be used to retreive/update/delete clients,
        Project is nested in the response here
    '''
    created_by = UserSerializer()
    projects = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'client_name', 'created_at',
                  'updated_at', 'created_by', 'projects']
        model = models.Client

    def get_projects(self, obj):
        queryset = models.ClientProjects.objects.filter(client=obj)
        return [ProjectSerializer(q.project).data for q in queryset]


class CreateClientProjectSerialzier(serializers.Serializer):

    def create(self):

        if not models.Client.objects.filter(id=self.initial_data.get('client_id')).exists():
            raise serializers.ValidationError("Client doesnot exist")
        # Check if this client already have a project with this name
        if models.ClientProjects.objects.filter(client_id=self.initial_data.get('client_id'), project__project_name=self.initial_data.get('project_name')).exists():
            raise serializers.ValidationError("Client doesnot exist")

        if not self.initial_data.get('users'):
            raise serializers.ValidationError("Users not supplied")
        
        p = models.Project.objects.get_or_create(project_name=self.initial_data.get('project_name'), created_by_id=2)
        c = models.ClientProjects.objects.get_or_create(client_id=self.initial_data.get('client_id'), project=p )
        for user in self.initial_data.get('users'):
            p.users.add(user.id)

        return p