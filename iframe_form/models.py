from django.db import models
from django.db.models import JSONField

class Organization(models.Model):
    FIELD_TYPES = (
        ('text', 'Text'),
        ('email', 'Email'),
        ('number', 'Number'),
        ('phone', 'Phone'),
        ('textarea', 'Text Area'),
        ('select', 'Select Dropdown'),
        ('multiselect', 'Multi Select Dropdown'),
        ('radio', 'Radio Buttons'),
        ('checkbox', 'Checkbox'),
        ('multicheckbox', 'Multi Checkbox'),
        ('date', 'Date'),
        ('time', 'Time'),
        ('url', 'Website URL'),
        ('html', 'HTML Content'),
        ('consent', 'Consent Checkbox'),
    )
    
    name = models.CharField(max_length=255)
    form_fields = JSONField(default=list)  # Stores field configurations
    form_style = models.TextField(blank=True)  # Custom CSS
    
    def __str__(self):
        return self.name

class ContactSubmission(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    form_data = JSONField(default=dict)  # Store all submitted data
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.organization.name if self.organization else 'Unknown'} - {self.created_at}"