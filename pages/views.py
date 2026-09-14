from django.shortcuts import render,redirect, get_object_or_404
from .models import Page
from django.core.mail import send_mail
from django.contrib import messages
from .contact import ContactForm

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'pages/page.html', {'page': page})

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            send_mail(
                cd['subject'],
                cd['message'],
                cd['email'],
                ['receiver@email.com'],
                fail_silently=False,
            )

            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  # IMPORTANT: use name, not URL
    else:
        form = ContactForm()

    return render(request, 'pages/contact.html', {'form': form})