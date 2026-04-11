"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import HomeView, LoginView, RegisterView, LegalView, ContactView, logout_view, ProfileView
<<<<<<< HEAD
from zones.views import ReservationCreateView
=======
from zones.views import BookingCreateView, BookingDetailView, BookingUpdateView, BookingDeleteView
>>>>>>> feature/crud-reservations

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('legal/', LegalView.as_view(), name='legal'),
<<<<<<< HEAD
    path('profile/', ProfileView.as_view(), name='profile'), # Por ahora el profile es lo mismo que el home, pero luego lo cambiaremos para que muestre información personalizada del usuario
    path('reservations/create/', ReservationCreateView.as_view(), name='reservation_create'),
=======
    path('profile/', ProfileView.as_view(), name='profile'), 
    path('reservations/create/', BookingCreateView.as_view(), name='reservation_create'),
    path('reservations/detail/<int:pk>', BookingDetailView.as_view(), name='reservation_detail'),
    path('reservations/update/<int:pk>', BookingUpdateView.as_view(), name='reservation_update'),
    path('reservations/delete/<int:pk>', BookingDeleteView.as_view(), name='reservation_delete'),
>>>>>>> feature/crud-reservations
]
