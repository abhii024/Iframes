# iframe_form/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import ContactForm
from .models import ContactSubmission, Organization
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt

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
    create_default_organizations()
    
    org_id = request.GET.get('org_id', 1)  # Default to org 1 if not specified
    organization = get_object_or_404(Organization, id=org_id)
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save to database
            submission = form.save(commit=False)
            submission.ip_address = request.META.get('REMOTE_ADDR')
            submission.organization = organization
            submission.save()
            
            # Email sending logic remains the same...
            return redirect('contact_success')
        
        # Form is invalid - show errors
        return render(request, 'iframe_form/contact_form.html', {
            'form': form,
            'organization': organization,
            'error': "Please correct the errors below"
        })
    
    # GET request - show empty form
    form = ContactForm(initial={'organization_id': org_id})
    return render(request, 'iframe_form/contact_form.html', {
        'form': form,
        'organization': organization
    })
    
def contact_success(request):
    return render(request, 'iframe_form/success.html')

def contact_iframe(request):
    return render(request, 'iframe_form/iFrame.html')
# Other views remain the same...