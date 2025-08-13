# from django.apps import AppConfig


# class IframeFormConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'iframe_form'



# app_name/apps.py
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iframe_form'

    def ready(self):
        from .utils import load_organizations_from_json
        try:
            load_organizations_from_json()
        except:
            pass
