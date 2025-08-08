# iframe_form/views.py
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm

@xframe_options_exempt
@csrf_exempt
def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form data here (save to DB, send email, etc.)
            return render(request, 'iframe_form/success.html')
    else:
        form = ContactForm()
    
    return render(request, 'iframe_form/contact_form.html', {'form': form})

@xframe_options_exempt
def success_view(request):
    return render(request, 'iframe_form/success.html')