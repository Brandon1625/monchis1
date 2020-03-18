from django.contrib import admin
from .models import *
from import_export import resources
from import_export import fields
from django.shortcuts import redirect
from import_export.admin import ExportMixin


class ModeloResource(resources.ModelResource):
    class Meta:
        model = Venta
        fields = [
            'no_venta', 'comprador', 'fecha', 'total',
            'pago', 'vendedor'
        ]
        export_order = [
            'no_venta', 'comprador', 'fecha', 'total',
            'pago', 'vendedor'
        ]


class DetalleAdmin(admin.TabularInline):
    model = Detalle_Venta
    extra = 5
    readonly_fields = ['precio', 'subtotal']
    autocomplete_fields = ['id_prod']


class VentaAdmin(ExportMixin, admin.ModelAdmin):
    autocomplete_fields = ['comprador']
    actions = ['grafica']
    list_display = [
        'no_venta', 'vendedor', 'comprador',
        'fecha', 'pago', 'total', 'ficha']
    list_filter = ['vendedor', 'fecha']
    inlines = [DetalleAdmin]
    readonly_fields = ['total']
    exclude = ['no_venta']
    search_fields = ['comprador']

    def get_form(self, request, *args, **kwargs):
        form = super(VentaAdmin, self).get_form(
            request, *args, **kwargs)
        usuario = request.user
        form.base_fields['vendedor'].initial = usuario
        return form

    def grafica(self, request, queryset):
        return redirect('/ventas')
    grafica.short_description = 'Ver ventas del mes'

admin.site.register(Venta, VentaAdmin)
