from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from .forms import ResidentRegistrationForm, LoginForm, ContactForm
from django.views.generic.edit import CreateView, FormView
from django.urls import reverse_lazy
from users.models import Resident
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView as DjangoLoginView
from zones.models import Zone, Booking
from django.db.models import Q
from django.core.mail import send_mail
from collections import Counter


# Create your views here.
class HomeView(TemplateView):
    template_name = 'general/home.html'


class LoginView(DjangoLoginView):
    template_name = 'general/login.html'
    authentication_form = LoginForm
    # Este método solo sirve para la clase LogineView. Si quisiera hacer algo similar en una vista normal, tendría que hacerlo en el método dispatch, como hice en el RegisterView.
    redirect_authenticated_user = True 

    def form_valid(self, form):
        # El mensaje solo se envía si el login fue exitoso en este momento
        messages.success(self.request, "¡Bienvenido de nuevo! Has iniciado sesión correctamente.")
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir dependiendo del tipo de perfil del usuario
        if hasattr(self.request.user, 'administrator_profile'):
            return reverse('dashboard_admin')
        return reverse('profile')


# Este decorador hace que solo los usuarios no autenticados puedan acceder a esta vista. Si un usuario autenticado intenta acceder, será redirigido al home. Es una forma más elegante de hacer lo mismo que hiciste en el dispatch del RegisterView, pero para vistas basadas en clases.
@method_decorator(user_passes_test(lambda u: not u.is_authenticated, login_url='home'), name='dispatch')
class RegisterView(CreateView):
    model = Resident
    template_name = 'general/register.html'
    form_class = ResidentRegistrationForm
    success_url = reverse_lazy('login')   
    
    # Este método se ejecuta antes de mostrar el formulario. Si el usuario ya está logueado, lo redirigimos al home para que no pueda registrarse de nuevo. 
    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         # Si ya está logueado, lo mandamos al home
    #         return redirect('home')
    #     return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        nombre = form.cleaned_data['first_name']
        email = form.cleaned_data['email']
        department = form.cleaned_data['department']
        
        # Ejecutamos el guardado de CreateView (que llama a form.save() internamente de forma segura)
        # y guardamos la respuesta para devolverla al final.
        response = super().form_valid(form)
        
        message_content = f"¡Hola {nombre}! \n Tu registro ha sido exitoso. Ahora puedes iniciar sesión. \nNombre del contacto: {nombre} \nCorreo electrónico: {email} \nNúmero de departamento: {department}" # Mensaje que se inserta en el correo

        send_mail(
            "Notificación de contacto",
            message_content,
            "jlozano.devcode@gmail.com",
            [email],
            fail_silently=True,
        )

        messages.success(self.request, "¡Registro exitoso! Ahora puedes iniciar sesión.")

        return response


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'general/contact.html'
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        nombre = form.cleaned_data['name']
        email = form.cleaned_data['email']
        mensaje = form.cleaned_data['message']
        message_content = f"Nombre del contacto: {nombre} \nCorreo electrónico: {email} \nMensaje: {mensaje}" # Mensaje que se inserta en el correo

        send_mail(
            "Notificación de contacto",
            message_content,
            "jlozano.devcode@gmail.com",
            ["jaickerlozano@outlook.com"],
            fail_silently=True,
        )
        messages.success(self.request, "¡Su mensaje ha sido enviado exitosamente! Nos contactaremos con usted a la brevedad.")

        return super().form_valid(form)


    
class LegalView(TemplateView):
    template_name = 'general/legal.html'

@login_required
def logout_view(request):
    logout(request) # Ahora sí, esta es la función de Django que importaste arriba
    messages.info(request, 'Sesión cerrada correctamente.') # Corregí INFO por info
    return redirect('home')


class ProfileView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'general/profile.html'

    def test_func(self):
        # Verifica si el usuario logueado tiene un perfil de administrador
        return hasattr(self.request.user, 'resident_profile')

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para acceder a este perfil.")
        if hasattr(self.request.user, 'administrator_profile'):
            return redirect('dashboard_admin')
        return redirect('home')

    # Con este método, cada vez que se renderice el profile, se añadirá al contexto la lista de reservas del usuario logueado. Esto es útil para mostrar las reservas en el perfil.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 1. Capturamos el filtro
        query = self.request.GET.get('dept', '') # Usamos 'dept' como el input principal
        
        # 2. Obtenemos el queryset base
        all_bookings = Booking.objects.all()
        
        # 3. Filtramos si hay búsqueda
        if query:
            all_bookings = all_bookings.filter(
                Q(user__resident_profile__department__icontains=query) |
                Q(resource__name__icontains=query) |
                Q(user__first_name__icontains=query)
            )

        context['zones'] = Zone.objects.all()
        context['bookings'] = self.request.user.bookings.all()
        context['all_bookings'] = all_bookings
        context['recurring_bookings'] = self.get_recurring_bookings()

        return context

    # 4. Sobreescribimos dispatch para manejar la petición AJAX
    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = self.get_context_data()
            # Si es AJAX, solo renderizamos un mini-template con la lista
            return render(request, '_includes/_all_bookings_list.html', context)
        return super().get(request, *args, **kwargs)
    
    def get_recurring_bookings(self):
        """Obtiene las reservas recurrentes (reservas padre) del usuario logueado"""
        return self.request.user.bookings.filter(
            is_recurring=True,
            recurrence_pattern__in=['WEEKLY', 'BIWEEKLY', 'MONTHLY'],
            parent_booking__isnull=True  # Solo la reserva padre, no las instancias
        ).distinct()


class DashboardAdminView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'general/dashboard_admin.html'

    def test_func(self):
        # Verifica si el usuario logueado tiene un perfil de administrador
        return hasattr(self.request.user, 'administrator_profile')

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para acceder al panel de administración.")
        return redirect('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['zones'] = Zone.objects.all()
        context['bookings'] = Booking.objects.all()
        return context