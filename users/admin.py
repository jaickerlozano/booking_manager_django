from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from users.models import Administrator, Resident


@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    model = Resident
    # Esto es lo que verás en la tabla principal
    list_display = ('get_name', 'department', 'get_email')
    # Permite buscar por nombre de usuario o departamento
    search_fields = ('user__first_name', 'user__last_name', 'department')

    def get_name(self, obj):
        return obj.user.get_full_name()
    get_name.short_description = 'Nombre Completo'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    model = Administrator
    list_display = ('get_name', 'get_email')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')

    def get_name(self, obj):
        return obj.user.get_full_name()
    get_name.short_description = 'Nombre'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'