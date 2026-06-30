from django.db import models
from django.contrib.auth.models import User
from matches.models import Match

class Prediction(models.Model):

    METODOS = [
        ('REGULAR', 'Tiempo Regular'),
        ('PRORROGA', 'Prórroga'),
        ('PENALES', 'Penales'),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    partido = models.ForeignKey(
        Match,
        on_delete=models.CASCADE
    )

    pred_local = models.IntegerField()
    pred_visitante = models.IntegerField()

    equipo_clasificado = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    metodo_clasificacion = models.CharField(
        max_length=20,
        choices=METODOS,
        blank=True,
        null=True
    )

    puntos_obtenidos = models.IntegerField(
        default=0
    )

    creado_en = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('usuario', 'partido')

    def calcular_puntos(self):

        puntos = 0

        real_local = self.partido.goles_local
        real_visit = self.partido.goles_visitante

        # 🚫 Si no hay resultado aún
        if real_local is None or real_visit is None:
            return 0

        fase = self.partido.fase
        pred_es_empate = (
                self.pred_local == self.pred_visitante
        )
        # 🎯 MARCADOR EXACTO
        if (
            self.pred_local == real_local and
            self.pred_visitante == real_visit
        ):
            puntos += 3

        else:
            pred_signo = (
                1 if self.pred_local > self.pred_visitante
                else -1 if self.pred_local < self.pred_visitante
                else 0
            )

            real_signo = (
                1 if real_local > real_visit
                else -1 if real_local < real_visit
                else 0
            )

            if pred_signo == real_signo:
                puntos += 1

        # 🟢 FASE DE GRUPOS → SOLO RESULTADO
        if fase == 'GRUPOS':
            self.puntos_obtenidos = puntos
            self.save()
            return puntos

        # =====================================
        # ELIMINATORIAS
        # =====================================
    
        # ¿Acertó el clasificado?
        # =====================================
# ELIMINATORIAS
# =====================================

# Si el usuario NO pronosticó empate,
# solamente cuentan los puntos del resultado.

        if not pred_es_empate:

            self.puntos_obtenidos = puntos
            self.save()

            return puntos


# -------------------------------------------------
# Desde aquí solamente llegan los pronósticos
# que fueron EMPATE
# -------------------------------------------------

        acerto_clasificado = (
            self.equipo_clasificado ==
            self.partido.clasificado
        )

        acerto_metodo = (
            self.metodo_clasificacion ==
            self.partido.metodo_clasificacion
        )

        if acerto_clasificado:
            puntos += 1

        if acerto_metodo:
            puntos += 1

        self.puntos_obtenidos = puntos
        self.save()

        return puntos

    def __str__(self):
        return f"{self.usuario} - {self.partido}"
    
class ChampionPrediction(models.Model):

        usuario = models.OneToOneField(
            User,
            on_delete=models.CASCADE
        )

        equipo_campeon = models.CharField(
            max_length=100
        )

        fecha_registro = models.DateTimeField(
            auto_now=True
        )

def __str__(self):
        return f"{self.usuario} → {self.equipo_campeon}"