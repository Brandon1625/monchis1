from django.shortcuts import render
from easy_pdf.views import PDFTemplateView
from .models import Trabajador


class FichaPDFViewTrabajadores(PDFTemplateView):
    template_name = "trabajadores.html"

    def get_context_data(self, **kwargs):
        trab = Trabajador.objects.all()
        return super(FichaPDFViewTrabajadores, self).get_context_data(
            pagesize="Letter",
            title="Trabajadores",
            trab=trab,
            **kwargs
        )
