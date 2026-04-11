from django.shortcuts import render, redirect
from .forms import BookingModelFormCreate
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Booking


# Create your views here.
class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingModelFormCreate
    template_name = 'reservations/reservation_create.html'
    success_url = reverse_lazy('profile')
    
    # Con este método lo que hacemos es asignar el usuario logueado a la reserva que se está creando. De esta forma, cada reserva estará asociada al usuario que la creó, lo cual es fundamental para luego mostrar las reservas en el perfil del usuario.
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.resource = form.cleaned_data['resource']
        event_date = form.cleaned_data['event_date']

        if Booking.objects.filter(resource=form.instance.resource, event_date__date=event_date.date()).exists():
            messages.error(self.request, f'El/La {form.instance.resource.name} ya está reservado para la fecha seleccionada. Por favor, elige otro espacio común o fecha.')
            return self.form_invalid(form)

        form.instance.resource.save()  # Guardar el cambio en el recurso
        messages.success(self.request, "¡Reserva creada exitosamente!")
        return super().form_valid(form)

        


class BookingDetailView(DetailView):
    model = Booking
    template_name = 'reservations/reservation_detail.html'
    context_object_name = 'booking'

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     form.instance.booking = self.get_object() # Este es el espacio que estoy viendo en la detailview
    #     return super(BookingDetailView, self).form_valid(form)


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    fields = ['resource', 'event_date']
    template_name = 'reservations/reservation_update.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, "¡Reserva actualizada exitosamente!")
        return super().form_valid(form)


class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'reservations/reservation_delete.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        self.object = self.get_object().resource  # Obtener el recurso asociado a la reserva que se va a eliminar
        self.object.bookings.filter(pk=self.get_object().pk).delete()  # Eliminar la reserva actual
        self.object.save()  # Guardar el cambio en el recurso
        messages.success(self.request, f"¡Reserva eliminada exitosamente! {self.object.pk}")
        return redirect(self.success_url)
