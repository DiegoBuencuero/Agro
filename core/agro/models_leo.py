from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def vista_trazabilidad(request):
    pass
    # planificaciones = Planificacion_cultivo.objects.filter(empresa = request.user.profile.empresa)
    # empresa = request.user.profile.empresa
    # if request.method == 'POST':
    #     form = PlanificacionCultivoForm(request.POST)
    #     if form.is_valid():
    #         plani = form.save(commit=False)
    #         plani.empresa = empresa
    #         plani.save()
    #         form = PlanificacionCultivoForm()
    # else:
    #     form = PlanificacionCultivoForm()
    # return render(request, 'vista_plani.html', {'planis': planificaciones, 'form': form, 'empresa': empresa })

