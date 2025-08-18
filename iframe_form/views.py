# iframe_form/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import ContactForm
from .models import ContactSubmission, Organization
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
import requests
# Create default organizations if they don't exist
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
        form = ContactForm(
            request.POST, 
            selected_fields=organization.fields,
            required_fields=organization.required_fields
        )
        
        # Verify hCaptcha
        captcha_token = request.POST.get('h-captcha-response')
        if not captcha_token:
            captcha_error = "Please complete the CAPTCHA verification"
        elif not verify_hcaptcha(captcha_token):
            captcha_error = "Invalid CAPTCHA. Please try again."
        
        if not captcha_error and form.is_valid():
            submission = form.save(commit=False)
            submission.organization = organization
            submission.ip_address = request.META.get('REMOTE_ADDR')
            submission.save()
            return render(request, "iframe_form/success.html", {
                "organization": organization
            })
        else:
            # If form is invalid, keep the submitted data
            print("Form errors:", form.errors)
    else:
        form = ContactForm(
            selected_fields=organization.fields,
            required_fields=organization.required_fields
        )
    print("Form fields:", form.fields)
    return render(request, "iframe_form/contact_form.html", {
        "organization": organization,
        "form": form,
        "custom_css": organization.form_style,
        "HCAPTCHA_SITEKEY": settings.HCAPTCHA_SITEKEY,
        "captcha_error": captcha_error
    })
    
def verify_hcaptcha(token):
    data = {
        'secret': settings.HCAPTCHA_SECRET,
        'response': token
    }
    response = requests.post('https://hcaptcha.com/siteverify', data=data)
    return response.json()

def contact_success(request):
    return render(request, 'iframe_form/success.html')

def contact_iframe(request):
    return render(request, 'iframe_form/iFrame.html')
# Other views remain the same...

def edit_organization(request):
    organizations = Organization.objects.all()
    selected_org = None
    available_fields = ['name', 'email', 'subject', 'message', 'phone']
    selected_fields = []
    required_fields = []

    if request.method == "POST":
        org_id = request.POST.get("organization")
        if org_id:
            selected_org = get_object_or_404(Organization, id=org_id)
            
            # Get selected fields and required fields from form
            selected_fields = request.POST.getlist("fields")
            required_fields = request.POST.getlist("required_fields")
            
            # Update organization data
            selected_org.fields = selected_fields
            selected_org.required_fields = required_fields
            selected_org.form_style = request.POST.get("form_style", "")
            selected_org.save()
            
            # Handle AJAX response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'fields': selected_fields,
                    'required_fields': required_fields,
                    'form_style': selected_org.form_style
                })
            return redirect(f"{request.path}?organization={selected_org.id}")

    elif request.method == "GET":
        if "organization" in request.GET:
            org_id = request.GET.get("organization")
            selected_org = get_object_or_404(Organization, id=org_id)
            selected_fields = selected_org.fields
            required_fields = selected_org.required_fields
            
            # For backward compatibility, if no required_fields exist, assume all are required
            if not hasattr(selected_org, 'required_fields') or not selected_org.required_fields:
                required_fields = selected_fields.copy()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'fields': selected_fields,
                    'required_fields': required_fields,
                    'form_style': selected_org.form_style
                })

    context = {
        "organizations": organizations,
        "selected_org": selected_org,
        "available_fields": available_fields,
        "selected_fields": selected_fields,
        "required_fields": required_fields
    }
    return render(request, "iframe_form/edit_organization.html", context)



