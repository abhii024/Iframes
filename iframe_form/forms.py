from django import forms
from .models import ContactSubmission, Organization
from hcaptcha.fields import hCaptchaField
import json

class DynamicContactForm(forms.Form):
    organization_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    
    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        
        if self.organization and self.organization.form_fields:
            for field_config in self.organization.form_fields:
                self.add_field_from_config(field_config)
    
    def add_field_from_config(self, config):
        field_type = config.get('type', 'text')
        field_name = config.get('name', '')
        label = config.get('label', field_name.title())
        required = config.get('required', False)
        placeholder = config.get('placeholder', '')
        css_class = config.get('css_class', 'form-control')
        max_length = config.get('max_length', None)
        options = config.get('options', [])
        help_text = config.get('help_text', '')
        
        # Common attributes for all fields
        attrs = {
            'class': css_class,
            'placeholder': placeholder
        }
        
        # Field-specific configurations
        if field_type == 'text':
            self.fields[field_name] = forms.CharField(
                label=label,
                required=required,
                max_length=max_length,
                widget=forms.TextInput(attrs=attrs),
                help_text=help_text
            )
        elif field_type == 'email':
            self.fields[field_name] = forms.EmailField(
                label=label,
                required=required,
                widget=forms.EmailInput(attrs=attrs),
                help_text=help_text
            )
        elif field_type == 'number':
            self.fields[field_name] = forms.IntegerField(
                label=label,
                required=required,
                widget=forms.NumberInput(attrs=attrs),
                help_text=help_text
            )
        elif field_type == 'phone':
            self.fields[field_name] = forms.CharField(
                label=label,
                required=required,
                widget=forms.TextInput(attrs=attrs),
                help_text=help_text
            )
        elif field_type == 'textarea':
            self.fields[field_name] = forms.CharField(
                label=label,
                required=required,
                widget=forms.Textarea(attrs={**attrs, 'rows': config.get('rows', 4)}),
                help_text=help_text
            )
        elif field_type == 'select':
            choices = [(opt, opt) for opt in options]
            self.fields[field_name] = forms.ChoiceField(
                label=label,
                required=required,
                choices=choices,
                widget=forms.Select(attrs=attrs),
                help_text=help_text
            )
        elif field_type == 'multiselect':
            choices = [(opt, opt) for opt in options]
            self.fields[field_name] = forms.MultipleChoiceField(
                label=label,
                required=required,
                choices=choices,
                widget=forms.SelectMultiple(attrs=attrs),
                help_text=help_text
            )
        elif field_type == 'radio':
            choices = [(opt, opt) for opt in options]
            self.fields[field_name] = forms.ChoiceField(
                label=label,
                required=required,
                choices=choices,
                widget=forms.RadioSelect(attrs={'class': 'form-radio'}),
                help_text=help_text
            )
        elif field_type == 'checkbox':
            self.fields[field_name] = forms.BooleanField(
                label=label,
                required=required,
                widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
                help_text=help_text
            )
        elif field_type == 'multicheckbox':
            choices = [(opt, opt) for opt in options]
            self.fields[field_name] = forms.MultipleChoiceField(
                label=label,
                required=required,
                choices=choices,
                widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-multicheckbox'}),
                help_text=help_text
            )
        elif field_type == 'date':
            self.fields[field_name] = forms.DateField(
                label=label,
                required=required,
                widget=forms.DateInput(attrs={**attrs, 'type': 'date'}),
                help_text=help_text
            )
        elif field_type == 'time':
            self.fields[field_name] = forms.TimeField(
                label=label,
                required=required,
                widget=forms.TimeInput(attrs={**attrs, 'type': 'time'}),
                help_text=help_text
            )
        elif field_type == 'url':
            self.fields[field_name] = forms.URLField(
                label=label,
                required=required,
                widget=forms.URLInput(attrs=attrs),
                help_text=help_text
            )
        elif field_type == 'html':
            # HTML content field (not a form input)
            self.fields[field_name] = forms.CharField(
                label='',
                required=False,
                widget=forms.HiddenInput()
            )
        elif field_type == 'consent':
            self.fields[field_name] = forms.BooleanField(
                label=label,
                required=required,
                widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
                help_text=help_text
            )
    
    def save(self, commit=True):
        form_data = {}
        for field_name in self.fields:
            if field_name != 'organization_id':
                form_data[field_name] = self.cleaned_data.get(field_name)
        
        submission = ContactSubmission(
            organization_id=self.cleaned_data.get('organization_id'),
            form_data=form_data
        )
        
        if commit:
            submission.save()
        
        return submission