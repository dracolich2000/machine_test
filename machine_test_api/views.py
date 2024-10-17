from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Client, Project
from .serializers import (
    ClientSerializer,
    ClientDetailSerializer,
    ProjectSerializer,
    ProjectCreateSerializer
)
from django.shortcuts import get_object_or_404
from rest_framework import generics


# Create your views here.
class ClientViewSet(viewsets.ModelViewSet):
    """
    Handles:
    - GET /clients/
    - POST /clients/
    - GET /clients/:id
    - PUT/PATCH /clients/:id
    - DELETE /clients/:id
    """
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ClientDetailSerializer
        return ClientSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ProjectViewSet(viewsets.ModelViewSet):
    """
    Handles:
    - GET /projects/
    - POST /projects/
    - GET /projects/:id
    - PUT/PATCH /projects/:id
    - DELETE /projects/:id
    """
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return ProjectCreateSerializer
        return ProjectSerializer

    def get_queryset(self):
        """
        For listing all projects assigned to the logged-in user when accessing /projects/
        """
        user = self.request.user
        return Project.objects.filter(users=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)



class ClientProjectCreateView(generics.CreateAPIView):
    """
    Handles:
    - POST /clients/:id/projects/
    """
    serializer_class = ProjectCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, client_id):
        data = request.data.copy()
        data['client_id'] = client_id
        serializer = self.get_serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        output_serializer = ProjectSerializer(project, context={'request': request})
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
