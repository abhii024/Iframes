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
            try:
                email = EmailMessage(
                    subject=f"New Contact Form Submission: {submission.subject}",
                    body=f"""
                    <html>
                    <body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto;">
                        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px;">
                            <h2 style="color: #2c3e50;">New Contact Form Submission</h2>
                            
                            <div style="margin: 20px 0; padding: 15px; background-color: white; border-radius: 5px;">
                                <p><strong>From:</strong> {submission.name} &lt;{submission.email}&gt;</p>
                                <p><strong>Subject:</strong> {submission.subject}</p>
                                <p><strong>Message:</strong></p>
                                <div style="padding: 10px; border: 1px solid #eee; border-radius: 3px; margin-top: 5px;">
                                    {submission.message}
                                </div>
                            </div>
                            
                            <div style="margin-top: 20px; font-size: 0.9em; color: #7f8c8d;">
                                <p>You can reply directly to this email to respond to {submission.name.split()[0]}.</p>
                                <p>This message was sent via your website contact form.</p>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    to=[submission.email],  # Send to user's email
                    from_email='abhi.w3web@gmail.com',  # Your email address
                    reply_to=[submission.email],
                )
                email.content_subtype = "html"  # Set content type to HTML
                email.send()
            except Exception as e:
                # Optionally log the error or handle it as needed
                print(f"Error sending email: {e}")
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