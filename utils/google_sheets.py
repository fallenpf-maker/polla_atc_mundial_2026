import os
import json
import gspread

from oauth2client.service_account import (
    ServiceAccountCredentials
)

# =====================================
# CREDENTIALS DESDE RENDER
# =====================================

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

# ==============================
# RENDER
# ==============================

if os.environ.get("GOOGLE_CREDENTIALS"):

    google_creds = json.loads(
        os.environ["GOOGLE_CREDENTIALS"]
    )

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        google_creds,
        scope
    )

# ==============================
# DESARROLLO LOCAL
# ==============================

else:

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials/google_credentials.json",
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