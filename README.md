# 🏢 Booking Manager (Gestor de Reservas)

Un sistema web desarrollado en Django diseñado para gestionar las reservas de espacios comunes (quinchos, salas de eventos, etc.) en edificios o condominios. 

> **Nota:** Este proyecto se encuentra actualmente en fase de desarrollo (WIP).

## ✨ Características Principales

* **Gestión de Usuarios y Roles:** Perfiles diferenciados para **Administradores** y **Residentes** (asociados a un número de departamento).
* **Espacios Comunes:** Administración completa (CRUD) de zonas comunes, definiendo detalles como su capacidad y disponibilidad.
* **Sistema de Reservas:** Los residentes pueden agendar espacios disponibles. El sistema valida automáticamente las fechas para evitar reservas en el pasado o solapamientos.
* **Búsqueda Dinámica:** Filtro de reservas en tiempo real mediante peticiones AJAX (búsqueda por departamento, residente o nombre del espacio).
* **Notificaciones por Email:** Envío automatizado de correos electrónicos informativos al confirmar, modificar o cancelar una reserva.
* **Dashboards Diferenciados:** Vistas dedicadas y protegidas para la administración general del recinto y para el perfil personal de cada residente.

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python, Django 5.2.x
* **Frontend:** HTML, CSS, JavaScript (Vanilla Fetch API para AJAX)
* **Base de Datos:** SQLite (por defecto para entorno de desarrollo)
* **Otros:** `python-dotenv` (para gestión segura de credenciales y variables de entorno)

## 🚀 Instalación y Configuración Local

Sigue estos pasos para desplegar el proyecto en tu entorno de desarrollo local:

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/booking_manager.git
   cd booking_manager
   ```

2. **Crear y activar un entorno virtual**
   ```bash
   python -m venv venv
   
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Variables de Entorno**
   Crea un archivo llamado `.env` en la raíz del proyecto (al mismo nivel que `manage.py`) y agrega las siguientes variables necesarias:
   ```env
   SECRET_KEY=tu_clave_secreta_django
   SECRET_EMAIL=tu_correo_smtp@gmail.com
   SECRET_KEY_EMAIL=tu_contraseña_de_aplicacion_gmail
   ```

5. **Aplicar migraciones de la base de datos**
   ```bash
   python manage.py migrate
   ```

6. **Ejecutar el servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```
   Finalmente, visita `http://127.0.0.1:8000` en tu navegador web.
