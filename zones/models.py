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
            last_day = date(year, month + 1, 1) - timedelta(days=1)
        
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    resource = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='bookings')
    reservation_date = models.DateTimeField('Fecha de reserva', auto_now_add=True) # -> Sólo fecha
    event_date = models.DateTimeField('Fecha del evento', default=timezone.now) # -> Fecha y hora del evento

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['event_date']  # Ordenar por fecha del evento, de más reciente a más antiguo
    
    def __str__(self):
        return f"Reserva para {self.resource.name} el {self.event_date} (Reservado el {self.reservation_date})"

# class Availability(models.Model):
#     available = models.BooleanField(Zone, default=True)
#     resource = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='availabilities')
    
#     def __str__(self):
#         return f"{self.resource.name} - {'Disponible' if self.available else 'No disponible'}"