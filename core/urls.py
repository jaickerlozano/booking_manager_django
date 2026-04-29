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
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView, LoginView, RegisterView, LegalView, ContactView, logout_view, ProfileView, DashboardAdminView
from users.views import ResidentUpdateView
from zones.views import AdminBookingCreateView, BookingCreateView, BookingDetailView, BookingUpdateView, BookingDeleteView, ZoneCreateView, ZoneUpdateView, ZoneDeleteView, BookingListView, ZoneDetailView, ZoneAvailabilityView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardAdminView.as_view(), name='dashboard_admin'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('legal/', LegalView.as_view(), name='legal'),
    path('profile/', ProfileView.as_view(), name='profile'), 
    path('profile/update/<int:pk>/', ResidentUpdateView.as_view(), name='resident_update'),
    path('reservations/create/', BookingCreateView.as_view(), name='reservation_create'),
    path('reservations/admin-create/', AdminBookingCreateView.as_view(), name='admin_reservation_create'),
    path('reservations/detail/<int:pk>/', BookingDetailView.as_view(), name='reservation_detail'),
    path('reservations/list/', BookingListView.as_view(), name='reservation_list'),
    path('reservations/update/<int:pk>/', BookingUpdateView.as_view(), name='reservation_update'),
    path('reservations/delete/<int:pk>/', BookingDeleteView.as_view(), name='reservation_delete'),
    path('zones/create/', ZoneCreateView.as_view(), name='zone_create'),
    path('zones/detail/<int:pk>/', ZoneDetailView.as_view(), name='zone_detail'),
    path('zones/api/availability/<int:zone_id>/', ZoneAvailabilityView.as_view(), name='zone_availability_api'),
    path('zones/update/<int:pk>/', ZoneUpdateView.as_view(), name='zone_update'),
    path('zones/delete/<int:pk>/', ZoneDeleteView.as_view(), name='zone_delete'),
    path("__reload__/", include("django_browser_reload.urls")),
]

# Servir archivos media y estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # En producción, WhiteNoise se encarga de servir los archivos estáticos y media
    # desde STATIC_ROOT y MEDIA_ROOT respectivamente
    pass