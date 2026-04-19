from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import Resident

class ResidentRegistrationForm(UserCreationForm):
    # 1. Definimos manualmente los campos que NO están en el modelo User
    # (Los que vienen de tu modelo Resident y de Profile)
    first_name = forms.CharField(max_length=30, label="Nombre") # Lo agrego aquí para colocar el label personalizado
    last_name = forms.CharField(max_length=30, label="Apellido")
    email = forms.EmailField(label="Correo electrónico")
    department = forms.CharField(max_length=10, label="Número de departamento")
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        label="Fecha de nacimiento",
        required=False
    )

    class Meta(UserCreationForm.Meta):
        # 2. El modelo principal es User
        model = User
        # 3. Campos del User que queremos en el formulario
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        # 4. Guardamos el usuario primero
        user = super().save(commit=commit)
        
        # 5. Creamos el perfil de Resident asociado a este usuario
        # Esto evita el IntegrityError que tenías al principio
        Resident.objects.create(
            user=user,
            department=self.cleaned_data['department'],
            birth_date=self.cleaned_data['birth_date']
            # la profile_picture la podrías manejar aquí también si la añades
        )
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = "Nombre de usuario"
        self.fields['username'].help_text = ""


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nombre de usuario"
        self.fields['password'].label = "Contraseña"
        
        # Agregamos las clases de Tailwind y Flowbite directamente a los inputs
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-brand-blue focus:border-brand-blue block w-full p-2.5'
            })


class ContactForm(forms.Form):
    name = forms.CharField(label='Nombre', max_length=100)
    email = forms.EmailField(label='Correo electrónico')
    message = forms.CharField(label='Mensaje', widget=forms.Textarea)
