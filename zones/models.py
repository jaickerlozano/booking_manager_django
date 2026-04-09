from django.db import models
from django.utils import timezone

# Create your models here.
class Zone(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre de la zona')
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(verbose_name='Capacidad máxima')
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Espacio común'
        verbose_name_plural = 'Espacios comunes'

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    resource = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='bookings')
    reservation_date = models.DateTimeField('Fecha de reserva', auto_now_add=True) # -> Sólo fecha
    event_date = models.DateTimeField('Fecha del evento', default=timezone.now) # -> Fecha y hora del evento

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
    
    def __str__(self):
        return f"Reserva para {self.resource.name} el {self.event_date} (Reservado el {self.reservation_date})"

# class Availability(models.Model):
#     available = models.BooleanField(Zone, default=True)
#     resource = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='availabilities')
    
#     def __str__(self):
#         return f"{self.resource.name} - {'Disponible' if self.available else 'No disponible'}"