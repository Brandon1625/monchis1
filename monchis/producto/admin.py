from django.contrib import admin
from .models import Categoriaproducto, Producto, AumentoProducto
from django.shortcuts import redirect
from import_export import resources
from import_export import fields
from import_export.admin import ExportMixin


class ModeloProdResource(resources.ModelResource):
    class Meta:
        model = Producto
        fields = [
            'nombre', 'categoria'
            ]
        export_order = [
            'nombre', 'categoria'
            ]


class ModeloCatResource(resources.ModelResource):
    class Meta:
        model = Categoriaproducto
        fields = [
            'categoria'
            ]
        export_order = [
            'categoria'
            ]


class ProductoAdmin(ExportMixin, admin.ModelAdmin):
    ordering = ['nombre', 'cantidad']
    search_fields = ['nombre']
    actions = ['inactivar', 'activar', 'informe', 'grafica']
    list_display = ['image_tag', 'nombre', 'descripcion', 'categoria', 'ref', 'activo', 'visible', 'cantidad']
    list_filter = ['categoria']
    readonly_fields = ['cantidad']

    def get_actions(self, request):
        actions = super(ProductoAdmin, self).get_actions(request)
        if not request.user.is_superuser:
           del actions['informe']
           del actions['grafica']
           del actions['activar']
           del actions['inactivar']
        return actions

    def inactivar(self, request, queryset):

        for row in queryset.filter(activo=True):
            self.log_change(request, row, 'inactivar producto')
        rows_updated = 0

        for obj in queryset:
            if obj.activo:
                obj.activo = False
                obj.save()

                rows_updated += 1

        if rows_updated == 1:
            message_bit = "1 producto se marco"
        else:
            message_bit = "%s productos se marcaron" % rows_updated
        self.message_user(
            request, "%s satisfactoriamente como inactivos" % message_bit)
    inactivar.short_description = 'Inactivar producto'

    def activar(self, request, queryset):
        for row in queryset.filter(activo=False):
            self.log_change(request, row, 'activar cliente')
        rows_updated = 0

        for obj in queryset:
            if not obj.activo:
                obj.activo = True
                obj.save()

                rows_updated += 1

        if rows_updated == 1:
            message_bit = "1 producto se marco"
        else:
            message_bit = "%s productos se marcaron" % rows_updated
        self.message_user(
            request, "%s satisfactoriamente como activos" % message_bit)
    activar.short_description = 'Activar Producto'

    def informe(self, request, queryset):
        return redirect('/productos')
    informe.short_description = 'Exportar en formato PDF'

    def grafica(self, request, queryset):
        return redirect('/productosgrafica')
    grafica.short_description = 'Ver grafica de productos'


class CategoriaAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['categoria']
    list_filter = ['categoria']
    search_fields = ['categoria']
    ordering = ['categoria']


admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoriaproducto, CategoriaAdmin)
