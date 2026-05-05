from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm
from .models import Perfil


def registro(request):

    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            user = form.save()

            # ✅ guardar teléfono
            Perfil.objects.create(
                user=user,
                telefono=form.cleaned_data['telefono']
            )

            login(request, user)
            return redirect('/predicciones/')  # 👈 flujo directo

    else:
        form = RegistroForm()

    return render(request, 'registration/register.html', {'form': form})