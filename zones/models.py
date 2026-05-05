from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta, date

# Create your models here.
class Zone(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre de la zona')
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(verbose_name='Capacidad máxima')
    is_available = models.BooleanField(default=True, verbose_name='Disponible')
    zone_picture = models.ImageField(upload_to='zone_pictures/', blank=True, null=True)

    class Meta:
        verbose_name = 'Espacio común'
        verbose_name_plural = 'Espacios comunes'

    def __str__(self):
        return self.name
    
    def get_availability_for_month(self, year, month):
        """Retorna las fechas reservadas de un mes específico"""
        # Obtener el primer y último día del mes
        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(year, month + 1, 2) - timedelta(days=1)
        
        # Obtener todas las reservas del mes
        bookings = self.bookings.filter(
            event_date__gte=first_day,
            event_date__lte=last_day
        ).values_list('event_date__date', flat=True)
        
        booked_dates = [str(b) for b in set(bookings)]
        return {
            'booked_dates': booked_dates,
            'year': year,
            'month': month
        }
    
class Booking(models.Model):
    RECURRENCE_CHOICES = [
        ('NONE', 'No recurrente'),
        ('WEEKLY', 'Semanal'),
        ('BIWEEKLY', 'Cada dos semanas'),
        ('MONTHLY', 'Mensual'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    resource = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='bookings')
    reservation_date = models.DateTimeField('Fecha de reserva', auto_now_add=True)
    event_date = models.DateTimeField('Fecha del evento', default=timezone.now)
    
    # Campos de recurrencia
    is_recurring = models.BooleanField('Es recurrente', default=False)
    recurrence_pattern = models.CharField(
        'Patrón de recurrencia',
        max_length=20,
        choices=RECURRENCE_CHOICES,
        default='NONE'
    )
    recurrence_end_date = models.DateField(
        'Fecha de finalización',
        null=True,
        blank=True,
        help_text='Fecha en la que termina la recurrencia'
    )
    parent_booking = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='recurring_instances',
        null=True,
        blank=True,
        help_text='Reserva padre si es una instancia de una recurrencia'
    )

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['event_date']

    def __str__(self):
        recurrence_label = f" ({self.get_recurrence_pattern_display()})" if self.is_recurring else ""
        return f"Reserva para {self.resource.name} el {self.event_date}{recurrence_label}"

    def is_past(self):
        """Verifica si la reserva ya pasó"""
        return self.event_date.date() < date.today()
    
    def get_overlapping_recurring_dates(self):
        """Busca solapamientos en las fechas generadas por la recurrencia"""
        if not self.is_recurring or not self.recurrence_pattern or self.recurrence_pattern == 'NONE':
            return []
        
        if not self.recurrence_end_date:
            return []
            
        pattern_days = {
            'WEEKLY': 7,
            'BIWEEKLY': 14,
            'MONTHLY': 30,
        }
        
        increment_days = pattern_days.get(self.recurrence_pattern, 7)
        current_event_date = self.event_date + timedelta(days=increment_days)
        
        if current_event_date.tzinfo is None and self.event_date.tzinfo is not None:
            current_event_date = timezone.make_aware(current_event_date.replace(tzinfo=None))
            
        conflicts = []
        while current_event_date.date() <= self.recurrence_end_date:
            if Booking.objects.filter(
                resource=self.resource,
                event_date__date=current_event_date.date()
            ).exists():
                conflicts.append(current_event_date.date())
            current_event_date = current_event_date + timedelta(days=increment_days)
            
        return conflicts

    def generate_recurring_instances(self):
        """Genera las instancias de una reserva recurrente"""
        if not self.is_recurring or not self.recurrence_pattern or self.recurrence_pattern == 'NONE':
            return []
        
        if not self.recurrence_end_date:
            return []
        
        instances = []
        
        # Mapeo de patrones a días
        pattern_days = {
            'WEEKLY': 7,
            'BIWEEKLY': 14,
            'MONTHLY': 30,
        }
        
        increment_days = pattern_days.get(self.recurrence_pattern, 7)
        
        # Empezar desde la próxima fecha sumando el patrón de recurrencia
        current_event_date = self.event_date + timedelta(days=increment_days)
        
        # Asegurar que current_event_date es un datetime
        if current_event_date.tzinfo is None and self.event_date.tzinfo is not None:
            current_event_date = timezone.make_aware(current_event_date.replace(tzinfo=None))
        
        while current_event_date.date() <= self.recurrence_end_date:
            # Verificar que no hay conflicto de reserva para esa fecha exacta
            if not Booking.objects.filter(
                resource=self.resource,
                event_date__date=current_event_date.date()
            ).exists():
                instance = Booking(
                    user=self.user,
                    resource=self.resource,
                    event_date=current_event_date,
                    is_recurring=False,
                    parent_booking=self,
                )
                instances.append(instance)
            
            # Incrementar a la siguiente ocurrencia
            current_event_date = current_event_date + timedelta(days=increment_days)
        
        return instances