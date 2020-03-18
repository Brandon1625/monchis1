from django.db import models
from comun.models import Persona
from django.utils.safestring import mark_safe


class Trabajador(Persona):
    codigo = models.IntegerField('Codigo')
    fecha_nacimiento = models.DateField('Fecha de nacimiento')
    activo = models.BooleanField(default=True, verbose_name='activo')

    def clean(self):
        if not self.id:
            trab = Trabajador.objects.all().order_by('nombre').last()
            self.codigo = 100 if not trab else trab.codigo + 1

    def __str__(self):
        return "%s" % (self.nombre)

    def ficha(self):
        return mark_safe(
            u'<a href="trabajadores"target="_blank">Imprimir</a>')
    ficha.short_description = 'Imprimir todos'

    class Meta:
        db_table = 'trabajador'
        verbose_name = 'Trabajador'
        verbose_name_plural = 'Trabajadores'
