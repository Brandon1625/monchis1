from django.contrib import admin
from .models import *
from django.shortcuts import redirect


class TrabajadorAdmin(admin.ModelAdmin):
    actions = ['informe']
    readonly_fields = ['codigo']
    list_display = [
     'codigo', 'nombre', 'apellido', 'direccion', 'telefono',
     'fecha_nacimiento', 'activo'
     ]
    list_filter = ['direccion', 'apellido']
    search_fields = ['nombre', 'apellido']

    def informe(self, request, queryset):
        return redirect('/trabajadores')
    informe.short_description = 'Exportar en formato PDF'

admin.site.register(Trabajador, TrabajadorAdmin)
