from django.db import models
from producto.models import Producto
from cliente.models import Cliente
from comun.models import Tipopago
from trabajador.models import Trabajador
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, F
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from datetime import datetime


class Venta(models.Model):
    no_venta = models.IntegerField('No de venta', null=True, blank=True)
    comprador = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField('Fecha emision', default=datetime.now)
    pago = models.ForeignKey(
        Tipopago, on_delete=models.CASCADE, null=True, blank=True)
    vendedor = models.ForeignKey(
        Trabajador, on_delete=models.CASCADE, null=True, blank=True)
    total = models.FloatField('Total', default=0.00, null=True, blank=True)

    def __str__(self):
        return "%s" % (self.no_venta)

    def clean(self):
        if not self.id:
            venta = Venta.objects.all().order_by('no_venta').last()
            self.no_venta = 100 if not venta else venta.no_venta+1

    def ficha(self):
        return mark_safe(u'<a href="/ficha/?id=%s" target="_blank">Imprimir</a>' % self.id)
    ficha.short_description = 'Imprimir'

    class Meta:
        db_table = 'vale'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'


PORCENTAJE = (
    (1.00, '0%'),
    (0.95, '5%'),
    (0.90, '10%'),
    (0.85, '15%'),
    (0.80, '20%'),
    (0.75, '25%'),
    (0.70, '30%'),
    (0.65, '35%'),
    (0.60, '40%'),
    (0.55, '45%'),
    (0.50, '50%'),
)


class Detalle_Venta(models.Model):
    id_venta = models.ForeignKey(
        Venta, on_delete=models.CASCADE, null=True,
        blank=True, related_name='detalles')
    id_prod = models.ForeignKey(
        Producto, on_delete=models.CASCADE, null=True, related_name = 'Producto')
    canti = models.PositiveIntegerField('Cantidad')
    precio = models.DecimalField('Precio', decimal_places=2, max_digits=12, blank=True)
    descuento = models.FloatField('Descuento', choices=PORCENTAJE, default=1.00, null=True)
    subtotal = models.FloatField('Subtotal', null=True, blank=True, editable=False)

    def clean(self):
        from decimal import Decimal
        desc = Decimal(self.descuento)
        self.precio = self.id_prod.precio
        self.subtotal = self.canti * self.id_prod.precio * desc
        if self.id:
            actual = Detalle_Venta.objects.filter(id=self.id)[0]
            if self.canti <= self.id_prod.cantidad + actual.canti:
                self.id_prod.cantidad = self.id_prod.cantidad + actual.canti - self.canti
                self.id_prod.save()
            else:
                raise ValidationError('La cantidad es mayor a las existencias porque la existencia es {}'.format(self.id_prod.cantidad))
        elif self.canti <= self.id_prod.cantidad:
                self.id_prod.cantidad = self.id_prod.cantidad - self.canti
                self.id_prod.save()
        else:
            raise ValidationError('La cantidad es mayor a las existencias porque la existencia es {}'.format(self.id_prod.cantidad))

    def __str__(self):
        return "%s" % (self.id_venta)

    class Meta:
        db_table = 'detalle_venta'
        verbose_name = 'Detalle de venta'
        verbose_name_plural = 'Detalle de ventas'


@receiver(post_delete, sender=Detalle_Venta)
def trigger_borradodedetalle(sender, **kwargs):
    linea = kwargs.get('instance')
    venta = Venta.objects.get(id=linea.id_venta.id)
    producto = Producto.objects.get(id=linea.id_prod.id)
    venta.total = venta.detalles.aggregate(total=Sum(F('subtotal')))['total']
    producto.cantidad = producto.cantidad + linea.canti
    producto.save()
    venta.save()


# Trigger para guardar totales
@receiver(post_save, sender=Detalle_Venta)
def trigger_sumadeventa(sender, **kwargs):
    linea = kwargs.get('instance')
    venta = Venta.objects.get(id=linea.id_venta.id)
    venta.total = venta.detalles.aggregate(total=Sum(F('subtotal')))['total']
    venta.save()
