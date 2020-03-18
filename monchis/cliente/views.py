from django.shortcuts import render
from easy_pdf.views import PDFTemplateView
from .models import Cliente


class FichaPDFViewClientesF(PDFTemplateView):
    template_name = "clientesinactivos.html"

    def get_context_data(self, **kwargs):
        clien = Cliente.objects.all()
        return super(FichaPDFViewClientesT, self).get_context_data(
            pagesize="Letter",
            title="Clientes",
            clien=clien,
            **kwargs
        )


class FichaPDFViewClientes(PDFTemplateView):
    template_name = "clientes.html"

    def get_context_data(self, **kwargs):
        clien = Cliente.objects.all().order_by('-activo')
        return super(FichaPDFViewClientes, self).get_context_data(
            pagesize="Legal Landscape",
            title="Clientes",
            clien=clien,
            **kwargs
        )


class FichaPDFViewClientesT(PDFTemplateView):
    template_name = "clientesactivos.html"

    def get_context_data(self, **kwargs):
        clien = Cliente.objects.all()
        return super(FichaPDFViewClientesT, self).get_context_data(
            pagesize="Letter",
            title="Clientes",
            clien=clien,
            **kwargs
        )


def home_view(request, *args, **kwargs): # *args, **kwargs
    print(args, kwargs)
    print(request.user)
    #return HttpResponse("<h1>Hello World</h1>") # string of HTML code
    return render(request, "home.html", {})
