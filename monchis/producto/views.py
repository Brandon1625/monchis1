from django.shortcuts import render
from django.http import HttpResponse
from easy_pdf.views import PDFTemplateView
from .models import Producto
from django.views.generic import ListView
from django.db.models import Count, Q


class FichaPDFViewProductos(PDFTemplateView):
    template_name = "productos.html"

    def get_context_data(self, **kwargs):
        prod = Producto.objects.all()
        return super(FichaPDFViewProductos, self).get_context_data(
            pagesize="Legal Landscape",
            title="Productos",
            prod=prod,
            **kwargs
        )


def ProductoLista(request):
    prod = Producto.objects.all().order_by('ref')
    contexto = {'productos': prod}
    return render(request, 'productos_lista.html', contexto)


def contact(request):
    return render(request, 'contacto.html', {})


def productosgrafica(request):
    dataset = Producto.objects \
        .all() \
        .filter(activo=True) \
        .order_by('-cantidad')
    return render(request, 'ticket_class.html', {'dataset': dataset})
