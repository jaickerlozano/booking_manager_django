from django.shortcuts import render
from .forms import BookingModelFormCreate
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Booking


# Create your views here.
class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingModelFormCreate
    template_name = 'zones/booking_create.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, "¡Reserva creada exitosamente!")
        return super().form_valid(form)