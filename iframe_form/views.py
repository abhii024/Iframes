# iframe_form/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import ContactForm
from .models import ContactSubmission, Organization
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponse
# Create default organizations if they don't exist
def create_default_organizations():
    if not Organization.objects.filter(id=1).exists():
        Organization.objects.create(id=1, name="Default Organization", form_style="")
    
    if not Organization.objects.filter(id=2).exists():
        Organization.objects.create(
            id=2, 
            name="Red Border Organization", 
            form_style="""
                .form-container {
                    border: 2px solid red;
                    padding: 20px;
                    border-radius: 5px;
                }
                h2 {
                    color: red;
                }
            """
        )

@xframe_options_exempt
@csrf_exempt
def contact_form(request):
    org_id = request.GET.get('org_id')
    if not org_id:
        return HttpResponse("Organization ID not provided", status=400)

    organization = get_object_or_404(Organization, id=org_id)

    if request.method == "POST":
        form = ContactForm(request.POST, selected_fields=organization.fields)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.organization = organization
            submission.save()
            return HttpResponse("Form submitted successfully!")
    else:
        form = ContactForm(selected_fields=organization.fields)

    # Pre-fill organization_id hidden field
    form.fields['organization_id'].initial = organization.id

    return render(request, "iframe_form/contact_form.html", {
        "organization": organization,
        "form": form,
        "custom_css": organization.form_style
    })
 
def contact_success(request):
    return render(request, 'iframe_form/success.html')

def contact_iframe(request):
    return render(request, 'iframe_form/iFrame.html')
# Other views remain the same...

def edit_organization(request):
    organizations = Organization.objects.all()
    selected_org = None
    available_fields = ['name', 'email', 'subject', 'message']  
    selected_fields = []

    if request.method == "POST":
        org_id = request.POST.get("organization")
        if org_id:
            selected_org = get_object_or_404(Organization, id=org_id)

            # Save fields & CSS
            selected_fields = request.POST.getlist("fields")
            selected_org.fields = selected_fields  # ✅ Save to JSONField
            selected_org.form_style = request.POST.get("form_style", "")
            selected_org.save()

            return redirect(f"{request.path}?organization={selected_org.id}")

    elif request.method == "GET" and "organization" in request.GET:
        org_id = request.GET.get("organization")
        selected_org = get_object_or_404(Organization, id=org_id)
        selected_fields = selected_org.fields  # ✅ Load saved fields

    context = {
        "organizations": organizations,
        "selected_org": selected_org,
        "available_fields": available_fields,
        "selected_fields": selected_fields
    }
    return render(request, "iframe_form/edit_organization.html", context)