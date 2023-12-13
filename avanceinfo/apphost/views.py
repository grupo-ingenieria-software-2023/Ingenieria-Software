from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.core.serializers import serialize
import json
from .models import *

# Create your views here.
def contacto(req):
    if req.method == "GET":
        return render(req, "contacto.html")
    elif req.method == "POST":
        nombre = req.POST.get("nombre", "[Nombre Desconocido]")
        email = req.POST.get("email")
        mensaje = f"""  Email de contacto recibido de {nombre}, de {req.POST.get("edad")} años.
                        Se puede contactar por...
                        Teléfono: {req.POST.get("fono")}
                        Email: {email}
                        
                        Su mensaje es:
                        {req.POST.get("mensaje")}
        """

        send_mail(
            f"Email Contacto de {nombre}",
            mensaje,
            "grpingsoft2023@gmail.com",
            ["grpingsoft2023@gmail.com"],
            fail_silently=False,
        )

        send_mail(
            "Mensaje Recibido",
            "Se ha recibido su mensaje con éxito y un representativo se contactará con usted pronto de ser necesario.",
            "grpingsoft2023@gmail.com",
            [email],
            fail_silently=False,
        )
        return render(req, "contacto.html")

def menu(req):
    omnivoras = Producto.objects.filter(tipo__exact="OMN", disponible=True)
    vegetarianas = Producto.objects.filter(tipo__exact="VGT", disponible=True)
    veganas = Producto.objects.filter(tipo__exact="VGN", disponible=True)
    acompanamientos = Producto.objects.filter(tipo__exact="ACO", disponible=True)
    datos = serialize("json", Producto.objects.filter(disponible=True))

    if req.method == "GET":
        return render(req, "menu.html", {
            'omnivoras': omnivoras,
            'vegetarianas': vegetarianas,
            'veganas': veganas,
            'acompanamientos': acompanamientos,
            'datos': datos
        })

    elif req.method == "POST":
        pedido = Pedido(direccion=req.POST.get("direccion"))
        pedido.save()
        for pk, cantidad in json.loads(req.POST.get("json_medianas")).items():
            pizza = Producto.objects.get(pk=pk)
            precio = pizza.precio_mediana * cantidad
            fragmento = FragmentoPedido(
                pedido = pedido,
                producto = pizza,
                cantidad = cantidad,
                precio_total = precio,
                tamano = "MD"
            )
            fragmento.save()
        for pk, cantidad in json.loads(req.POST.get("json_familiares")).items():
            pizza = Producto.objects.get(pk=pk)
            precio = pizza.precio_familiar * cantidad
            fragmento = FragmentoPedido(
                pedido = pedido,
                producto = pizza,
                cantidad = cantidad,
                precio_total = precio,
                tamano = "FM"
            )
            fragmento.save()
        for pk, cantidad in json.loads(req.POST.get("json_acompanamientos")).items():
            acompanamiento = Producto.objects.get(pk=pk)
            precio = acompanamiento.precio_unico * cantidad
            fragmento = FragmentoPedido(
                pedido = pedido,
                producto = acompanamiento,
                cantidad = cantidad,
                precio_total = precio,
                tamano = "AC"
            )
            fragmento.save()

        return redirect("/")

## Requieren login:
LOGUEADO = "logueado"
def login(req):
    if (req.method != "POST"):
        if (req.session.get(LOGUEADO)):
            req.session.pop(LOGUEADO)
        return render(req, "login.html", {'login_form': FormTrabajador()})
    else:
        try:
            trabajador = Trabajador.objects.get(rut=req.POST.get("rut"))
        except Trabajador.DoesNotExist:
            trabajador = None

        PERMITIR_ADMIN = False
        if ((PERMITIR_ADMIN and req.POST.get("password") == "admin") or (trabajador and trabajador.password == req.POST.get("password"))):
            req.session[LOGUEADO] = True
            return redirect("/")
        else:
            return render(req, "login.html", {'login_form': FormTrabajador()})

def requiere_login(vista):
    def wrapper(req, *args, **kwargs):
        print(req.session.get(LOGUEADO))
        if (req.session.get(LOGUEADO)):
            return vista(req, *args, **kwargs)
        else:
            return redirect("/login")
    return wrapper

@requiere_login
def agregar_producto(req):
    if req.method == "GET":
        return render(req, "agregar_producto.html", { 'form_producto': FormProducto() })
    elif req.method == "POST":
        nuevo_producto = FormProducto(req.POST)
        nuevo_producto.save()
        return redirect("/")

@requiere_login
def pedidos(req, modo=None, pk=None):
    if modo and pk:
        pedido = Pedido.objects.get(pk=pk)
        if pedido:
            if modo == "enviar" and pedido.estado == "PD":
                pedido.estado = "EN" 
            elif modo == "recibir" and pedido.estado == "EN":
                pedido.estado = "RC"
            elif modo == "cancelar" and pedido.estado != "RC":
                pedido.estado = "CN"
        pedido.save()
        return redirect("/pedidos")

    pendientes = Pedido.objects.filter(estado="PD")
    enviados = Pedido.objects.filter(estado="EN")
    items = FragmentoPedido.objects.filter(pedido__estado__in=["PD", "EN"]).order_by("tamano").order_by("pedido")

    return render(req, "pedidos.html", {
        'pendientes': pendientes,
        'enviados': enviados,
        'items': items
    })

URL_ADMINISTRAR = "/administrar"
@requiere_login
def administrar(req):
    return render(req, 'administracion.html', {
        'form_trabajador': FormTrabajador(),
        'trabajadores': Trabajador.objects.all(),
        'productos': Producto.objects.filter(disponible=True),
        'ventas': Pedido.objects.all()
    })

@requiere_login
def nuevo_trabajador(req):
    if (req.method == "POST"):
        trab_nuevo = FormTrabajador(req.POST)
        try:
            Trabajador.objects.get(rut=req.POST.get("rut"))
        except Trabajador.DoesNotExist:
            trab_nuevo.save()
    
    return redirect(URL_ADMINISTRAR)

@requiere_login
def eliminar_trabajador(req, rut):
    try:
        Trabajador.objects.get(rut=rut).delete()
    except:
        ...
    return redirect(URL_ADMINISTRAR)

@requiere_login
def eliminar_producto(req, pk):
    try:
        producto = Producto.objects.get(pk=pk)
    except:
        producto = None
    if producto:
        producto.disponible = False
        producto.save()
    return redirect(URL_ADMINISTRAR)