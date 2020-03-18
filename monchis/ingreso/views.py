from django.shortcuts import render
from easy_pdf.views import PDFTemplateView
from .models import Ingreso, Detalle_Ingreso


class IngresoPDFView(PDFTemplateView):
    template_name = "ingreso.html"

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get("id")
        miingreso = Ingreso.objects.get(id=ids)
        deta = Detalle_Ingreso.objects.all()
        return super(IngresoPDFView, self).get_context_data(
            pagesize="Letter",
            title="Ingreso",
            miingreso=miingreso,
            deta=deta,
            **kwargs
        )
