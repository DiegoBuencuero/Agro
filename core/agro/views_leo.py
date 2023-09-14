from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TrazaLote, Lote, Especificacion_tipo, Mov, Com, Deposito, Contactos
from .models import Campo, EstadoLote, Planificacion_cultivo, Actividad
from .models import Prod_Conf
from .forms_leo import TrazabilidadForm, TrazaLoteItemFormSet, ContactoForm, EstadoLoteForm, agro_Producto, Producto, ProdConfForm
from .views import get_producto
from datetime import datetime
from django.http import HttpResponse, JsonResponse


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
            if hoy >= estado.fecha_desde and hoy <= estado.fecha_hasta and estado.estado != 'C':
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
    hoy = datetime.today().date()
    empresa = request.user.profile.empresa
    try:
        lote = Lote.objects.get(id=id_lote)
    except:
        return redirect('vista_estado_lote')

    modificacion = False
    estados = EstadoLote.objects.filter(lote = lote).filter(fecha_desde__lte = hoy).filter(fecha_hasta__gte = hoy)
    if len(estados) > 0:
        for i, estado in enumerate(estados):
            if i > 0:
                estado.delete()
        estado_edit = estados[0]
        modificacion = True
    if request.method == 'POST':
        if modificacion:
            form = EstadoLoteForm(empresa, request.POST, instance = estado_edit)
        else:
            form = EstadoLoteForm(empresa, request.POST)
        if form.is_valid():
            estado = form.save(commit=False)
            if request.POST.get('borrar') == '':
                estado.delete()
                return redirect('vista_estado_lote')
            else:
                estado.lote = lote
                if estado.fecha_hasta <= estado.fecha_desde:
                    form.add_error('fecha_desde', 'La fecha origen debe ser menor a la fecha de finalizacion del cultivo')
                    form.add_error('fecha_hasta', 'La fecha final debe ser mayor a la fecha de inicio del cultivo')
                else:
                    estado.save()
                    return redirect('vista_estado_lote')
        else:
            print(form.errors.as_data)
    else:
        if modificacion:
            form = EstadoLoteForm(empresa, instance = estado_edit)
        else:
            form = EstadoLoteForm(empresa)
    context = { 'lote':lote, 'form': form, 'empresa': empresa }
    if modificacion:
        context["modificacion"] = 'M'
    return render(request, 'vista_asign_lote.html', context )


def ajax_get_planificacion(request):
    plani_id = request.GET.get('plani')
    planificacion = Planificacion_cultivo.objects.get(id = plani_id)
    data = {'desde': planificacion.fecha_desde, 'hasta': planificacion.fecha_hasta, 'cultivo_nombre':planificacion.costo.cultivo.nombre, 'cultivo_id':planificacion.costo.cultivo.id}
    return JsonResponse(data)



@login_required
def vista_lote_trazabilidad(request):
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
            if hoy >= estado.fecha_desde and hoy <= estado.fecha_hasta and estado.estado != 'C':
                encontre = True
                break
        if encontre:
            dias = estado.fecha_hasta - hoy
            linea = {'lote': lote, 'estado': estado,  'p':porciento, 'dias': dias.days}
            lista.append(linea)
    return render(request, 'vista_lote_trazabilidad.html', {'estados': lista, 'hoy': hoy, 'empresa': empresa, })

@login_required
def vista_trazabilidad_lote(request, id_estado):
    try:
        estado = EstadoLote.objects.get(id = id_estado)
    except:
        return redirect('vista_lote_trazabilidad')
    
    empresa = request.user.profile.empresa
    if estado.lote.campo.empresa == empresa:
        if request.method == 'POST':
            form = TrazabilidadForm(empresa, request.POST)
            traza_lote_item_formset = TrazaLoteItemFormSet(request.POST, prefix='traza_lote_item')
            if form.is_valid() and traza_lote_item_formset.is_valid():
                traz = form.save(commit=False)
                traz.estado_lote = estado
                traz.perfil = request.user.profile
                traz.empresa = empresa
                traz.save()
                for subform in traza_lote_item_formset:
                    print('formulario')
                    if subform.cleaned_data:
                        item = subform.save(commit=False)
                        item.trazalote = traz
                        item.save()
                return redirect('vista_trazabilidad')
                # if traz.fecha is None:
                #     form.add_error('fecha', 'Este campo es requerido')
                # else:
                #     traz.empresa = empresa
                #     traz.perfil = request.user.profile
                #     com = Com.objects.get(id=1)
                #     depo = Deposito.objects.get(id=1)
                #     movim = Mov(empresa = empresa, n_suc=0, n_com=0, fecha=traz.fecha, com=com, deposito1 = depo)
                #     movim.save()
                #     traz.id_mov = movim
                #     try:
                #         traz.estado_lote = estado
                #         traz.origen_prod = form.cleaned_data['producto'][0:1]
                #         traz.producto_id = int(form.cleaned_data['producto'][1:])
                #         try:
                #             traz.especificacion = Especificacion_tipo.objects.get(id = form.cleaned_data['espec'])
                #             traz.save()
                #             if traz.actividad.codigo == 'FP':
                #                 estado.estado = 'C'
                #                 estado.save()
                #                 return redirect('vista_lote_trazabilidad')
                #             traza_list = get_traza_list(empresa, estado)
                #             form = TrazabilidadForm(empresa)
                #         except:
                #             form.add_error('espec', 'Error inesperado, la especificacion no existe')
                #     except:
                #         form.add_error('lote_campo', 'Error inesperado, el lote no existe')
            else:
                print(form.errors.as_data)
                for x in traza_lote_item_formset:
                    print(x.errors.as_data)
                #print(traza_lote_item_formset.errors.as_data)
        else:
            form = TrazabilidadForm(empresa)
            traza_lote_item_formset = TrazaLoteItemFormSet(prefix='traza_lote_item')
        return render(request, 'vista_trazabilidad.html', {'traza_lote_item_formset': traza_lote_item_formset, 'form': form, 'estado_lote': estado, 'empresa': empresa })
    else:
        return redirect('vista_lote_trazabilidad')
    
def ajax_get_prods_actividad(request):
    actividad_id = request.GET.get('actividad')
    actividad = Actividad.objects.get(id = actividad_id)
    tipos = actividad.agro_tipo.all()
    respuesta = []
    for t in tipos:
        productosA = agro_Producto.objects.filter(agro_tipo = t)
        productosU = Producto.objects.filter(agro_tipo = t)
        for p in productosA:
            linea = {'id': 'A'+str(p.id), 'desc': p.descripcion}
            respuesta.append(linea)
        for p in productosU:
            linea = {'id': 'U'+str(p.id), 'desc': p.descripcion}
            respuesta.append(linea)
    data = {'data': respuesta}
    return JsonResponse(data)


@login_required
def editar_trazabilidad(request, id_traza):
    empresa = request.user.profile.empresa
    try:
        trazabilidad = Trazabilidad.objects.get(id = id_traza)
    except:
        return redirect('vista_trazabilidad')
    estado = trazabilidad.estado_lote
    traza_list = get_traza_list(empresa, estado)

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
                'espec': trazabilidad.especificacion.id,
            }
            print(initial_data)
            form = TrazabilidadForm(empresa, initial = initial_data, instance = trazabilidad)
        return render(request, 'vista_trazabilidad.html', {'form': form, 'empresa': empresa, 'trazabilidades':traza_list, 'modificacion': 'S'})
    else:
        return redirect('vista_trazabilidad')


@login_required
def vista_conf_producto(request):
    empresa = request.user.profile.empresa
    productos = Prod_Conf.objects.filter(empresa = empresa)
    if request.method == 'POST':
        form = ProdConfForm(empresa, request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.empresa = empresa
            producto.save()
            form = ProdConfForm(empresa)
    else:
        form = ProdConfForm(empresa)
    return render(request, 'vista_producto_conf.html', {'form': form, 'productos': productos, 'empresa': empresa })

@login_required
def editar_conf_producto(request, id_prod):
    empresa = request.user.profile.empresa
    productos = Prod_Conf.objects.filter(empresa = empresa)
    try:
        producto = Prod_Conf.objects.get(id = id_prod)
    except:
        return redirect('vista_conf_producto')
    if request.method == 'POST':
        form = ProdConfForm( empresa, request.POST, request.FILES, instance = producto)
        if form.is_valid():
            producto = form.save(commit=False)
            if request.POST.get('borrar') == '':
                producto.delete()
            else:
                producto.save()
            return redirect('vista_conf_producto')
    else:
        form = ProdConfForm(empresa, instance = producto)
    return render(request, 'vista_producto_conf.html', {'form': form, 'empresa': empresa, 'productos':productos, 'prod':producto, 'modificacion': 'S'})
