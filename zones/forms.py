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


class ZoneCreateModelForm(ModelForm):
    class Meta:
        model = Zone
        fields = ['name', 'description', 'capacity']


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