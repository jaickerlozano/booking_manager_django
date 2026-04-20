from django import forms
from django.contrib.auth.models import User
from .models import Resident

class ResidentUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label="Nombre")
    last_name = forms.CharField(max_length=30, label="Apellido")
    email = forms.EmailField(label="Correo electrónico")
    
    # Añadimos phone_number ya que está en tu template. 
    # Al no existir en el modelo, lo marcamos como no requerido para evitar errores.
    phone_number = forms.CharField(max_length=20, label="Número de Teléfono", required=False)

    class Meta:
        model = Resident
        fields = ['profile_picture'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Inicializamos los campos con la información actual del usuario
        if self.instance and hasattr(self.instance, 'user'):
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

        # Inyectamos las clases de Tailwind a todos los inputs
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
            })

    def save(self, commit=True):
        resident = super().save(commit=False)
        user = resident.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            resident.save()
            
        return resident