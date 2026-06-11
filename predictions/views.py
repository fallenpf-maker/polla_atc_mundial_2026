from django.shortcuts import render, redirect
from matches.models import Match
from .models import Prediction, ChampionPrediction
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from collections import defaultdict
from utils.google_sheets import (
    guardar_prediccion,
    guardar_campeon
)
# =========================================
# FECHA CIERRE
# =========================================

FECHA_CIERRE_GRUPOS = timezone.make_aware(
    datetime(2026, 6, 11, 15, 0)
)

# =========================================
# BANDERAS
# =========================================

FLAGS = {

    # ANFITRIONES
    'Estados Unidos': 'us',
    'México': 'mx',
    'Canadá': 'ca',

# CONMEBOL
    'Argentina': 'ar',
    'Brasil': 'br',
    'Uruguay': 'uy',
    'Colombia': 'co',
    'Ecuador': 'ec',
    'Paraguay': 'py',

# UEFA
    'España': 'es',
    'Francia': 'fr',
    'Alemania': 'de',
    'Inglaterra': 'gb',
    'Portugal': 'pt',
    'Países Bajos': 'nl',
    'Croacia': 'hr',
    'Bélgica': 'be',
    'Suiza': 'ch',
    'Escocia': 'gb',
    'Noruega': 'no',
    'Austria': 'at',
    'Suecia': 'se',
    'Turquía': 'tr',
    'Bosnia y Herc.': 'ba',
    'Rep. Checa': 'cz',

# AFC
    'Japón': 'jp',
    'Corea del Sur': 'kr',
    'Australia': 'au',
    'Arabia Saudita': 'sa',
    'Irán': 'ir',
    'Qatar': 'qa',
    'Uzbekistán': 'uz',
    'Irak': 'iq',
    'Jordania': 'jo',

# CAF
    'Marruecos': 'ma',
    'Senegal': 'sn',
    'Egipto': 'eg',
    'Ghana': 'gh',
    'Costa de Marfil': 'ci',
    'Túnez': 'tn',
    'Sudáfrica': 'za',
    'Argelia': 'dz',
    'Cabo Verde': 'cv',
    'RD Congo': 'cd',

# CONCACAF
    'Panamá': 'pa',
    'Haití': 'ht',
    'Curazao': 'cw',

# OFC
    'Nueva Zelanda': 'nz',
}

# =========================================
# SELECCIONES
# =========================================

SELECCIONES = sorted(list(set(FLAGS.keys())))

# =========================================
# VIEW PRINCIPAL
# =========================================

@login_required
def mis_predicciones(request):

    partidos = Match.objects.all().order_by('fecha_partido')

    # =========================================
    # POST
    # =========================================

    if request.method == 'POST':

        # 🚫 BLOQUEO TOTAL
        if timezone.now() >= FECHA_CIERRE_GRUPOS:
            return redirect('mis_predicciones')

        # =========================================
        # CAMPEÓN
        # =========================================
        campeon_actual = ChampionPrediction.objects.filter(
            usuario=request.user
        ).first()
        
        campeon = request.POST.get('campeon')

        if campeon:

            ChampionPrediction.objects.update_or_create(
                usuario=request.user,
                defaults={
                    'equipo_campeon': campeon
                }
            )
            if campeon and not campeon_actual:

                guardar_campeon([
                    str(timezone.now()),
                    request.user.username,
                    campeon
                ])
        # =========================================
        # PREDICCIONES
        # =========================================

        predicciones_export = []

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

                predicciones_export.append(
                    f"{partido.equipo_local} vs {partido.equipo_visitante}: {local}-{visitante}"
                )

# =====================================
# GOOGLE SHEETS (UNA SOLA FILA)
# =====================================

        if predicciones_export:

            try:

                guardar_prediccion([
                    str(timezone.now()),
                    request.user.username,
                    " | ".join(predicciones_export)
                ])

            except Exception as e:

                print("ERROR EXPORTANDO:")
                print(e)
        return redirect('mis_predicciones')

    # =========================================
    # PREDICCIONES USUARIO
    # =========================================

    predicciones = Prediction.objects.filter(
        usuario=request.user
    )

    pred_dict = {
        p.partido.id: p
        for p in predicciones
    }

    # =========================================
    # CAMPEÓN ACTUAL
    # =========================================

    campeon_actual = ChampionPrediction.objects.filter(
        usuario=request.user
    ).first()

    # =========================================
    # AGRUPAR PARTIDOS POR FECHA
    # =========================================

    partidos_por_fecha = defaultdict(list)

    for partido in partidos:

        fecha = partido.fecha_partido.date()

        partido.flag_local = FLAGS.get(
            partido.equipo_local,
            'un'
        )

        partido.flag_visitante = FLAGS.get(
            partido.equipo_visitante,
            'un'
        )

        partidos_por_fecha[fecha].append(partido)

    # =========================================
    # CONTEXTO
    # =========================================

    contexto = {

        'partidos_por_fecha': dict(partidos_por_fecha),

        'pred_dict': pred_dict,

        'now': timezone.now(),

        'fecha_cierre': FECHA_CIERRE_GRUPOS,

        'selecciones': SELECCIONES,

        'campeon_actual': campeon_actual,

    }

    return render(
        request,
        'predictions/mis_predicciones.html',
        contexto
    )