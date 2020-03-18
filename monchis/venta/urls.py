from django.urls import path
from .views import ventas

app_name = 'producto'
urlpatterns = [
    path('ventas', ventas, name='grafica'),
]
