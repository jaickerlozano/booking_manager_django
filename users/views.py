from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Resident
from .forms import ResidentUpdateForm

# Create your views here.
class ResidentUpdateView(LoginRequiredMixin, UpdateView):
    model = Resident
    form_class = ResidentUpdateForm
    template_name = 'users/resident_update.html'
    success_url = reverse_lazy('profile')

    # Esto asegura que el usuario que actualiza es únicamente el que está logueado
    def get_object(self, queryset=None):
        return self.request.user.resident_profile