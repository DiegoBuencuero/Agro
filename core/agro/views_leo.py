from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Trazabilidad
from .forms_leo import TrazabilidadForm
from .views import get_producto

@login_required
def vista_trazabilidad(request):
    trazabilidades = Trazabilidad.objects.filter(empresa = request.user.profile.empresa)
    traza_list = []
    for t in trazabilidades:
        producto = get_producto(t.origen_prod, t.producto_id)
        linea = {
            'campo': t.campo,
            'lote': t.lote,
            'producto_id': producto.id,
            'producto': producto.descripcion,
            'actividad': t.actividad,
        }
        traza_list.append(linea)


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
    return render(request, 'vista_trazabilidad.html', {'trazabilidades': traza_list, 'form': form, 'empresa': empresa })

