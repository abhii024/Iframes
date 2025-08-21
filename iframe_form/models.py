from django.db import models
from django.db.models import JSONField

class Organization(models.Model):
    FIELD_TYPES = {
        "text": {"icon": "fas fa-font", "label": "Text"},
        "email": {"icon": "fas fa-envelope", "label": "Email"},
        "number": {"icon": "fas fa-hashtag", "label": "Number"},
        "phone": {"icon": "fas fa-phone", "label": "Phone"},
        "textarea": {"icon": "fas fa-align-left", "label": "Text Area"},
        "select": {"icon": "fas fa-caret-down", "label": "Dropdown"},
        "multiselect": {"icon": "fas fa-bars", "label": "Multi Select"},
        "radio": {"icon": "fas fa-dot-circle", "label": "Radio Buttons"},
        "checkbox": {"icon": "fas fa-check-square", "label": "Checkbox"},
        "multicheckbox": {"icon": "fas fa-tasks", "label": "Multi Checkbox"},
        "date": {"icon": "fas fa-calendar", "label": "Date"},
        "time": {"icon": "fas fa-clock", "label": "Time"},
        "url": {"icon": "fas fa-link", "label": "Website URL"},
        "html": {"icon": "fas fa-code", "label": "HTML Content"},
        "consent": {"icon": "fas fa-check-circle", "label": "Consent"},
    }
    
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