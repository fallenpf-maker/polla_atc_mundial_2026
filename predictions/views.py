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
    datetime(2026, 6, 29, 18, 0)
)

FECHA_CIERRE_16VOS = timezone.make_aware(
    datetime(2026, 6, 25, 18, 0)
)

FECHA_CIERRE_OCTAVOS = timezone.make_aware(
    datetime(2026, 6, 6, 1, 0)
)

FECHA_CIERRE_CUARTOS = timezone.make_aware(
    datetime(2026, 7, 9, 23, 0)
)

FECHA_CIERRE_SEMIS = timezone.make_aware(
    datetime(2026, 7, 14, 18, 0)
)

FECHA_CIERRE_FINAL = timezone.make_aware(
    datetime(2026, 7, 18, 17, 0)
)
# =========================================
# FASE ACTIVA
# =========================================

FASE_ACTIVA = "FINAL"
CAMPEON_HABILITADO = False

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

        
        # =========================================
        # CAMPEÓN
        # =========================================
        campeon_actual = ChampionPrediction.objects.filter(
            usuario=request.user
        ).first()
        
        campeon = None

        if CAMPEON_HABILITADO:
            campeon = request.POST.get("campeon")

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
            # Solo guardar la fase actualmente habilitada
            if partido.fase != FASE_ACTIVA:
                continue
            local = request.POST.get(f'local_{partido.id}')
            visitante = request.POST.get(f'visitante_{partido.id}')

            clasificado = request.POST.get(f'clasificado_{partido.id}')
            metodo = request.POST.get(f'metodo_{partido.id}')

            if local != '' and visitante != '':

                datos = {
                    'pred_local': int(local),
                    'pred_visitante': int(visitante)
                }

    # Solo para eliminatorias
                if partido.fase != 'GRUPOS':

                    datos['equipo_clasificado'] = clasificado
                    datos['metodo_clasificacion'] = metodo

                Prediction.objects.update_or_create(

                    usuario=request.user,

                    partido=partido,

                    defaults=datos

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

        partido.editable = (
            partido.fase == FASE_ACTIVA
        )

        partidos_por_fecha[fecha].append(partido)


# =========================================
# FECHA DE CIERRE SEGÚN FASE ACTIVA
# =========================================

    if FASE_ACTIVA == "GRUPOS":
        fecha_cierre_actual = FECHA_CIERRE_GRUPOS

    elif FASE_ACTIVA == "DIECISEISAVOS":
        fecha_cierre_actual = FECHA_CIERRE_16VOS

    elif FASE_ACTIVA == "OCTAVOS":
        fecha_cierre_actual = FECHA_CIERRE_OCTAVOS

    elif FASE_ACTIVA == "CUARTOS":
        fecha_cierre_actual = FECHA_CIERRE_CUARTOS

    elif FASE_ACTIVA == "SEMIS":
        fecha_cierre_actual = FECHA_CIERRE_SEMIS

    elif FASE_ACTIVA == "FINAL":
        fecha_cierre_actual = FECHA_CIERRE_FINAL

    else:
        fecha_cierre_actual = timezone.now()

    # =========================================
    # CONTEXTO
    # =========================================

    contexto = {

                'partidos_por_fecha': dict(partidos_por_fecha),

                'pred_dict': pred_dict,

                'now': timezone.now(),

                'fecha_cierre': fecha_cierre_actual,

                'selecciones': SELECCIONES,

                'campeon_actual': campeon_actual,
                
                'campeon_habilitado': CAMPEON_HABILITADO,

    }

    return render(
        request,
        'predictions/mis_predicciones.html',
        contexto
    )