import os
import json
from django.conf import settings
from .models import Organization

def load_organizations_from_json():
    json_path = os.path.join(settings.BASE_DIR, 'organizations.json')

    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
            for org in data:
                print(f"Loading organization: {org.get('name', 'Unnamed')}")
                Organization.objects.get_or_create(
                    name=org.get("name", ""),
                    defaults={
                        "form_style": org.get("form_style", ""),
                        "fields": org.get("fields", [])
                    }
                )
