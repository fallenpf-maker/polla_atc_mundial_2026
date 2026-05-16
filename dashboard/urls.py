from django.urls import path
from .views import dashboard, estadisticas

urlpatterns = [

    path(
        '',
        dashboard,
        name='dashboard'
    ),

    path(
        'estadisticas/',
        estadisticas,
        name='estadisticas'
    ),

]