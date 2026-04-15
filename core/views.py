from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from .forms import ResidentRegistrationForm, LoginForm
from django.views.generic.edit import CreateView, FormView
from django.urls import reverse_lazy
from users.models import Resident
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView as DjangoLoginView
from zones.models import Zone, Booking
from django.db.models import Q

# Create your views here.
class HomeView(TemplateView):
    template_name = 'general/home.html'


class LoginView(DjangoLoginView):
    template_name = 'general/login.html'
    authentication_form = LoginForm
    # Este método solo sirve para la clase LogineView. Si quisieras hacer algo similar en una vista normal, tendrías que hacerlo en el método dispatch, como hiciste en el RegisterView.
    redirect_authenticated_user = True 

    def form_valid(self, form):
        # El mensaje solo se envía si el login fue exitoso en este momento
        messages.success(self.request, "¡Bienvenido de nuevo! Has iniciado sesión correctamente.")
        return super().form_valid(form)


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
        messages.success(self.request, "¡Registro exitoso! Ahora puedes iniciar sesión.")

        return super().form_valid(form)


class ContactView(TemplateView):
    template_name = 'general/contact.html'

    
class LegalView(TemplateView):
    template_name = 'general/legal.html'

@login_required
def logout_view(request):
    logout(request) # Ahora sí, esta es la función de Django que importaste arriba
    messages.info(request, 'Sesión cerrada correctamente.') # Corregí INFO por info
    return redirect('home')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'general/profile.html'
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

        return context

    # 4. Sobreescribimos dispatch para manejar la petición AJAX
    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = self.get_context_data()
            # Si es AJAX, solo renderizamos un mini-template con la lista
            return render(request, '_includes/_all_bookings_list.html', context)
        return super().get(request, *args, **kwargs)


class DashboardAdminView(TemplateView):
    template_name = 'general/dashboard_admin.html'