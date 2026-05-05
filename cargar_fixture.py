import os
import django
import csv
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from matches.models import Match

print("🚀 INICIANDO SCRIPT...")

try:
    with open('data/fixture_grupos.csv', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')

        for row in reader:
            print("📄 Procesando:", row)

            Match.objects.create(
                equipo_local=row['local'],
                equipo_visitante=row['visitante'],
                fecha_partido=datetime.strptime(row['fecha'], '%d/%m/%y %H:%M'),
                jornada=int(row['jornada']),
                grupo=row['grupo'],
                fase=row['fase']
            )

    print("✅ Fixture cargado correctamente")

except Exception as e:
    print("❌ ERROR:", e)