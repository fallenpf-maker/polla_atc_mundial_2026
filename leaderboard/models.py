from django.db import models
from django.contrib.auth.models import User


class RankingHistorico(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    jornada = models.IntegerField()

    puntos_jornada = models.IntegerField(
        default=0
    )

    puntos_acumulados = models.IntegerField(
        default=0
    )

    posicion = models.IntegerField(
        default=0
    )


    class Meta:
        unique_together = (
            'usuario',
            'jornada'
        )


    def __str__(self):
        return (
            f"{self.usuario} "
            f"J{self.jornada} "
            f"Puesto {self.posicion}"
        )