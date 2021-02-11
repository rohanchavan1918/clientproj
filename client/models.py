from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    client_name = models.CharField(max_length=254)
    projects = models.ManyToManyField('Project', through='ClientProjects', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client_creator")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.client_name

class Project(models.Model):
    users = models.ManyToManyField(User, null=True, blank=True)
    project_name = models.CharField(max_length=254)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_creator")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.project_name

class ClientProjects(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


def get_first_name(self):
    ''' Override default __str__ of User model to return first_name by default '''
    return self.first_name

User.add_to_class("__str__", get_first_name)