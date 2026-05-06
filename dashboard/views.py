from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User
from predictions.models import Prediction
from matches.models import Match
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Case, When, IntegerField

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

    # 📅 Jornadas
    jornadas = list(
        Match.objects
        .values_list('jornada', flat=True)
        .distinct()
        .order_by('jornada')
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

        for j in jornadas:
            puntos = sum(
                (p.puntos_obtenidos or 0)
                for p in predicciones
                if p.usuario_id == user.id and p.partido.jornada == j
            )

            acumulado += puntos
            puntos_acumulados.append(acumulado)

        evolucion_usuarios.append({
            'usuario': user.username,
            'puntos': puntos_acumulados
        })
    # 📊 TOTAL PREDICCIONES
        # 📊 SOLO predicciones evaluadas
    preds = Prediction.objects.filter(
        usuario=request.user,
        puntos_obtenidos__isnull=False
)

# 🚀 MÉTRICAS OPTIMIZADAS (1 sola consulta)
    stats = preds.aggregate(
        total=Count('id'),
        exactos=Count(Case(When(puntos_obtenidos=3, then=1), output_field=IntegerField())),
        parciales=Count(Case(When(puntos_obtenidos=1, then=1), output_field=IntegerField())),
    )

    total = stats['total'] or 0
    exactos = stats['exactos'] or 0
    parciales = stats['parciales'] or 0
    fallados = total - exactos - parciales

    # 🧮 CÁLCULOS
    tasa_acierto = (exactos / total * 100) if total > 0 else 0
    
    porc_exactos = (exactos / total * 100) if total > 0 else 0
    porc_parciales = (parciales / total * 100) if total > 0 else 0
    porc_fallados = (fallados / total * 100) if total > 0 else 0

    # 📦 contexto final
    contexto = {
        'ranking': ranking,
        'mis_puntos': mis_puntos,
        'cantidad_predicciones': cantidad_predicciones,
        'max_puntos': max_puntos,
        'jornadas': list(jornadas),
        'evolucion_usuarios': evolucion_usuarios,
        'mi_posicion': mi_posicion,
        'tasa_acierto': round(tasa_acierto, 1),
        'exactos': exactos,
        'parciales': parciales,
        'fallados': fallados,
        'porc_exactos': round(porc_exactos, 1),
        'porc_parciales': round(porc_parciales, 1),
        'porc_fallados': round(porc_fallados, 1),
        'total': total
        }

    return render(request, 'dashboard/index.html', contexto)