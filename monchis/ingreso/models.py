from django.db import models
from producto.models import Producto
from trabajador.models import Trabajador
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, F
from django.utils.safestring import mark_safe
from datetime import datetime


class Ingreso(models.Model):
    no_ingreso = models.IntegerField('No de ingreso', null=True, blank=True)
    fecha = models.DateField('Fecha emision', default=datetime.now)
    vendedor = models.ForeignKey(
        Trabajador, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "%s" % (self.no_ingreso)

    def clean(self):
        if not self.id:
            ingreso = Ingreso.objects.all().order_by('no_ingreso').last()
            self.no_ingreso = 100 if not ingreso else ingreso.no_ingreso+1

    def ficha(self):
        return mark_safe(u'<a href="/ingreso/?id=%s" target="_blank">Imprimir</a>' % self.id)
    ficha.short_description = 'Imprimir'

    class Meta:
        db_table = 'ingreso'
        verbose_name = 'Ingreso de mercaderia'
        verbose_name_plural = 'Ingresos de mercaderia'


class Detalle_Ingreso(models.Model):
    id_ingreso = models.ForeignKey(
        Ingreso, on_delete=models.CASCADE, null=True,
        blank=True, related_name='detalles')
    id_prod = models.ForeignKey(
        Producto, on_delete=models.CASCADE, null=True)
    canti = models.PositiveIntegerField('Cantidad')

    def __str__(self):
        return "%s" % (self.id_ingreso)

    class Meta:
        db_table = 'detalle_ingreso'
        verbose_name = 'Detalle de ingreso de mercaderia'
        verbose_name_plural = 'Detalle de ingresos de mercaderia'


@receiver(post_delete, sender=Detalle_Ingreso)
def trigger_borradodesproductos1(sender, **kwargs):
    linea = kwargs.get('instance')
    ingreso = Ingreso.objects.get(id=linea.id_ingreso.id)
    producto = Producto.objects.get(id=linea.id_prod.id)
    producto.cantidad = producto.cantidad - linea.canti
    producto.save()
    ingreso.save()


@receiver(post_save, sender=Detalle_Ingreso)
def trigger_aumetodelproducto1(sender, **kwargs):
    linea = kwargs.get('instance')
    producto = Producto.objects.get(id=linea.id_prod.id)
    producto.cantidad = producto.cantidad + linea.canti
    producto.save()
