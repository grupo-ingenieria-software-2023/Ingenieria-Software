from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.core.serializers import serialize
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
        return render(req, "menu.html")

def agregar_producto(req):
    if req.method == "GET":
        return render(req, "agregar_producto.html", { 'form_producto': FormProducto() })
    elif req.method == "POST":
        nuevo_producto = FormProducto(req.POST)
        nuevo_producto.save()
        return redirect("/")