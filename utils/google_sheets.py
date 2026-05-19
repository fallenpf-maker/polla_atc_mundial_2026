import os
import json
import gspread

from oauth2client.service_account import (
    ServiceAccountCredentials
)

# =====================================
# CREDENTIALS DESDE RENDER
# =====================================

google_creds = json.loads(
    os.environ.get('GOOGLE_CREDENTIALS')
)

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    google_creds,
    scope
)

client = gspread.authorize(creds)

# =====================================
# PREDICCIONES
# =====================================

def guardar_prediccion(data):

    try:

        sheet = client.open(
            'Backup Mundial 2026'
        ).worksheet('Predicciones')

        sheet.append_row(data)

        print("✅ Predicción enviada a Google Sheets")

    except Exception as e:

        print("❌ ERROR GOOGLE SHEETS:")
        print(e)

# =====================================
# CAMPEÓN
# =====================================

def guardar_campeon(data):

    try:

        sheet = client.open(
            'Backup Mundial 2026'
        ).worksheet('Campeon')

        sheet.append_row(data)

        print("✅ Campeón enviado a Google Sheets")

    except Exception as e:

        print("❌ ERROR GOOGLE SHEETS:")
        print(e)