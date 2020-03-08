from django.shortcuts import render
from .forms import BookingForm
from .models import Booking


# Create your views here.
def index(request):
    ctx = {}

    return render(request, 'index.html', ctx)


def form(request):
    """
     Create object by form via Booking model
    """
    if request.method == 'POST':
        f = BookingForm(request.POST)
        if f.is_valid():
            booking = f.save(commit=False)
            booking.save()
        else:
            BookingForm()

    ctx = {
        'form': BookingForm
    }

    return render(request, 'form.html', ctx)
