from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('perfil/', views.perfil, name='perfil'),
    path('eventos/', views.eventos, name='eventos'),
    path('contacto/', views.contacto, name='contacto'),
    path('logout/', views.logout_view, name='logout'),
    path('reservas/', views.reservas, name='reservas'),
    path('reservar/', views.reservar, name='reservar'),
    path('manual_usuario/', views.manual_usuario, name='manual_usuario'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('send_reclaim_email/', views.send_reclaim_email, name='send_reclaim_email'),
    path('send_domicilio_email/', views.send_domicilio_email, name='send_domicilio_email'),
    path('redirect_to_whatsapp/', views.redirect_to_whatsapp, name='redirect_to_whatsapp'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
