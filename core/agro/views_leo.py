from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Trazabilidad, Lote, Especificacion_tipo, Mov, Com, Deposito, Contactos
from .models import Campo, EstadoLote
from .forms_leo import TrazabilidadForm, ContactoForm, EstadoLoteForm
from .views import get_producto
from datetime import datetime


def get_traza_list(empresa):
    trazabilidades = Trazabilidad.objects.filter(empresa = empresa)
    traza_list = []
    for t in trazabilidades:
        producto = get_producto(t.origen_prod, t.producto_id)
        linea = {
            'id': t.id,
            'campo': t.lote.campo,
            'lote': t.lote,
            'producto_id': producto.id,
            'producto': producto.descripcion,
            'actividad': t.actividad,
            'cantidad': t.cantidad,
        }
        traza_list.append(linea)
    return traza_list

@login_required
def vista_trazabilidad(request):

    empresa = request.user.profile.empresa
    traza_list = get_traza_list(empresa)
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
                    traz.save()
                    traza_list = get_traza_list(empresa)
                    form = TrazabilidadForm(empresa)
                except:
                    form.add_error('espec', 'Error inesperado, la especificacion no existe')
            except:
                form.add_error('lote_campo', 'Error inesperado, el lote no existe')

        else:
            print(form.errors.as_data)
    else:
        form = TrazabilidadForm(empresa)
    return render(request, 'vista_trazabilidad.html', {'trazabilidades': traza_list, 'form': form, 'empresa': empresa })

@login_required
def editar_trazabilidad(request, id_traza):
    empresa = request.user.profile.empresa
    traza_list = get_traza_list(empresa)
    try:
        trazabilidad = Trazabilidad.objects.get(id = id_traza)
    except:
        return redirect('vista_trazabilidad')
    if trazabilidad.empresa == empresa:
        if request.method == 'POST':
            form = TrazabilidadForm(request.POST, instance = trazabilidad)
            if form.is_valid():
                traz = form.save(commit=False)
                if request.POST.get('borrar') == '':
                    traz.delete()
                else:
                    try:
                        traz.lote = Lote.objects.get(id = form.cleaned_data['lote_campo'])
                        traz.origen_prod = form.cleaned_data['producto'][0:1]
                        traz.producto_id = int(form.cleaned_data['producto'][1:])
                        try:
                            traz.especificacion = Especificacion_tipo.objects.get(id = form.cleaned_data['espec'])
                            traz.save()
                            traza_list = get_traza_list(empresa)
                            return redirect('vista_planificacion')
                        except:
                            form.add_error('espec', 'Error inesperado, la especificacion no existe')
                    except:
                        form.add_error('lote_campo', 'Error inesperado, el lote no existe')
        else:
            initial_data = {
                'producto': trazabilidad.origen_prod + str(trazabilidad.producto_id),
                'espec': trazabilidad.especificacion,
                'campo': trazabilidad.lote.campo.id,
                'lote_campo': trazabilidad.lote,
            }
            form = TrazabilidadForm(empresa, initial = initial_data, instance = trazabilidad)
        return render(request, 'vista_trazabilidad.html', {'form': form, 'empresa': empresa, 'trazabilidades':traza_list, 'modificacion': 'S'})
    else:
        return redirect('vista_planificacion')





@login_required
def vista_contactos(request):

    empresa = request.user.profile.empresa
    contactos = Contactos.objects.filter(empresa = empresa)
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            cont = form.save(commit=False)
            cont.empresa = empresa
            cont.save()
            form.save_m2m()
            form = ContactoForm()
    else:
        form = ContactoForm()
    return render(request, 'vista_contacto.html', {'contactos': contactos, 'form': form, 'empresa': empresa })



@login_required
def editar_contacto(request, id_contacto):
    empresa = request.user.profile.empresa
    try:
        contacto = Contactos.objects.get(id=id_contacto)
    except:
        return redirect('vista_contactos')
    if contacto.empresa != empresa:
        return redirect('vista_contactos')
    contactos = Contactos.objects.filter(empresa = empresa)
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance = contacto)
        if form.is_valid():
            cont = form.save()
            form = ContactoForm()
    else:
        form = ContactoForm(instance = contacto)
    return render(request, 'vista_contacto.html', {'contactos': contactos, 'form': form, 'empresa': empresa,  'modificacion': 'S' })


@login_required
def vista_estado_lote(request):
    hoy = datetime.today().date()
    empresa = request.user.profile.empresa
    campos = Campo.objects.filter(empresa=empresa)
    lotes = Lote.objects.filter(campo__in = campos)
    lista = []
    for lote in lotes:
        porciento = (lote.ha_productivas/lote.ha_totales) * 100
        estados = EstadoLote.objects.filter(lote = lote)
        encontre = False
        for estado in estados:
            if hoy >= estado.fecha_desde and hoy <= estado.fecha_hasta:
                encontre = True
                break
        if encontre:
            linea = {'lote': lote, 'estado': estado, 'encontre': encontre, 'p':porciento}
            lista.append(linea)
        else:
            linea = {'lote': lote,  'encontre': encontre, 'p': porciento}
            lista.append(linea)
    return render(request, 'vista_estado_lote.html', {'estados': lista, 'hoy': hoy, 'empresa': empresa, })


@login_required
def vista_asign_lote(request, id_lote):
    empresa = request.user.profile.empresa
    try:
        lote = Lote.objects.get(id=id_lote)
    except:
        return redirect('vista_estado_lote')

    if request.method == 'POST':
        form = EstadoLoteForm(empresa, request.POST)
        if form.is_valid():
            estado = form.save(commit=False)
            estado.lote = lote
            estado.save()
            form = EstadoLoteForm(empresa)
    else:
        form = EstadoLoteForm(empresa)
    return render(request, 'vista_asign_lote.html', { 'lote':lote, 'form': form, 'empresa': empresa })
