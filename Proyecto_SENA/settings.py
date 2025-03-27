from pathlib import Path
import os

# BASE_DIR - Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY - Hardcodeado solo para desarrollo
SECRET_KEY = '5(mi%ydcd!gpvxy%q*keqri68fvl+@9l@o=p$37temsqa%q69@'

# Activar modo debug (No usar en producción)
DEBUG = True

ALLOWED_HOSTS = []

# Redirecciones de login/logout
LOGIN_REDIRECT_URL = 'menu'  
LOGOUT_REDIRECT_URL = '/'

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vahalla',  # Asegúrate de que tu app esté aquí
]

AUTH_USER_MODEL = 'vahalla.CustomUser'

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Proyecto_SENA.urls'

# Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Proyecto_SENA.wsgi.application'

# Base de datos SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}

# Validación de contraseñas (puedes quitar esto si no lo necesitas)
AUTH_PASSWORD_VALIDATORS = []

# Configuración de idioma y zona horaria
LANGUAGE_CODE = 'es-co'  
TIME_ZONE = 'America/Bogota'  
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'vahalla', 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Tipo de clave primaria por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de correos (Solo si lo necesitas)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'prime2025exotic@gmail.com'
EMAIL_HOST_PASSWORD = 'lanu xqnc lece rksx'
