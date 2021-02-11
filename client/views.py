from django.shortcuts import render
from rest_framework import generics
from .serializers import ClientSerializer, ClientUpdateDeleteSerializer, CreateClientProjectSerialzier
from . models import Client, Project
from rest_framework.views import APIView
from rest_framework.response import Response

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
        print(user_data)
        serializer = CreateClientProjectSerialzier(data=user_data)
        if serializer.is_valid():
            serializer.create()
            print("data > ", serializer.data)
        return Response("Yo")
