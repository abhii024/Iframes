from django import forms
from .models import ContactSubmission
from hcaptcha.fields import hCaptchaField

class ContactForm(forms.ModelForm):
    organization_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message','phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}),
        }

    def __init__(self, *args, **kwargs):
        selected_fields = kwargs.pop('selected_fields', [])
        required_fields = kwargs.pop('required_fields', [])
        super().__init__(*args, **kwargs)
        
        # Keep only selected fields (except organization_id and captcha)
        for field_name in list(self.fields.keys()):
            if field_name not in selected_fields and field_name not in ['organization_id', 'captcha']:
                self.fields.pop(field_name)
        
        # Set required status based on organization settings
        for field_name, field in self.fields.items():
            if field_name in required_fields:
                field.required = True
                if hasattr(field.widget, 'attrs'):
                    field.widget.attrs['required'] = 'required'
            elif field_name != 'captcha':  # captcha is always required
                field.required = False
                if hasattr(field.widget, 'attrs') and 'required' in field.widget.attrs:
                    del field.widget.attrs['required']

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Ensure organization_id is set
        instance.organization_id = self.cleaned_data.get('organization_id')
        if commit:
            instance.save()
        return instance