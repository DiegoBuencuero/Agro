from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Trazabilidad
from .forms_leo import TrazabilidadForm


@login_required
def vista_trazabilidad(request):
    trazabilidades = Trazabilidad.objects.filter(empresa = request.user.profile.empresa)
    empresa = request.user.profile.empresa
    if request.method == 'POST':
        form = TrazabilidadForm(request.POST)
        if form.is_valid():
            plani = form.save(commit=False)
            plani.empresa = empresa
            plani.save()
            form = TrazabilidadForm()
    else:
        form = TrazabilidadForm()
    return render(request, 'vista_trazabilidad.html', {'trazabilidades': trazabilidades, 'form': form, 'empresa': empresa })

