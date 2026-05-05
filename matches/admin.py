from django.contrib import admin
from .models import Match
from predictions.models import Prediction


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):

    list_display = (
        'equipo_local',
        'equipo_visitante',
        'fase',
        'numero_llave',
        'fecha_partido'
    )

    def save_model(
        self,
        request,
        obj,
        form,
        change
    ):

        super().save_model(
            request,
            obj,
            form,
            change
        )

        predicciones = Prediction.objects.filter(
            partido=obj
        )

        for p in predicciones:
            p.calcular_puntos()