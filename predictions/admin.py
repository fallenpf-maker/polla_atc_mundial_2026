from django.contrib import admin
from .models import Prediction
from .models import ChampionPrediction

admin.site.register(Prediction)
admin.site.register(ChampionPrediction)