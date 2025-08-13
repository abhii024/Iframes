# admin.py
from django.contrib import admin
from .models import Organization

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    fields = ('name', 'form_style', 'fields')
    filter_horizontal = ()
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'fields':
            kwargs['widget'] = admin.widgets.AdminTextareaWidget()  # Textarea to type JSON or list
        return super().formfield_for_dbfield(db_field, **kwargs)

admin.site.register(Organization, OrganizationAdmin)
