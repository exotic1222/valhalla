from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Reservation, MenuItem, Cart, CartItem, PurchaseHistory, Event
from .forms import ReservationForm
import json
from decimal import Decimal

User = get_user_model()

def index(request):
    return render(request, 'index.html')

def menu(request):
    menu_items = MenuItem.objects.all()
    cart = None
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    return render(request, 'menu.html', {'menu_items': menu_items, 'cart': cart})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya está en uso.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'El correo electrónico ya está en uso.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, 'Tu cuenta ha sido creada exitosamente.')
                return redirect('login')
        else:
            messages.error(request, 'Las contraseñas no coinciden.')

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if not username or not password:
            messages.error(request, 'Por favor, ingresa ambos campos.')
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('perfil')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    
    return render(request, 'login.html')

@login_required
def perfil_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        messages.success(request, "¡Perfil actualizado exitosamente!")
        return redirect('perfil')
    
    return render(request, 'perfil.html', {'user': request.user})

def eventos(request):
    events = Event.objects.all()
    return render(request, 'eventos.html', {'events': events})

def contacto(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        mensaje = request.POST['mensaje']

        send_mail(
            f'Mensaje de {nombre} desde el formulario de contacto',
            mensaje,
            email,
            ['dadslinger1222@gmail.com'],
            fail_silently=False,
        )

        messages.success(request, 'Tu mensaje ha sido enviado exitosamente.')
        return redirect('contacto')

    return render(request, 'contacto.html')

def logout_view(request):
    auth_logout(request)
    messages.success(request, "Gracias por visitarnos. ¡Vuelve pronto!")
    return render(request, 'logout.html')

def reservas(request):
    return render(request, 'reservas.html')

@login_required
def reservar(request):
    if request.method == 'POST':
        event_date = request.POST.get('event_date')
        event_time = request.POST.get('event_time')
        reservation_type = request.POST.get('reservation_type')
        mesa_number = request.POST.get('mesa_number')
        num_people = request.POST.get('num_people')
        price = request.POST.get('price')

        if not all([event_date, event_time, reservation_type, num_people, price]):
            messages.error(request, 'Por favor, completa todos los campos.')
            return redirect('reservas')

        reservation = Reservation.objects.create(
            user=request.user,
            event_date=event_date,
            event_time=event_time,
            reservation_type=reservation_type,
            mesa_number=mesa_number if reservation_type == 'mesa' else None,
            num_people=num_people,
            price=price
        )

        subject_user = 'Confirmación de Reserva - Valhalla Bar'
        html_message_user = render_to_string('email_user.html', {
            'event_date': event_date,
            'event_time': event_time,
            'reservation_type': reservation_type,
            'mesa_number': mesa_number if reservation_type == 'mesa' else None,
            'num_people': num_people,
            'price': price,
        })
        plain_message_user = strip_tags(html_message_user)
        from_email = settings.EMAIL_HOST_USER
        to_user = request.user.email

        send_mail(subject_user, plain_message_user, from_email, [to_user], html_message=html_message_user)

        subject_admin = 'Nueva Reserva - Valhalla Bar'
        html_message_admin = render_to_string('email_admin.html', {
            'user': request.user,
            'event_date': event_date,
            'event_time': event_time,
            'reservation_type': reservation_type,
            'mesa_number': mesa_number if reservation_type == 'mesa' else None,
            'num_people': num_people,
            'price': price,
        })
        plain_message_admin = strip_tags(html_message_admin)
        to_admin = 'dadslinger1222@gmail.com'

        send_mail(subject_admin, plain_message_admin, from_email, [to_admin], html_message=html_message_admin)

        return render(request, 'confirmacion_reserva.html', {
            'event_date': event_date,
            'event_time': event_time,
            'reservation_type': reservation_type,
            'mesa_number': mesa_number if reservation_type == 'mesa' else None,
            'num_people': num_people,
            'price': price,
        })

    return redirect('reservas')

def manual_usuario(request):
    return render(request, 'manual_usuario.html')

@login_required
def add_to_cart(request, item_id):
    if request.method == 'POST' and request.user.is_authenticated:
        menu_item = get_object_or_404(MenuItem, id=item_id)
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        cart.items.add(menu_item)
        # Obtener el ID del ítem recién agregado (el último en la relación muchos-a-muchos)
        cart_item_id = CartItem.objects.filter(cart=cart, menu_item=menu_item).latest('id').id
        return JsonResponse({'status': 'success', 'cart_item_id': cart_item_id})
    elif request.method == 'GET':
        # Mantener compatibilidad con redirección si se accede directamente
        if request.user.is_authenticated:
            menu_item = get_object_or_404(MenuItem, id=item_id)
            cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
            cart.items.add(menu_item)
        return redirect('menu')
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST' and request.user.is_authenticated:
        menu_item = get_object_or_404(MenuItem, id=item_id)
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart.items.remove(menu_item)
        return JsonResponse({'status': 'success'})
    elif request.method == 'GET':
        # Mantener compatibilidad con redirección si se accede directamente
        if request.user.is_authenticated:
            menu_item = get_object_or_404(MenuItem, id=item_id)
            cart = Cart.objects.get(user=request.user, is_active=True)
            cart.items.remove(menu_item)
        return redirect('menu')
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def send_reclaim_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        secret_key = data['secret_key']
        total_price = data['total_price']
        product_names = data['product_names']

        user_email = request.user.email
        user_subject = "Detalles de tu pedido en Valhalla Bar"
        user_message = render_to_string('emails/user_reclaim_email.html', {
            'user': request.user,
            'secret_key': secret_key,
            'total_price': total_price,
            'product_names': product_names
        })
        user_email_message = EmailMultiAlternatives(
            subject=user_subject,
            body=user_message,
            from_email='info@valhallabar.com',
            to=[user_email]
        )
        user_email_message.attach_alternative(user_message, "text/html")
        user_email_message.send()

        admin_email = 'dadslinger1222@gmail.com'
        admin_subject = "Nuevo pedido para reclamar en el bar"
        admin_message = render_to_string('emails/admin_reclaim_email.html', {
            'user': request.user,
            'secret_key': secret_key,
            'total_price': total_price,
            'product_names': product_names
        })
        admin_email_message = EmailMultiAlternatives(
            subject=admin_subject,
            body=admin_message,
            from_email='info@valhallabar.com',
            to=[admin_email]
        )
        admin_email_message.attach_alternative(admin_message, "text/html")
        admin_email_message.send()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)

@login_required
def send_domicilio_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        secret_key = data['secret_key']
        total_price = data['total_price']
        product_names = data['product_names']
        nombre = data['nombre']
        direccion = data['direccion']
        telefono = data['telefono']

        user_email = request.user.email
        user_subject = "Detalles de tu pedido a domicilio en Valhalla Bar"
        user_message = render_to_string('emails/user_domicilio_email.html', {
            'user': request.user,
            'secret_key': secret_key,
            'total_price': total_price,
            'product_names': product_names,
            'nombre': nombre,
            'direccion': direccion,
            'telefono': telefono
        })
        user_email_message = EmailMultiAlternatives(
            subject=user_subject,
            body=user_message,
            from_email='info@valhallabar.com',
            to=[user_email]
        )
        user_email_message.attach_alternative(user_message, "text/html")
        user_email_message.send()

        admin_email = 'dadslinger1222@gmail.com'
        admin_subject = "Nuevo pedido a domicilio"
        admin_message = render_to_string('emails/admin_domicilio_email.html', {
            'user': request.user,
            'secret_key': secret_key,
            'total_price': total_price,
            'product_names': product_names,
            'nombre': nombre,
            'direccion': direccion,
            'telefono': telefono
        })
        admin_email_message = EmailMultiAlternatives(
            subject=admin_subject,
            body=admin_message,
            from_email='info@valhallabar.com',
            to=[admin_email]
        )
        admin_email_message.attach_alternative(admin_message, "text/html")
        admin_email_message.send()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)

@login_required
def redirect_to_whatsapp(request):
    if request.method == 'POST':
        user = request.user
        total_price = request.POST.get('total_price')
        product_names = request.POST.get('product_names')

        try:
            total_price = Decimal(total_price)
        except (ValueError, TypeError):
            return redirect('menu')

        product_names_list = product_names.split(', ')

        for product_name in product_names_list:
            PurchaseHistory.objects.create(
                user=user,
                product_name=product_name,
                total_price=total_price
            )

        phone_number = "573144662953"
        message = f"Hola, este es el comprobante de mi pago por los productos: {product_names}. El total a pagar es {total_price}."
        url = f"https://wa.me/{phone_number}?text={message}"
        return redirect(url)

    return redirect('menu')

@login_required
def perfil(request):
    purchase_history = PurchaseHistory.objects.filter(user=request.user).order_by('-date')
    return render(request, 'perfil.html', {'purchase_history': purchase_history})

@login_required
def clear_cart(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart.items.clear()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)