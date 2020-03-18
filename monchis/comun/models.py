from django.db import models


class Persona(models.Model):
    nombre = models.CharField('Nombres', max_length=50)
    apellido = models.CharField('Apellidos', max_length=50)
    direccion = models.CharField('Direccion', max_length=50)
    telefono = models.PositiveIntegerField('Telefono')

    def __str__(self):
        return "%s %s" % (self.nombre, self.apellido)

    class Meta():
        abstract = True


class Tipopago(models.Model):
    tipo = models.CharField('Tipo de pago', max_length=50)

    def __str__(self):
        return "%s" % (self.tipo)

    class Meta:
        db_table = 'tipopago'
        verbose_name = 'Tipo de pago'
        verbose_name_plural = 'Tipos de pago'


class Referencia(models.Model):
    referencia = models.CharField('Referencia', max_length=50)

    def __str__(self):
        return "%s" % (self.referencia)

    class Meta:
        db_table = 'referencia'
        verbose_name = 'Referencia'
        verbose_name_plural = 'Referencias'
