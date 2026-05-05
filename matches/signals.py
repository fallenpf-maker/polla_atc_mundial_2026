from django.db.models.signals import post_save
from django.dispatch import receiver
from matches.models import Match
from predictions.models import Prediction

@receiver(post_save, sender=Match)
def calcular_puntos_predicciones(sender, instance, **kwargs):

    # Solo si el partido tiene resultado
    if instance.goles_local is None or instance.goles_visitante is None:
        return

    predicciones = Prediction.objects.filter(partido=instance)

    for pred in predicciones:
        pred.calcular_puntos()