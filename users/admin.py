from django.contrib import admin
from .models import Perfil

# =====================================
# PERFIL
# =====================================

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'telefono'
    )