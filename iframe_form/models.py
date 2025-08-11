# iframe_form/models.py
from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=100)
    form_style = models.TextField(default='')  # CSS styles for the form
    
    def __str__(self):
        return self.name

class ContactSubmission(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at})"