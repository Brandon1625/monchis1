from django.db import models
from comun.models import Persona


class Cliente(Persona):
    nit = models.CharField('Nit', max_length=10, primary_key=True)
    email = models.EmailField('E-mail', max_length=50, null=True)
    activo = models.BooleanField(default=True, verbose_name='activo')

    def __str__(self):
        return "%s %s" % (self.nombre, self.apellido)

    class Meta:
        db_table = 'cliente'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
