from django import forms
from .models import Zone, Booking
from django.forms import ModelForm
from django.contrib.auth.models import User


# Create your forms here.
class ReservationModelFormCreate(ModelForm):
    class Meta: 
        model = Booking
        fields = ['resource', 'event_date']
        widgets = {
            'event_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resource'].label = "Espacio a reservar"
        self.fields['event_date'].label = "Fecha y hora del evento"
        
        # Agregamos las clases de Tailwind y Flowbite a los inputs
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-brand-blue focus:border-brand-blue block w-full p-2.5'
            })

class ZoneForm(ModelForm):
    class Meta:
        model = Zone
        fields = ['name', 'description', 'capacity', 'zone_picture', 'is_available']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_available'].label = "Habilitado"
        # Agregamos las clases de Tailwind y Flowbite a los inputs
        for field_name, field in self.fields.items():
            # El campo de imagen es diferente
            if field_name == 'zone_picture':
                 field.widget.attrs.update({
                    'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none'
                })
            # El campo de checkbox es diferente
            elif field_name == 'is_available':
                field.widget.attrs.update({
                    'class': 'w-4 h-4 text-brand-blue bg-gray-100 border-gray-300 rounded focus:ring-brand-blue'
                })
            else:
                field.widget.attrs.update({
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-brand-blue focus:border-brand-blue block w-full p-2.5'
                })


class AdminReservationModelFormCreate(ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(resident_profile__isnull=False),
        label="Residente",
        empty_label="Seleccione un residente"
    )

    class Meta:
        model = Booking
        fields = ['user', 'resource', 'event_date']
        widgets = {
            'event_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].label_from_instance = lambda obj: f"{obj.get_full_name()} - Depto: {obj.resident_profile.department}"
        self.fields['resource'].label = "Espacio a reservar"
        self.fields['event_date'].label = "Fecha y hora del evento"
        
        # Agregamos las clases de Tailwind y Flowbite a los inputs (incluyendo el select de usuario)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-brand-blue focus:border-brand-blue block w-full p-2.5'
            })