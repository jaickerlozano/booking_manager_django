from django.shortcuts import render
from .forms import ReservationModelFormCreate
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Booking


# Create your views here.
class ReservationCreateView(CreateView):
    model = Booking
    form_class = ReservationModelFormCreate
    template_name = 'reservations/reservation_create.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, "¡Reserva creada exitosamente!")
        return super().form_valid(form)