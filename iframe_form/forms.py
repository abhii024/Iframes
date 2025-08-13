# iframe_form/forms.py
from django import forms
from .models import ContactSubmission

class ContactForm(forms.ModelForm):
    organization_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = ContactSubmission
        fields = []  # initially empty, set dynamically
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        selected_fields = kwargs.pop('selected_fields', [])
        super().__init__(*args, **kwargs)
        # Keep only selected fields
        for field_name in list(self.fields.keys()):
            if field_name not in selected_fields and field_name != 'organization_id':
                self.fields.pop(field_name)

    organization_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email',
                'required': 'required'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject',
                'required': 'required'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message',
                'rows': 5,
                'required': 'required'
            }),
        }