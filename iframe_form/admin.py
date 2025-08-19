# # admin.py
# from django.contrib import admin
# from .models import Organization

# class OrganizationAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     fields = ('name', 'form_style', 'fields')
#     filter_horizontal = ()
    
#     def formfield_for_dbfield(self, db_field, **kwargs):
#         if db_field.name == 'fields':
#             kwargs['widget'] = admin.widgets.AdminTextareaWidget()  # Textarea to type JSON or list
#         return super().formfield_for_dbfield(db_field, **kwargs)

# admin.site.register(Organization, OrganizationAdmin)

from django.core.management.base import BaseCommand
from iframe_form.models import Organization

class Command(BaseCommand):
    help = 'Create default organizations'
    
    def handle(self, *args, **options):
        default_orgs = [
            "Organization A",
            "Organization B",
            "Organization C"
        ]
        
        for org_name in default_orgs:
            org, created = Organization.objects.get_or_create(name=org_name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created organization: {org.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Organization already exists: {org.name}')
                )