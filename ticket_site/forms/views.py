from django.shortcuts import render, redirect

from .forms import TicketForm


def alibaba(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            time = form.cleaned_data.get('time')
            is_qom_tehran = form.cleaned_data.get('is_qom_tehran', False)
            return redirect('/alibaba')
            return render(request, "success.html")
    else:
        form = TicketForm()

    return render(request, "alibaba.html", {"form": form})
