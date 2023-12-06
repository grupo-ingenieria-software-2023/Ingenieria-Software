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

def agregar_producto(req):
    if req.method == "GET":
        return render(req, "agregar_producto.html", { 'form_producto': FormProducto() })
    elif req.method == "POST":
        nuevo_producto = FormProducto(req.POST)
        nuevo_producto.save()
        return redirect("/")

def lista_productos(req):
    ...

def pedidos(req):
    modo = req.GET.get("modo")
    pk = req.GET.get("pk")
    if modo and pk:
        pedido = Pedido.objects.get(pk=pk)
        if pedido:
            if modo == "enviar":
                pedido.estado = "EN" 
            elif modo == "recibir":
                pedido.estado = "RC" 
            elif modo == "cancelar":
                pedido.estado = "CN"
        pedido.save()

    pendientes = Pedido.objects.filter(estado="PD")
    enviados = Pedido.objects.filter(estado="EN")
    items = FragmentoPedido.objects.filter(pedido__estado__in=["PD", "EN"]).order_by("tamano").order_by("pedido")

    return render(req, "pedidos.html", {
        'pendientes': pendientes,
        'enviados': enviados,
        'items': items
    })  