from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User
from predictions.models import Prediction
from matches.models import Match
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Case, When, IntegerField
from django.db.models.functions import TruncDate

@login_required

def dashboard(request):

    # 🏆 Ranking (con manejo de None)
    ranking = (
        User.objects
        .annotate(
            puntos_totales=Coalesce(Sum('prediction__puntos_obtenidos'), 0)
        )
        .order_by('-puntos_totales')
    )

    # 🏆 máximo para barras
    max_puntos = ranking[0].puntos_totales if ranking else 1

    # 👤 Usuario actual
    mis_puntos = (
        Prediction.objects
        .filter(usuario=request.user)
        .aggregate(total=Sum('puntos_obtenidos'))['total'] or 0
    )

    cantidad_predicciones = (
        Prediction.objects
        .filter(usuario=request.user)
        .count()
    )

    # 🏆 Posición del usuario
    mi_posicion = None
    for i, user in enumerate(ranking, start=1):
        if user.id == request.user.id:
            mi_posicion = i
            break

    # 📅 Fechas únicas de partidos
    fechas = list(
        Match.objects
        .filter(
            goles_local__isnull=False,
            goles_visitante__isnull=False
        )
        .annotate(fecha=TruncDate('fecha_partido'))
        .values_list('fecha', flat=True)
        .distinct()
        .order_by('fecha')
    )

    # 👥 usar ranking para mantener orden consistente
    usuarios = list(ranking)

    # ⚡ OPTIMIZACIÓN: traer todas las predicciones en una sola consulta
    predicciones = Prediction.objects.select_related('partido').all()

    # 📊 evolución acumulada de TODOS los usuarios
    evolucion_usuarios = []

    for user in usuarios:

        acumulado = 0
        puntos_acumulados = []

        for fecha in fechas:

            puntos = sum(
                (p.puntos_obtenidos or 0)
                for p in predicciones
                if (
                    p.usuario_id == user.id and
                    p.partido.fecha_partido.date() == fecha
                )
            )

            acumulado += puntos
            puntos_acumulados.append(acumulado)

        evolucion_usuarios.append({
            'usuario': user.username,
            'puntos': puntos_acumulados
        })
    # 📊 TOTAL PREDICCIONES
        # 📊 SOLO predicciones evaluadas
    
    # =====================================
# ESTADÍSTICAS PERSONALES
# =====================================

        preds = Prediction.objects.filter(
    usuario=request.user
)

        total = preds.count()

# Pronósticos aún no evaluados
        pendientes = preds.filter(
            partido__goles_local__isnull=True
        ).count()

# Solo partidos con resultado cargado
        evaluadas = preds.filter(
            partido__goles_local__isnull=False,
            partido__goles_visitante__isnull=False
        )

        exactos = evaluadas.filter(
            puntos_obtenidos=3
        ).count()

        parciales = evaluadas.filter(
            puntos_obtenidos=1
        ).count()

        fallados = evaluadas.filter(
            puntos_obtenidos=0
        ).count()

        total_evaluadas = evaluadas.count()

# Porcentajes
        tasa_acierto = (
            (exactos / total_evaluadas) * 100
            if total_evaluadas > 0
            else 0
        )

        porc_exactos = (
            (exactos / total_evaluadas) * 100
            if total_evaluadas > 0
            else 0
        )

        porc_parciales = (
            (parciales / total_evaluadas) * 100
            if total_evaluadas > 0
            else 0
        )

        porc_fallados = (
            (fallados / total_evaluadas) * 100
            if total_evaluadas > 0
            else 0
        )

    # 📦 contexto final
    contexto = {
        'ranking': ranking,
        'mis_puntos': mis_puntos,
        'cantidad_predicciones': cantidad_predicciones,
        'max_puntos': max_puntos,
        'fechas': [
            f.strftime('%d/%b')
            for f in fechas
        ],
        'evolucion_usuarios': evolucion_usuarios,
        'mi_posicion': mi_posicion,
        'tasa_acierto': round(tasa_acierto, 1),
        'exactos': exactos,
        'parciales': parciales,
        'fallados': fallados,
        'pendientes': pendientes,
        'total_evaluadas': total_evaluadas,
        'porc_exactos': round(porc_exactos, 1),
        'porc_parciales': round(porc_parciales, 1),
        'porc_fallados': round(porc_fallados, 1),
        'total': total
        }

    return render(request, 'dashboard/index.html', contexto)

@login_required
def estadisticas(request):

    # 🏆 Ranking
    ranking = (
        User.objects
        .annotate(
            puntos_totales=Coalesce(
                Sum('prediction__puntos_obtenidos'),
                0
            )
        )
        .order_by('-puntos_totales')
    )

    # 📅 Fechas únicas
    fechas = list(
        Match.objects
        .filter(
            goles_local__isnull=False,
            goles_visitante__isnull=False
        )
        .annotate(fecha=TruncDate('fecha_partido'))
        .values_list('fecha', flat=True)
        .distinct()
        .order_by('fecha')
    )

    # 👥 usuarios
    usuarios = list(ranking)

    # ⚡ predicciones
    predicciones = Prediction.objects.select_related('partido').all()

    # 📈 evolución
    evolucion_usuarios = []

    for user in usuarios:

        acumulado = 0
        puntos_acumulados = []

        for fecha in fechas:

            puntos = sum(
                (p.puntos_obtenidos or 0)
                for p in predicciones
                if (
                    p.usuario_id == user.id and
                    p.partido.fecha_partido.date() == fecha
                )
            )

            acumulado += puntos
            puntos_acumulados.append(acumulado)

        evolucion_usuarios.append({
            'usuario': user.username,
            'puntos': puntos_acumulados
        })

    contexto = {

        'ranking': ranking,

        'fechas': [
            f.strftime('%d/%b')
            for f in fechas
        ],

        'evolucion_usuarios': evolucion_usuarios,
    }

    return render(
        request,
        'dashboard/estadisticas.html',
        contexto
    )