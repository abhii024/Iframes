# iframe_form/views.py
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import ContactForm
from .models import ContactSubmission
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
@csrf_exempt
def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save to database
            submission = form.save(commit=False)
            submission.ip_address = request.META.get('REMOTE_ADDR')
            submission.save()
            print(f"Form submitted: {submission}")
            # Send email
            # Send email from user's email to your address
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
                    from_email=submission.email,  # Send from user's email
                    to=['abhi.w3web@gmail.com'],  # Your email address
                    reply_to=[submission.email],
                )
                email.content_subtype = "html"  # Set content type to HTML
                email.send()
                
                return redirect('contact_success')
            
            except Exception as e:
                # Log the error but still show success to user
                import logging
                logging.error(f"Failed to send email: {str(e)}")
                return redirect('contact_success')
        
        # Form is invalid - show errors
        return render(request, 'iframe_form/contact_form.html', {
            'form': form,
            'error': "Please correct the errors below"
        })
    
    # GET request - show empty form
    return render(request, 'iframe_form/contact_form.html', {
        'form': ContactForm()
    })

def contact_success(request):
    return render(request, 'iframe_form/success.html')

def contact_iframe(request):
    return render(request, 'iframe_form/iFrame.html')
