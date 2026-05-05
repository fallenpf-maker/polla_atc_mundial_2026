from django.urls import path
from .views import mis_predicciones

urlpatterns = [
    path('', mis_predicciones, name='mis_predicciones'),
]