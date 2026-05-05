from django.db import models


class Match(models.Model):

    FASES = [
        ('GRUPOS','Grupos'),
        ('DIECISEISAVOS','Dieciseisavos'),
        ('OCTAVOS','Octavos'),
        ('CUARTOS','Cuartos'),
        ('SEMIS','Semifinales'),
        ('TERCER_PUESTO','Tercer Puesto'),
        ('FINAL','Final'),
    ]

    equipo_local = models.CharField(max_length=50)
    equipo_visitante = models.CharField(max_length=50)

    fecha_partido = models.DateTimeField()

    jornada = models.IntegerField()
    grupo = models.CharField(
        max_length=5,
        blank=True,
        null=True
    )

    fase = models.CharField(
        max_length=20,
        choices=FASES
    )

    goles_local = models.IntegerField(
        blank=True,
        null=True
    )

    goles_visitante = models.IntegerField(
        blank=True,
        null=True
    )

    clasificado = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    metodo_clasificacion = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    cerrado = models.BooleanField(default=False)
    
    numero_llave = models.IntegerField(
        blank=True,
        null=True
    )
    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante}"

