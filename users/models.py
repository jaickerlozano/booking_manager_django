from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class Profile(models.Model):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    birth_date = models.DateField(verbose_name='Fecha de nacimiento', blank=True, null=True)

    class Meta:
        abstract = True

class Administrator(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='administrator_profile')

    class Meta:
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Administrador"
    
    # Esta es otra forma de mostrar el nombre del usuario, pero la anterior es más clara y directa. Se utiliza para mostrar el nombre completo del usuario o su nombre de usuario si el nombre completo no está disponible.
    # def __str__(self):
    # # Esto devuelve "Nombre Apellido" o el "username" si los otros están vacíos
    # full_name = self.user.get_full_name() or self.user.username
    # return f"{full_name} - Departamento {self.department}"


class Resident(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resident_profile')
    department = models.CharField(max_length=10, verbose_name='Número de departamento')

    class Meta:
        verbose_name = 'Residente'
        verbose_name_plural = 'Residentes'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Departamento {self.department}"