from django.shortcuts import render
from rest_framework import generics
from .serializers import ClientSerializer, ClientUpdateDeleteSerializer, CreateClientProjectSerialzier
from . models import Client, Project, ClientProjects
from rest_framework.views import APIView
from rest_framework.response import Response
from json import loads, dumps
from rest_framework import status

# Create your views here.

class ListCreateClient(generics.ListCreateAPIView):
    '''
        Returns List of clients on Get request
        Creates a client on Post request.
    '''

    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def pre_save(self, obj):
        obj.created_by = self.request.user

    def get_switcher_class(self):
        switcher = {
            'GET' : ClientSerializer,
            'POST' : ClientSerializer,
        }
        return switcher.get(self.request.method)

class GetUpdateDeleteClientInfo(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientUpdateDeleteSerializer
    queryset = Client.objects.all()

class CreateClientProject(APIView):

    def get(self, request,id, format=None):
        return Response("Method Not Allowed.", status=401)


    def post(self, request,id, format=None):
        '''
            Creates a project for user
        '''
        user_data = request.data.copy()
        user_data['client_id'] = id

        if not Client.objects.filter(id=id).exists():
            content = {'Client doesnot exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        # Check if this client already have a project with this name
        if ClientProjects.objects.filter(client_id=id, project__project_name=request.data.get('project_name')).exists():
            content = {'Project with this name already exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        if not request.data.get('users'):
            content = {'Users not supplied'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        p = Project.objects.create(project_name=request.data.get('project_name'), created_by_id=2)
        c = ClientProjects.objects.create(client_id=id, project_id=p.id )
        for user in request.data.get('users'):
            p.users.add(user['id'])
        data = {}
        data['id'] = p.id
        data['project_name'] = p.project_name
        data['client'] = c.client.client_name
        data['users'] = request.data.get('users')
        data['created_at'] = p.created_at
        data['created_by'] = p.created_by.first_name
        return Response(data)