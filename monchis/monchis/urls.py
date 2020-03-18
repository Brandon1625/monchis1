"""monchis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.views.debug import default_urlconf
from django.urls import path, include
from django.conf.urls import url, re_path
from venta.views import FichaPDFView
from producto.views import FichaPDFViewProductos
from cliente.views import FichaPDFViewClientesT, FichaPDFViewClientesF, FichaPDFViewClientes
from trabajador.views import FichaPDFViewTrabajadores
from django.conf import settings
from django.conf.urls.static import static
from ingreso.views import IngresoPDFView
from venta.views import ventas


urlpatterns = [
    path('monchis/', admin.site.urls),
    path('', include('producto.urls')),
    path('', include('venta.urls')),
    url(r"^clientesactivos/", FichaPDFViewClientesT.as_view()),
    url(r"^clientes/", FichaPDFViewClientes.as_view()),
    url(r"^ficha/(?P<id>)", FichaPDFView.as_view()),
    url(r"^ingreso/(?P<id>)", IngresoPDFView.as_view()),
    url(r"^clientesinactivos/", FichaPDFViewClientesF.as_view()),
    url(r"^productos/", FichaPDFViewProductos.as_view()),
    url(r"^trabajadores/", FichaPDFViewTrabajadores.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
