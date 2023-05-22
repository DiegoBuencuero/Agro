from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Trazabilidad, Lote, Especificacion_tipo, Mov, Com, Deposito
from .forms_leo import TrazabilidadForm
from .views import get_producto

@login_required
def vista_trazabilidad(request):
    empresa = request.user.profile.empresa
    trazabilidades = Trazabilidad.objects.filter(empresa = empresa)
    traza_list = []
    for t in trazabilidades:
        producto = get_producto(t.origen_prod, t.producto_id)
        linea = {
            'campo': t.lote.campo,
            'lote': t.lote,
            'producto_id': producto.id,
            'producto': producto.descripcion,
            'actividad': t.actividad,
        }
        traza_list.append(linea)


    empresa = request.user.profile.empresa
    if request.method == 'POST':
        form = TrazabilidadForm(empresa, request.POST)
        if form.is_valid():
            traz = form.save(commit=False)
            traz.empresa = empresa
            traz.perfil = request.user.profile
            com = Com.objects.get(id=1)
            depo = Deposito.objects.get(id=1)
            movim = Mov(empresa = empresa, n_suc=0, n_com=0, fecha=traz.fecha, com=com, deposito1 = depo)
            movim.save()
            traz.id_mov = movim
            try:
                traz.lote = Lote.objects.get(id = form.cleaned_data['lote_campo'])
                traz.origen_prod = form.cleaned_data['producto'][0:1]
                traz.producto_id = int(form.cleaned_data['producto'][1:])
                try:
                    traz.especificacion = Especificacion_tipo.objects.get(id = form.cleaned_data['espec'])
                    form = TrazabilidadForm(empresa)
                except:
                    form.add_error('espec', 'Error inesperado, la especificacion no existe')
                    print('error 1')
            except:
                form.add_error('lote_campo', 'Error inesperado, el lote no existe')
                print('error 2')
            traz.save()

        else:
            print(form.errors.as_data)
    else:
        form = TrazabilidadForm(empresa)
    return render(request, 'vista_trazabilidad.html', {'trazabilidades': traza_list, 'form': form, 'empresa': empresa })

