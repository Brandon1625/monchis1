from django.contrib import admin
from .models import *
from import_export import resources
from import_export import fields
from import_export.admin import ExportMixin


class ModeloResource(resources.ModelResource):
    class Meta:
        model = Ingreso
        fields = [
            'no_ingreso', 'vendedor', 'fecha'
        ]
        export_order = [
            'no_ingreso', 'vendedor', 'fecha'
        ]


class DetalleAdmin(admin.TabularInline):
    model = Detalle_Ingreso
    extra = 3


class IngresoAdmin(ExportMixin, admin.ModelAdmin):
    list_display = [
        'no_ingreso', 'vendedor', 'fecha', 'ficha'
        ]
    list_filter = ['vendedor', 'fecha']
    inlines = [DetalleAdmin]
    exclude = ['no_ingreso']
    search_fields = ['comprador']

admin.site.register(Ingreso, IngresoAdmin)
