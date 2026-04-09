from django import forms
from .models import Zone, Booking
from django.forms import ModelForm

# Create your forms here.
class BookingModelFormCreate(ModelForm):
    class Meta:
        model = Booking
        fields = ['resource', 'event_date']
        widgets = {
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }   