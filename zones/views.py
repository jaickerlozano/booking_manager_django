from django.shortcuts import render, redirect
from .forms import ReservationModelFormCreate, ZoneForm, AdminReservationModelFormCreate
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Booking, Zone
from users.models import Resident
from datetime import datetime
from django.db.models import Count, F, Q
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

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

        # Guardar la reserva padre si es recurrente
        booking = form.save(commit=False)
        booking.user = self.request.user

        # Validar conflictos futuros de la recurrencia antes de guardar
        if booking.is_recurring and booking.recurrence_pattern != 'NONE':
            conflicts = booking.get_overlapping_recurring_dates()
            if conflicts:
                conflict_dates = ", ".join([d.strftime('%d/%m/%Y') for d in conflicts])
                messages.error(self.request, f'El/La {booking.resource.name} ya está reservado/a en estas fechas de la recurrencia: {conflict_dates}. Ajusta el periodo o elige otro espacio.')
                return self.form_invalid(form)

        booking.save()

        # Preparar información para la notificación
        nombre = self.request.user.first_name
        email = self.request.user.email
        
        # Generar instancias recurrentes si aplica
        if booking.is_recurring and booking.recurrence_pattern != 'NONE':
            instances = booking.generate_recurring_instances()
            Booking.objects.bulk_create(instances)
            
            recurrence_info = f"\n\nEsta es una reserva recurrente ({booking.get_recurrence_pattern_display()}) que finalizará el {booking.recurrence_end_date.strftime('%d/%m/%Y')}.\nSe han generado {len(instances)} instancias automáticas."
            message_content = f"¡{nombre}, tu reserva recurrente ha sido creada exitosamente! \nEspacio común: {booking.resource.name} \nFecha de inicio: {str(booking.event_date.date())} {recurrence_info}"
            
            send_mail(
                "Notificación de reserva recurrente",
                message_content,
                "jlozano.devcode@gmail.com",
                [email],
                fail_silently=True,
            )
            
            messages.success(self.request, f"¡Reserva recurrente creada! Se generaron {len(instances)} instancias.")
        else:
            message_content = f"¡{nombre}, tu reserva ha sido creada exitosamente! \nEspacio común: {booking.resource.name} \nFecha del evento: {str(booking.event_date.date())}"
            
            send_mail(
                "Notificación de reserva",
                message_content,
                "jlozano.devcode@gmail.com",
                [email],
                fail_silently=True,
            )
            
            messages.success(self.request, "¡Reserva creada exitosamente!")

        return super().form_valid(form)


class AdminBookingCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Booking
    form_class = AdminReservationModelFormCreate
    template_name = 'reservations/admin_reservation_create.html'
    success_url = reverse_lazy('dashboard_admin')

    # Este método verifica si 
    def test_func(self):
        return hasattr(self.request.user, 'administrator_profile')

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para realizar esta acción.")
        return redirect('profile')

    def form_valid(self, form):
        event_date = form.cleaned_data['event_date'].date()
        current_date = datetime.now().date()

        if event_date <= current_date:
            messages.error(self.request, "La fecha del evento no puede ser antes o igual a la fecha actual. Intente nuevamente con una fecha válida.")
            return self.form_invalid(form)

        if Booking.objects.filter(resource=form.instance.resource, event_date__date=event_date).exists():
            messages.error(self.request, f'El/La {form.instance.resource.name} ya está reservado para la fecha seleccionada. Por favor, elige otro espacio común o fecha.')
            return self.form_invalid(form)

        resident_user = form.cleaned_data['user']
        nombre = resident_user.first_name
        email = resident_user.email
        
        # Guardar la reserva
        booking = form.save(commit=False)
        booking.user = resident_user

        # Validar conflictos futuros de la recurrencia antes de guardar
        if booking.is_recurring and booking.recurrence_pattern != 'NONE':
            conflicts = booking.get_overlapping_recurring_dates()
            if conflicts:
                conflict_dates = ", ".join([d.strftime('%d/%m/%Y') for d in conflicts])
                messages.error(self.request, f'El/La {booking.resource.name} ya está reservado/a en estas fechas de la recurrencia: {conflict_dates}. Ajusta el periodo o elige otro espacio.')
                return self.form_invalid(form)

        booking.save()

        # Generar instancias recurrentes si aplica
        if booking.is_recurring and booking.recurrence_pattern != 'NONE':
            instances = booking.generate_recurring_instances()
            Booking.objects.bulk_create(instances)
            
            recurrence_info = f"\n\nEsta es una reserva recurrente ({booking.get_recurrence_pattern_display()}) que finalizará el {booking.recurrence_end_date.strftime('%d/%m/%Y')}.\nSe han generado {len(instances)} instancias automáticas."
            message_content = f"¡Hola {nombre}! \nEl administrador ha creado una reserva recurrente a tu nombre. \n\nDetalles de la reserva: \nEspacio común: {booking.resource.name} \nFecha de inicio: {str(booking.event_date.date())} {recurrence_info}"
            
            send_mail(
                "Notificación de reserva recurrente creada por administrador",
                message_content,
                "jlozano.devcode@gmail.com",
                [email],
                fail_silently=False,
            )
            
            messages.success(self.request, f"¡Reserva recurrente creada exitosamente para {resident_user.get_full_name()}! Se generaron {len(instances)} instancias.")
        else:
            message_content = f"¡Hola {nombre}! \nEl administrador ha creado una reserva a tu nombre. \n\nDetalles de la reserva: \nEspacio común: {booking.resource.name} \nFecha del evento: {str(booking.event_date.date())}"
            
            send_mail(
                "Notificación de reserva creada por administrador",
                message_content,
                "jlozano.devcode@gmail.com",
                [email],
                fail_silently=False,
            )
            
            messages.success(self.request, f"¡Reserva creada exitosamente para {resident_user.get_full_name()}!")

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
    context_object_name = 'bookings' # Aseguramos que el queryset filtrado se llame 'bookings' en el contexto
    
    def get_queryset(self):
        # Este método se encarga de obtener el queryset base y aplicar el filtro de búsqueda.
        # Solo retorna reservas que no son instancias de recurrencia (parent_booking__isnull=True)
        queryset = super().get_queryset().filter(parent_booking__isnull=True)
        query = self.request.GET.get('dept', '')
        if query:
            queryset = queryset.filter(
                Q(user__resident_profile__department__icontains=query) |
                Q(resource__name__icontains=query) |
                Q(user__first_name__icontains=query)
            )
        return queryset

    # Este método lo estoy utilizando para filtrar por departamentos y cantidad de reservas totales que tiene cada uno para luego mostrar en el context del template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 'bookings' ya está en el contexto gracias a get_queryset y context_object_name

        # Agrupamos por departamento para obtener la recurrencia de reservas
        context['ranking_departamentos'] = Booking.objects.filter(
            user__resident_profile__isnull=False,
            parent_booking__isnull=True
        ).annotate(
            departamento=F('user__resident_profile__department')
        ).values('departamento').annotate(
            total_reservas=Count('id')
        ).order_by('-total_reservas')[:3]

        # Obtener reservas recurrentes (parent_booking__isnull=True e is_recurring=True)
        context['recurring_bookings'] = Booking.objects.filter(
            parent_booking__isnull=True,
            is_recurring=True
        ).order_by('event_date')

        return context

    # 
    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Si es una solicitud AJAX, solo queremos devolver la lista filtrada de reservas.
            self.object_list = self.get_queryset() # Obtiene el queryset filtrado
            context = self.get_context_data() # Prepara el contexto, incluyendo 'bookings' (la lista filtrada)

            # Renderiza solo el template parcial con la lista de reservas
            return render(request, '_includes/_booking_list_partial.html', {'bookings': context['bookings']})
        
        # Para una solicitud GET normal, procede como siempre (renderiza el template completo)
        return super().get(request, *args, **kwargs)

class BookingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Booking
    fields = ['resource', 'event_date']
    template_name = 'reservations/reservation_update.html'
    success_url = reverse_lazy('profile')

    def test_func(self):
        # Comprueba si el usuario actual es el dueño de la reserva a actualizar o si tiene perfil de administrador
        return self.get_object().user.pk == self.request.user.pk or self.request.user.administrator_profile

    def handle_no_permission(self):
        # Qué hacer si test_func devuelve False (cuando no es el dueño)
        messages.error(self.request, "No tienes permiso para editar esta reserva.")
        return redirect('profile')

    def form_valid(self, form):
        nombre = self.request.user.first_name
        email = self.request.user.email
        message_content = f"¡{nombre}, tu reserva ha sido modificada exitosamente! \nEspacio común: {form.instance.resource.name} \nFecha del evento: {str(form.instance.event_date.date())}" # Mensaje que se inserta en el correo

        send_mail(
            "Notificación de reserva",
            message_content,
            "jlozano.devcode@gmail.com",
            [email],
            fail_silently=False,
        )

        messages.success(self.request, "¡Reserva actualizada exitosamente!") # Mensaje del template

        return super().form_valid(form)
    

class BookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Booking
    template_name = 'reservations/reservation_delete.html'
    success_url = reverse_lazy('profile')

    def test_func(self):
        # Comprueba si el usuario actual es el dueño de la reserva a eliminar o si tiene perfil de adminstrador
        return self.get_object().user.pk == self.request.user.pk or self.request.user.administrator_profile

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para eliminar esta reserva.")
        return redirect('profile')

    def form_valid(self, form):
        booking = self.get_object()
        booking_id = booking.pk
        name = self.request.user.first_name
        resource = booking.resource.name
        event_date = str(booking.event_date.date())
        email = self.request.user.email
        booking.delete() # Forma estándar de eliminar la instancia

        message_content = f"¡{name}, tu reserva del '{resource}' con fecha: {event_date}, ha sido eliminada exitosamente!" # Mensaje que se inserta en el correo
        send_mail(
            "Notificación de reserva",
            message_content,
            "jlozano.devcode@gmail.com",
            [email],
            fail_silently=False,
        )
        messages.success(self.request, f"¡Reserva eliminada exitosamente!")
        return redirect(self.success_url)


class CancelRecurringBookingView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Vista para cancelar una reserva recurrente y todas sus instancias"""
    
    def test_func(self):
        booking = Booking.objects.get(pk=self.kwargs['pk'])
        # Comprueba si el usuario actual es el dueño o administrador
        return booking.user.pk == self.request.user.pk or hasattr(self.request.user, 'administrator_profile')

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para cancelar esta reserva recurrente.")
        return redirect('reservation_list')

    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
            
            # Validar que sea una reserva recurrente padre
            if not booking.is_recurring or booking.parent_booking is not None:
                messages.error(request, "Esta no es una reserva recurrente válida.")
                return redirect('reservation_list')
            
            # Obtener información antes de eliminar
            nombre = booking.user.first_name
            email = booking.user.email
            resource = booking.resource.name
            recurrence_pattern = booking.get_recurrence_pattern_display()
            
            # Eliminar todas las instancias recurrentes
            instances_count = booking.recurring_instances.count()
            booking.recurring_instances.all().delete()
            
            # Eliminar la reserva padre
            booking.delete()
            
            # Enviar notificación
            message_content = (
                f"¡{nombre}, tu reserva recurrente ha sido cancelada exitosamente!\n\n"
                f"Detalles:\n"
                f"Espacio común: {resource}\n"
                f"Patrón: {recurrence_pattern}\n"
                f"Instancias eliminadas: {instances_count}"
            )
            send_mail(
                "Notificación: Reserva recurrente cancelada",
                message_content,
                "jlozano.devcode@gmail.com",
                [email],
                fail_silently=False,
            )
            
            messages.success(request, f"¡Reserva recurrente cancelada! Se eliminaron {instances_count} instancias.")
            
        except Booking.DoesNotExist:
            messages.error(request, "La reserva recurrente no fue encontrada.")
        except Exception as e:
            messages.error(request, f"Error al cancelar la reserva: {str(e)}")
        
        return redirect('reservation_list')


class ZoneCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Zone
    form_class = ZoneForm
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


class ZoneDetailView(DetailView):
    model = Zone
    template_name = 'zones/zone_detail.html'
    context_object_name = 'zone'   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = hasattr(self.request.user, 'administrator_profile')
        return context


class ZoneUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Zone
    form_class = ZoneForm
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


class ZoneAvailabilityView(View):
    """API View que retorna disponibilidad de una zona en formato JSON"""
    
    def get(self, request, zone_id):
        try:
            zone = Zone.objects.get(pk=zone_id)
            year = int(request.GET.get('year', datetime.now().year))
            month = int(request.GET.get('month', datetime.now().month))
            
            # Validar que el mes y año sean válidos
            if month < 1 or month > 12:
                return JsonResponse({'success': False, 'error': 'Mes inválido'}, status=400)
            
            availability = zone.get_availability_for_month(year, month)
            
            return JsonResponse({
                'success': True,
                'zone': zone.name,
                'zone_id': zone.pk,
                'booked_dates': availability['booked_dates'],
                'year': year,
                'month': month
            })
        except Zone.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Zona no encontrada'}, status=404)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Parámetros inválidos'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    def get_recurring_bookings(self):
        """Obtiene las reservas recurrentes del usuario"""
        return self.request.user.bookings.filter(
            is_recurring=True,
            recurrence_pattern__in=['WEEKLY', 'BIWEEKLY', 'MONTHLY']
        ).distinct()
