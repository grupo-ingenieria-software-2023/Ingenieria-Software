"""
URL configuration for avanceinfo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import apphost.views as apphost
from django.shortcuts import render

urlpatterns = [
    path('', lambda req: render(req, "index.html")),
    path('index', lambda req: render(req, "index.html")),
    path('menu', apphost.menu),
    path('contacto', apphost.contacto),
    path('nosotros', lambda req: render(req, "nosotros.html")),
    path('agregar_producto', apphost.agregar_producto),
    path('pedidos', apphost.pedidos),
    path('admin/', admin.site.urls),
]
