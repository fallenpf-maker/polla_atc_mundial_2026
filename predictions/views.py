from django.shortcuts import render, redirect
from matches.models import Match
from .models import Prediction
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime

FECHA_CIERRE_GRUPOS = timezone.make_aware(
    datetime(2026, 6, 11, 12, 0)
)

@login_required
def mis_predicciones(request):

    partidos = Match.objects.filter(fase='GRUPOS').order_by('fecha_partido')

    if request.method == 'POST':

    # 🚫 BLOQUEO GLOBAL TOTAL
        if timezone.now() >= FECHA_CIERRE_GRUPOS:
            return redirect('mis_predicciones')

        for partido in partidos:

            local = request.POST.get(f'local_{partido.id}')
            visitante = request.POST.get(f'visitante_{partido.id}')

            if local != '' and visitante != '':

                Prediction.objects.update_or_create(
                    usuario=request.user,
                    partido=partido,
                    defaults={
                        'pred_local': int(local),
                        'pred_visitante': int(visitante)
                    }
                )

        return redirect('mis_predicciones')

    predicciones = Prediction.objects.filter(usuario=request.user)

    pred_dict = {
        p.partido.id: p for p in predicciones
    }

    contexto = {
        'partidos': partidos,
        'pred_dict': pred_dict,
        'now': timezone.now(),
        'fecha_cierre': FECHA_CIERRE_GRUPOS
    }

    return render(request, 'predictions/mis_predicciones.html', contexto)