# iframe_form/models.py
from django.db import models
from django.contrib.postgres.fields import ArrayField  # If using PostgreSQL
import json
from django.contrib.postgres.fields import JSONField  # For Django < 3.1
from django.db.models import JSONField  
class Organization(models.Model):
    name = models.CharField(max_length=255)
    fields = models.JSONField(default=list)  # Stores all selected fields
    required_fields = models.JSONField(default=list)  # Stores only required fields
    form_style = models.TextField(blank=True)  # Custom CSS
    
    def __str__(self):
        return self.name

class ContactSubmission(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    additional_data = models.JSONField(null=True, blank=True)  # Make this field optional
    
    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at})"