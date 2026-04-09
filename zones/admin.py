from django.contrib import admin
from zones.models import Zone, Booking

# Register your models here.
@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    model = Zone
    list_display = ('pk', 'name', 'capacity', 'is_available')

    # AQUÍ ESTÁ EL TRUCO: 
    # Definimos qué campos de la lista de arriba funcionarán como enlaces
    list_display_links = ('pk', 'name') # Ahora el pk y Nombre te llevarán al detalle
    
    # Opcional: para que sea más pro, podemos añadir filtros y búsqueda
    list_filter = ('is_available',)
    search_fields = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    model = Booking
    list_display = ('pk', 'resource', 'reservation_date', 'event_date')

    list_display_links = ('pk', 'resource')

    list_filter = ('reservation_date', 'event_date')
    search_fields = ('resource__name', 'reservation_date', 'event_date')
