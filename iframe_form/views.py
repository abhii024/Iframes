from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .forms import DynamicContactForm
from .models import Organization, ContactSubmission
import json
import requests

@xframe_options_exempt
@csrf_exempt
@require_http_methods(["GET", "POST"])
def contact_form(request):
    org_id = request.GET.get('org_id') or request.POST.get('organization_id')
    if not org_id:
        return HttpResponse("Organization ID not provided", status=400)

    organization = get_object_or_404(Organization, id=org_id)
    captcha_error = None

    if request.method == "POST":
        form = DynamicContactForm(request.POST, organization=organization)
        
        # Verify hCaptcha
        captcha_token = request.POST.get('h-captcha-response')
        if not captcha_token:
            captcha_error = "Please complete the CAPTCHA verification"
        elif not verify_hcaptcha(captcha_token):
            captcha_error = "Invalid CAPTCHA. Please try again."
        
        if not captcha_error and form.is_valid():
            submission = form.save()
            return render(request, "iframe_form/success.html", {
                "organization": organization
            })
        else:
            print("Form errors:", form.errors)
    else:
        form = DynamicContactForm(organization=organization)
    
    # Check for HTML fields to handle them differently in the template
    html_fields = []
    if organization.form_fields:
        for field in organization.form_fields:
            if field.get('type') == 'html':
                html_fields.append(field.get('name'))
    
    return render(request, "iframe_form/show_form.html", {
        "organization": organization,
        "form": form,
        "html_fields": html_fields,
        "custom_css": organization.form_style,
        "HCAPTCHA_SITEKEY": settings.HCAPTCHA_SITEKEY,
        "captcha_error": captcha_error
    })

def verify_hcaptcha(token):
    data = {
        'secret': settings.HCAPTCHA_SECRET,
        'response': token
    }
    try:
        response = requests.post('https://hcaptcha.com/siteverify', data=data, timeout=5)
        return response.json().get('success', False)
    except:
        return False

def contact_success(request):
    return render(request, 'iframe_form/success.html')

def create_organization(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            org = Organization.objects.create(name=name)
            return redirect('edit_organization', org_id=org.id)
    
    return render(request, "iframe_form/create_organization.html")

def edit_organization(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    
    if request.method == "POST":
        form_fields_json = request.POST.get("form_fields", "[]")
        try:
            form_fields = json.loads(form_fields_json)
            organization.form_fields = form_fields
        except json.JSONDecodeError:
            organization.form_fields = []
        
        organization.form_style = request.POST.get("form_style", "")
        organization.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'form_fields': organization.form_fields,
                'form_style': organization.form_style
            })
        return redirect('edit_organization', org_id=org_id)

    context = {
        "organization": organization,
        "field_types": Organization.FIELD_TYPES
    }
    return render(request, "iframe_form/edit_organization.html", context)

def organization_list(request):
    organizations = Organization.objects.all()
    return render(request, "iframe_form/organization_list.html", {
        "organizations": organizations
    })