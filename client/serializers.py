from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
from django.db import transaction


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

class ProjectListSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    class Meta:
        fields = ['id','project_name','created_at','created_by']
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
 
    @transaction.atomic
    def create(self):

        if not models.Client.objects.filter(id=self.initial_data.get('client_id')).exists():
            raise serializers.ValidationError("Client doesnot exist")
        # Check if this client already have a project with this name
        if models.ClientProjects.objects.filter(client_id=self.initial_data.get('client_id'), project__project_name=self.initial_data.get('project_name')).exists():
            raise serializers.ValidationError("Project with this name already exist")

        if not self.initial_data.get('users'):
            raise serializers.ValidationError("Users not supplied")
        
        p = models.Project.objects.create(project_name=self.initial_data.get('project_name'), created_by_id=2)
        c = models.ClientProjects.objects.create(client_id=self.initial_data.get('client_id'), project_id=p.id )
        for user in self.initial_data.get('users'):
            p.users.add(user['id'])
        data = {}
        data['id'] = p.id
        data['project_name'] = p.project_name
        data['client'] = c.client.client_name
        data['users'] = self.initial_data.get('users')
        data['created_at'] = p.created_at
        data['created_by'] = p.created_by.first_name
        return data