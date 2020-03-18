from django.shortcuts import render
from easy_pdf.views import PDFTemplateView
from .models import Venta, Detalle_Venta
from django.db.models import Count, Q, Sum
from datetime import datetime, timedelta


class FichaPDFView(PDFTemplateView):
    template_name = "ficha.html"

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get("id")
        miventa = Venta.objects.get(id=ids)
        deta = Detalle_Venta.objects.all()
        return super(FichaPDFView, self).get_context_data(
            pagesize="Letter",
            title="Ficha",
            miventa=miventa,
            deta=deta,
            **kwargs
        )


def ventas(request):
    last_month = datetime.now() - timedelta(days=30)
    dataset = (Venta.objects
        .filter(fecha__gt= last_month)
        .extra(select={'day': 'date(fecha)'})
        .values('day')
        .annotate(sum=Sum('total')))
    print (dataset)
    return render(request, 'ventas.html', {'dataset': dataset})
