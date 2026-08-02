from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ContactForm


def contact_view(request):
    """Handle contact form submissions."""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Thank you for contacting us. We will get back to you soon.")
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form})
