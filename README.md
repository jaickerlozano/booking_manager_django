# 🏢 Booking Manager - Gestor de Reservas de Espacios Comunes

[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776ab?style=flat&logo=python)](https://www.python.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.x-38B2AC?style=flat&logo=tailwindcss)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Sistema web completo para la gestión integral de reservas de espacios comunes (quinchos, salas de eventos, piscinas, gyms, etc.) en edificios, condominios y complejos residenciales. Permite a administradores y residentes gestionar de manera eficiente la disponibilidad y ocupación de infraestructuras compartidas.

## ✨ Características Principales

### 👥 Gestión de Usuarios y Autenticación
- **Sistema de Roles:** Diferenciación entre Administradores y Residentes
- **Perfiles de Residente:** Asociación automática a números de departamento
- **Autenticación Segura:** Contraseñas hasheadas con Django's built-in security
- **Edición de Perfil:** Los residentes pueden actualizar su información personal
- **Foto de Perfil:** Carga de imágenes de perfil almacenadas en Cloudinary

### 🏛️ Administración de Espacios Comunes (Zonas)
- **CRUD Completo:** Crear, leer, actualizar y eliminar espacios comunes
- **Gestión de Detalles:** Nombre, descripción, capacidad máxima, disponibilidad
- **Imágenes Descriptivas:** Carga de fotos de espacios almacenadas en Cloudinary
- **Estado de Disponibilidad:** Habilitar/deshabilitar espacios rápidamente
- **Panel de Administración:** Vista dedicada para gestionar todas las zonas

### 📅 Sistema Avanzado de Reservas
- **Reserva por Residentes:** Interfaz amigable para agendar espacios disponibles
- **Validaciones Inteligentes:**
  - Prevención de reservas en fechas pasadas
  - Evitación automática de solapamientos
  - Validación de capacidad
- **Gestión de Reservas:** Crear, visualizar, editar y cancelar reservas
- **Historial Completo:** Registro de todas las reservas realizadas
- **Detalles de Reserva:** Información completa del espacio, fecha, hora y usuario

### 🔍 Búsqueda Dinámica en Tiempo Real
- **Filtros por AJAX:** Sin necesidad de recargar la página
- **Búsqueda Multi-campo:** Por departamento, nombre de residente o espacio común
- **Interfaz Responsive:** Funciona perfectamente en dispositivos móviles

### 📧 Notificaciones por Email
- **Confirmación de Reserva:** Email al crear una nueva reserva
- **Notificación de Actualización:** Cuando se modifica una reserva existente
- **Confirmación de Cancelación:** Cuando se cancela una reserva
- **Contacto:** Formulario de contacto para comunicarse con administración
- **Envío No Bloqueante:** Los errores de email no rompen la aplicación (fail_silently=True)

### 📊 Dashboards Diferenciados
- **Dashboard de Admin:**
  - Estadísticas generales de reservas
  - Gestión completa de espacios comunes
  - Creación manual de reservas para residentes
  - Visualización de todas las reservas del condominio
- **Perfil de Residente:**
  - Mis reservas activas y pasadas
  - Edición de información personal
  - Acceso a espacios comunes disponibles

### 🎨 Diseño Moderno y Responsive
- **Tailwind CSS 3.x:** Estilos modernos y optimizados
- **Totalmente Responsive:** Funciona en desktop, tablet y móvil
- **Interfaz Intuitiva:** Navegación clara y fácil de usar
- **Iconografía Profesional:** SVG icons integrados

### 📸 Almacenamiento de Archivos
- **Cloudinary Integration:** Almacenamiento seguro y confiable de imágenes
- **Caché y CDN:** Optimización automática de imágenes
- **Gestión Persistente:** Las imágenes persisten en producción (Render)

### 🔐 Seguridad
- **CSRF Protection:** Protección contra ataques CSRF
- **SQL Injection Prevention:** Queries parametrizadas
- **XSS Protection:** Escaping automático en templates
- **Debug Mode:** Deshabilitado en producción

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.12** - Lenguaje de programación
- **Django 5.2.3** - Framework web backend
- **dj-database-url** - Configuración de BD desde variables de entorno
- **python-dotenv** - Gestión segura de credenciales

### Frontend
- **HTML5** - Estructura semántica
- **Tailwind CSS 3.x** - Framework CSS utility-first
- **JavaScript (Vanilla)** - AJAX y interactividad
- **Fetch API** - Peticiones asincrónicas

### Base de Datos
- **SQLite** - Desarrollo local
- **PostgreSQL** - Producción (Render + Neon)

### Almacenamiento
- **Cloudinary** - CDN y almacenamiento de imágenes
- **django-cloudinary-storage** - Integración con Django

### Deployment
- **Render** - Hosting en la nube
- **Gunicorn** - WSGI HTTP Server
- **WhiteNoise** - Servir archivos estáticos

### Otros
- **Pillow** - Procesamiento de imágenes
- **psycopg2-binary** - Adaptador PostgreSQL
- **django-browser-reload** - Hot reload en desarrollo

## 📁 Estructura del Proyecto

```
booking_manager/
├── core/                    # App principal de configuración
│   ├── settings.py         # Configuración de Django
│   ├── urls.py             # Rutas principales
│   ├── views.py            # Vistas generales (home, login, etc.)
│   ├── forms.py            # Formularios
│   ├── templates/          # Templates HTML
│   │   ├── general/        # Templates generales
│   │   ├── reservations/   # Templates de reservas
│   │   ├── zones/          # Templates de zonas
│   │   └── users/          # Templates de usuarios
│   └── media/              # Carpeta de archivos media locales
│
├── users/                   # Gestión de usuarios
│   ├── models.py           # Modelos (Resident, Administrator)
│   ├── views.py            # Vistas de usuarios
│   ├── forms.py            # Formularios de usuario
│   ├── admin.py            # Admin customizado
│   ├── migrations/         # Migraciones de BD
│   └── templates/          # Templates específicos
│
├── zones/                   # Gestión de espacios comunes
│   ├── models.py           # Modelos (Zone, Booking)
│   ├── views.py            # Vistas CRUD y lógica de reservas
│   ├── forms.py            # Formularios de zonas y reservas
│   ├── admin.py            # Admin customizado
│   ├── migrations/         # Migraciones de BD
│   └── templates/          # Templates específicos
│
├── theme/                   # Configuración de estilos
│   ├── static/             # CSS y assets
│   ├── static_src/         # Fuentes de CSS (Tailwind)
│   └── templates/          # Template base (layout.html)
│
├── env/                     # Entorno virtual (NO comitear)
├── media/                   # Archivos subidos por usuarios
├── staticfiles/             # Archivos estáticos colectados
├── .env                     # Variables de entorno (NO comitear)
├── manage.py                # Comando de management de Django
├── db.sqlite3               # BD SQLite local
├── requirements.txt         # Dependencias Python
├── build.sh                 # Script de build para Render
├── render.yaml              # Configuración de Render
└── README.md                # Este archivo
```

## 🤖 Demostración de Funcionalidad

- Live: https://booking-manager-django.onrender.com/
- Usuario como administrador de edificios: admin_edificio
- Password como administrador de edificios: Prueba123456
- Para probar el perfil como residente puedes crear una cuenta en el live...

## 🚀 Instalación y Configuración Local

### Requisitos Previos
- Python 3.12 o superior
- Git
- pip (viene con Python)
- Cuenta en Cloudinary (gratis) - opcional para desarrollo

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/jaickerlozano/booking_manager_django.git
   cd booking_manager
   ```

2. **Crear y activar entorno virtual**
   ```bash
   # En Windows
   python -m venv env
   env\Scripts\activate
   
   # En macOS/Linux
   python3 -m venv env
   source env/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Variables de Entorno**
   
   Crea un archivo `.env` en la raíz del proyecto:
   ```env
   # Django
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   
   # Email SMTP (Gmail)
   SECRET_EMAIL=your-email@gmail.com
   SECRET_KEY_EMAIL=your-app-password
   
   # Database (opcional, usa SQLite por defecto)
   DATABASE_URL=sqlite:///db.sqlite3
   
   # Cloudinary (opcional para desarrollo)
   CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
   ```

   **Nota:** Para obtener la contraseña de Gmail:
   - Ve a tu cuenta de Google
   - Activa la Verificación en 2 pasos
   - Ve a [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - Genera una contraseña de aplicación

5. **Ejecutar migraciones**
   ```bash
   python manage.py migrate
   ```

6. **Crear superusuario (Admin)**
   ```bash
   python manage.py createsuperuser
   ```
   Introduce:
   - Username: `admin`
   - Email: tu-email@example.com
   - Password: tu-contraseña

7. **Construir estilos Tailwind**
   ```bash
   python manage.py tailwind install
   python manage.py tailwind build
   ```

8. **Ejecutar servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```
   
   Accede a `http://127.0.0.1:8000`

## 📖 Guía de Uso

### Para Administradores
1. Accede a `/admin/` con tus credenciales de superusuario
2. **Crear Espacios Comunes:**
   - Ve al Dashboard (`/dashboard/`)
   - Crea nuevas zonas con nombre, descripción, capacidad e imagen
3. **Gestionar Residentes:**
   - En el admin, crea nuevos usuarios residentes
   - Asigna números de departamento
4. **Ver Reservas:**
   - En el Dashboard, visualiza todas las reservas del condominio
   - Puedes crear reservas manualmente para residentes
5. **Crear Espacios:**
   - Usa el botón "Crear Espacio Común"

### Para Residentes
1. **Registrarse:**
   - Haz click en "Registrarse"
   - Completa el formulario con tu información y número de departamento
2. **Acceder a Perfil:**
   - Click en tu nombre en la esquina superior derecha
   - Edita tu información y foto de perfil
3. **Crear Reservas:**
   - Ve a "Crear Reserva" (`/reservations/create/`)
   - Selecciona espacio, fecha y hora
   - Confirma la reserva
4. **Gestionar Reservas:**
   - Ve a "Mis Reservas" (`/reservations/list/`)
   - Edita o cancela reservas existentes

## 🌐 Despliegue en Producción (Render)

### Configuración en Render

1. **Conectar GitHub**
   - Crea una cuenta en [render.com](https://render.com)
   - Conecta tu repositorio de GitHub

2. **Variables de Entorno**
   
   En el Dashboard de Render, agrega:
   ```
   SECRET_KEY=your-production-secret-key
   DEBUG=False
   SECRET_EMAIL=your-email@gmail.com
   SECRET_KEY_EMAIL=your-app-password
   DATABASE_URL=your-postgresql-url
   CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
   ```

3. **Base de Datos**
   
   Usa [Neon PostgreSQL](https://neon.tech/) (gratis con Render):
   - Crea una base de datos PostgreSQL en Neon
   - Copia la URL `DATABASE_URL`
   - Agrégala a las variables de entorno en Render

4. **Cloudinary para Imágenes**
   
   - Crea cuenta gratis en [cloudinary.com](https://cloudinary.com)
   - Obtén tu `CLOUDINARY_URL`
   - Agrégalo a las variables de entorno

5. **Deploy Automático**
   
   - Cada push a `main` dispara un deploy automático
   - Los logs están disponibles en el Dashboard de Render

## 🔧 Configuración Adicional

### Configurar Tailwind CSS en Desarrollo

```bash
# Instalar dependencias de Node.js
python manage.py tailwind install

# Compilar CSS (una sola vez)
python manage.py tailwind build

# O modo watch (recompila automáticamente)
python manage.py tailwind start
```

### Crear Datos de Prueba

```bash
python manage.py shell

# Dentro del shell de Django
from users.models import Resident
from zones.models import Zone
from django.contrib.auth.models import User

# Crear usuario
user = User.objects.create_user(username='resident1', password='pass123')

# Crear residente
resident = Resident.objects.create(user=user, apartment_number='101')

# Crear zona
zone = Zone.objects.create(
    name='Quincho',
    description='Quincho con parrilla',
    capacity=20,
    is_available=True
)
```

## 🐛 Solución de Problemas

### Las imágenes no se ven en producción
- Verifica que `CLOUDINARY_URL` está configurado en Render
- Asegúrate de que el formato es: `cloudinary://api_key:api_secret@cloud_name`
- Haz un redeploy manual en Render

### Error 500 al crear reservas
- Verifica que `SECRET_EMAIL` y `SECRET_KEY_EMAIL` están correctos
- Intenta con una contraseña de aplicación de Gmail
- Revisa los logs en Render

### Estilos no se ven
- Ejecuta `python manage.py collectstatic --noinput`
- Verifica que `DEBUG=False` en producción

## 📝 Licencia

Este proyecto está bajo la licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

Desarrollado por [Jaicker Lozano](https://github.com/jaickerlozano)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Haz un fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Contacto y Soporte

Para reportar bugs o sugerencias, abre un issue en el repositorio o contacta a través del formulario de contacto en la aplicación.
