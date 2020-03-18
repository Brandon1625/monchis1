from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from comun.models import Referencia
from django.utils.html import escape


class Categoriaproducto(models.Model):
    categoria = models.CharField('nombre', max_length=50)

    def __str__(self):
        return "%s" % (self.categoria)

    class Meta:
        db_table = 'categoriaproducto'
        verbose_name = 'Categoria de producto'
        verbose_name_plural = 'Categorias de productos'


class Producto(models.Model):
    nombre = models.CharField('nombre', max_length=50)
    categoria = models.ForeignKey(
        Categoriaproducto, on_delete=models.CASCADE, null=True, blank=True)
    descripcion = models.CharField('descripcion', max_length=50)
    ref = models.ForeignKey(
        Referencia, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.PositiveIntegerField('cantidad', default=0)
    precio = models.DecimalField('Precio', decimal_places=2, max_digits=12)
    activo = models.BooleanField(default=True, verbose_name='activo')
    visible = models.BooleanField(default=True, verbose_name='visible')
    precio_visible = models.BooleanField(default=True, verbose_name='precio visible')
    cantidad_visible = models.BooleanField(default=True, verbose_name='cantidad visible')
    descripcion_visible = models.BooleanField(default=True, verbose_name='descripcion visible')
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.nombre

    def image_tag(self):
        if not self.image:
            return mark_safe('<img src="/media/sin-imagen.png" width="100" height="100" />')
        else:
            return mark_safe('<img src="/media/%s" width="100" height="100" />' % (self.image))

    image_tag.short_description = 'Image'

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


class AumentoProducto(models.Model):
    miprod = models.ForeignKey(
        Producto, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField('Fecha', null=True, blank=True)
    unidades = models.PositiveIntegerField('Unidades', default=1)

    def __str__(self):
        return "%s" % (self.miprod.nombre)

    class Meta:
        db_table = 'aumentoproducto'
        verbose_name = 'Aumento de Producto'
        verbose_name_plural = 'Aumento de Productos'


@receiver(post_save, sender=AumentoProducto)
def trigger_aumetodelproducto(sender, **kwargs):
    linea = kwargs.get('instance')
    producto = Producto.objects.get(id=linea.miprod.id)
    producto.cantidad = producto.cantidad + linea.unidades
    producto.save()


@receiver(post_delete, sender=AumentoProducto)
def trigger_borradodesproductos(sender, **kwargs):
    linea = kwargs.get('instance')
    producto = Producto.objects.get(id=linea.miprod.id)
    producto.cantidad = producto.cantidad - linea.unidades
    producto.save()
