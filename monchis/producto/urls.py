from django.urls import path
from .views import ProductoLista, contact, productosgrafica

app_name = 'producto'
urlpatterns = [
    path('', ProductoLista, name='productos'),
    path('productosgrafica', productosgrafica, name='grafica'),
    path('contacto', contact, name='contacto'),
]
