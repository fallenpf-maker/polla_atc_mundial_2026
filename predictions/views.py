from django.shortcuts import render, redirect
from matches.models import Match
from .models import Prediction, ChampionPrediction
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from collections import defaultdict

# =========================================
# FECHA CIERRE
# =========================================

FECHA_CIERRE_GRUPOS = timezone.make_aware(
    datetime(2026, 6, 11, 12, 0)
)

# =========================================
# BANDERAS
# =========================================

FLAGS = {

    # ANFITRIONES
    'Estados Unidos': 'us',
    'México': 'mx',
    'Mexico': 'mx',
    'Canada': 'ca',
    'Canadá': 'ca',

    # CONMEBOL
    'Argentina': 'ar',
    'Brasil': 'br',
    'Uruguay': 'uy',
    'Colombia': 'co',
    'Ecuador': 'ec',
    'Perú': 'pe',
    'Chile': 'cl',
    'Paraguay': 'py',
    'Bolivia': 'bo',
    'Venezuela': 've',

    # UEFA
    'España': 'es',
    'Francia': 'fr',
    'Alemania': 'de',
    'Inglaterra': 'gb',
    'Italia': 'it',
    'Portugal': 'pt',
    'Países Bajos': 'nl',
    'Holanda': 'nl',
    'Croacia': 'hr',
    'Bélgica': 'be',
    'Suiza': 'ch',
    'Dinamarca': 'dk',
    'Suecia': 'se',
    'Noruega': 'no',
    'Polonia': 'pl',
    'Serbia': 'rs',
    'Austria': 'at',
    'Ucrania': 'ua',
    'Turquía': 'tr',
    'República Checa': 'cz',
    'Rep. Checa': 'cz',
    'Escocia': 'gb',
    'Gales': 'gb',
    'Hungría': 'hu',
    'Grecia': 'gr',
    'Rumania': 'ro',

    # AFC
    'Japón': 'jp',
    'Japón': 'jp',
    'Corea del Sur': 'kr',
    'Corea': 'kr',
    'Australia': 'au',
    'Arabia Saudita': 'sa',
    'Irán': 'ir',
    'Qatar': 'qa',
    'Irak': 'iq',
    'Emiratos Árabes Unidos': 'ae',
    'China': 'cn',
    'Uzbekistán': 'uz',

    # CAF
    'Marruecos': 'ma',
    'Senegal': 'sn',
    'Egipto': 'eg',
    'Nigeria': 'ng',
    'Camerún': 'cm',
    'Ghana': 'gh',
    'Costa de Marfil': 'ci',
    'Túnez': 'tn',
    'Argelia': 'dz',
    'Sudáfrica': 'za',

    # CONCACAF
    'Costa Rica': 'cr',
    'Panamá': 'pa',
    'Jamaica': 'jm',
    'Honduras': 'hn',
    'El Salvador': 'sv',

    # OFC
    'Nueva Zelanda': 'nz',

}

# =========================================
# SELECCIONES
# =========================================

SELECCIONES = sorted(list(FLAGS.keys()))

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

        # 🏆 campeón
        campeon = request.POST.get('campeon')

        if campeon:

            ChampionPrediction.objects.update_or_create(
                usuario=request.user,
                defaults={
                    'equipo_campeon': campeon
                }
            )

        # ⚽ predicciones partidos
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

        fecha = partido.fecha_partido.strftime('%d %b %Y')

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