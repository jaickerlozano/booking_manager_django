from django.shortcuts import render, redirect
from .forms import ReservationModelFormCreate, ZoneCreateModelForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Booking, Zone
from datetime import datetime

# Create your views here.
class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = ReservationModelFormCreate
    template_name = 'reservations/reservation_create.html'
    success_url = reverse_lazy('profile')
    
    # Con este método lo que hacemos es asignar el usuario logueado a la reserva que se está creando. De esta forma, cada reserva estará asociada al usuario que la creó, lo cual es fundamental para luego mostrar las reservas en el perfil del usuario.
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.resource = form.cleaned_data['resource']
        event_date = form.cleaned_data['event_date'].date()
        current_date = datetime.now().date()  # La fecha actual

        if event_date <= current_date:
            messages.error(self.request, "La fecha del evento no puede ser antes o igual a la fecha actual. Intente nuevamente con una fecha válida.")
            return self.form_invalid(form)

        if Booking.objects.filter(resource=form.instance.resource, event_date__date=event_date).exists():
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


class BookingListView(ListView):
    model = Booking
    template_name = 'reservations/reservation_list.html'
    context_object_name = 'bookings'


class BookingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Booking
    fields = ['resource', 'event_date']
    template_name = 'reservations/reservation_update.html'
    success_url = reverse_lazy('profile')

    def test_func(self):
        # Comprueba si el usuario actual es el dueño de la reserva a actualizar
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        # Qué hacer si test_func devuelve False (cuando no es el dueño)
        messages.error(self.request, "No tienes permiso para editar esta reserva.")
        return redirect('profile')

    def form_valid(self, form):
        messages.success(self.request, "¡Reserva actualizada exitosamente!")
        return super().form_valid(form)
    

class BookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Booking
    template_name = 'reservations/reservation_delete.html'
    success_url = reverse_lazy('profile')

    def test_func(self):
        # Comprueba si el usuario actual es el dueño de la reserva a eliminar
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para eliminar esta reserva.")
        return redirect('profile')

    def form_valid(self, form):
        booking = self.get_object()
        booking_id = booking.pk
        booking.delete() # Forma estándar de eliminar la instancia
        messages.success(self.request, f"¡Reserva eliminada exitosamente! {booking_id}")
        return redirect(self.success_url)
    

class ZoneCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Zone
    form_class = ZoneCreateModelForm
    template_name = 'zones/zone_create.html'
    success_url = reverse_lazy('dashboard_admin')

    def test_func(self):
        # Verifica si el usuario logueado tiene un perfil de administrador
        return hasattr(self.request.user, 'administrator_profile')

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para crear espacios comunes.")
        return redirect('profile')
    
    def form_valid(self, form):
        messages.success(self.request, "¡Espacio común creado exitosamente!")
        return super().form_valid(form)


class ZoneListView(ListView):
    model = Zone
    template_name = 'zones/zone_list.html'
    context_object_name = 'zones'   


class ZoneUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Zone
    fields = ['name', 'description']
    template_name = 'zones/zone_update.html'
    success_url = reverse_lazy('dashboard_admin')

    def test_func(self):
        # Verifica si el usuario logueado tiene un perfil de administrador
        return hasattr(self.request.user, 'administrator_profile')

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para editar espacios comunes.")
        return redirect('profile')
    
    def form_valid(self, form):
        messages.success(self.request, "¡Espacio común actualizado exitosamente!")
        return super().form_valid(form)
    

class ZoneDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Zone
    template_name = 'zones/zone_delete.html'
    success_url = reverse_lazy('dashboard_admin')

    def test_func(self):
        # Verifica si el usuario logueado tiene un perfil de administrador
        return hasattr(self.request.user, 'administrator_profile')

    def handle_no_permission(self):
        # Verifica si el usuario logueado tiene un perfil de administrador
        messages.error(self.request, "No tienes permiso para eliminar espacios comunes.")
        return redirect('profile')
    
    def form_valid(self, form):
        zone = self.get_object()
        zone_id = zone.pk
        zone.delete() # Forma estándar de eliminar la instancia
        messages.success(self.request, f"¡Espacio común eliminado exitosamente! {zone_id}")
        return redirect(self.success_url)
