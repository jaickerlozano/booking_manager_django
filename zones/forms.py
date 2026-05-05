from django import forms
from .models import Zone, Booking
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils import timezone


# Create your forms here.
class ReservationModelFormCreate(ModelForm):
    class Meta: 
        model = Booking
        fields = ['resource', 'event_date', 'is_recurring', 'recurrence_pattern', 'recurrence_end_date']
        widgets = {
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'recurrence_end_date': forms.DateInput(attrs={'type': 'date'}),
            'is_recurring': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-brand-blue bg-gray-100 border-gray-300 rounded focus:ring-brand-blue'
            }),
            'recurrence_pattern': forms.Select(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-brand-blue focus:border-brand-blue block w-full p-2.5'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resource'].label = "Espacio a reservar"
        self.fields['event_date'].label = "Fecha y hora del evento"
        self.fields['is_recurring'].label = "¿Deseas que sea una reserva recurrente?"
        self.fields['recurrence_pattern'].label = "Patrón de recurrencia"
        self.fields['recurrence_end_date'].label = "¿Hasta cuándo deseas que sea recurrente?"
        
        # No son requeridos por defecto, pero se validarán en clean()
        self.fields['recurrence_pattern'].required = False
        self.fields['recurrence_end_date'].required = False
        
        for field in self.fields.values():
            if field.widget.__class__.__name__ != 'CheckboxInput':
                field.widget.attrs.setdefault('class', 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-brand-blue focus:border-brand-blue block w-full p-2.5')
    
    def clean(self):
        cleaned_data = super().clean()
        is_recurring = cleaned_data.get('is_recurring')
        recurrence_pattern = cleaned_data.get('recurrence_pattern')
        recurrence_end_date = cleaned_data.get('recurrence_end_date')
        
        # Si es recurrente, validar que los campos sean requeridos
        if is_recurring:
            if not recurrence_pattern or recurrence_pattern == 'NONE':
                self.add_error('recurrence_pattern', 'Este campo es requerido si la reserva es recurrente.')
            if not recurrence_end_date:
                self.add_error('recurrence_end_date', 'Este campo es requerido si la reserva es recurrente.')
            elif recurrence_end_date <= cleaned_data.get('event_date', timezone.now()).date():
                self.add_error('recurrence_end_date', 'La fecha de finalización debe ser posterior a la fecha del evento.')
        
        return cleaned_data


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
        fields = ['user', 'resource', 'event_date', 'is_recurring', 'recurrence_pattern', 'recurrence_end_date']
        widgets = {
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'recurrence_end_date': forms.DateInput(attrs={'type': 'date'}),
            'is_recurring': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-brand-blue bg-gray-100 border-gray-300 rounded focus:ring-brand-blue'
            }),
            'recurrence_pattern': forms.Select(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-brand-blue focus:border-brand-blue block w-full p-2.5'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].label_from_instance = lambda obj: f"{obj.get_full_name()} - Depto: {obj.resident_profile.department}"
        self.fields['resource'].label = "Espacio a reservar"
        self.fields['event_date'].label = "Fecha y hora del evento"
        self.fields['is_recurring'].label = "¿Deseas que sea una reserva recurrente?"
        self.fields['recurrence_pattern'].label = "Patrón de recurrencia"
        self.fields['recurrence_end_date'].label = "¿Hasta cuándo deseas que sea recurrente?"
        
        # No son requeridos por defecto, pero se validarán en clean()
        self.fields['recurrence_pattern'].required = False
        self.fields['recurrence_end_date'].required = False
        
        # Agregamos las clases de Tailwind y Flowbite a los inputs (incluyendo el select de usuario)
        for field in self.fields.values():
            if field.widget.__class__.__name__ != 'CheckboxInput':
                field.widget.attrs.setdefault('class', 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-brand-blue focus:border-brand-blue block w-full p-2.5')
    
    def clean(self):
        cleaned_data = super().clean()
        is_recurring = cleaned_data.get('is_recurring')
        recurrence_pattern = cleaned_data.get('recurrence_pattern')
        recurrence_end_date = cleaned_data.get('recurrence_end_date')
        
        # Si es recurrente, validar que los campos sean requeridos
        if is_recurring:
            if not recurrence_pattern or recurrence_pattern == 'NONE':
                self.add_error('recurrence_pattern', 'Este campo es requerido si la reserva es recurrente.')
            if not recurrence_end_date:
                self.add_error('recurrence_end_date', 'Este campo es requerido si la reserva es recurrente.')
            elif recurrence_end_date <= cleaned_data.get('event_date', timezone.now()).date():
                self.add_error('recurrence_end_date', 'La fecha de finalización debe ser posterior a la fecha del evento.')
        
        return cleaned_data