from django.shortcuts import render

from .forms import TicketForm


def alibaba(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            age = form.cleaned_data["age"]
            return render(request, "success.html", {"name": name, "email": email, "age": age})
    else:
        form = TicketForm()

    return render(request, "alibaba.html", {"form": form})
