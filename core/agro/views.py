from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.core.mail import EmailMessage  
from django.utils.encoding import force_bytes, force_str  
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from .tokens import account_activation_token  
from .models import Empresa, Campo, Lote, Producto, Tipo, Rubro,agro_CostoProd, agro_CostoProdo, CostoProd, CostoProdo, agro_Producto, Especificacion_tipo
from .models import Campana, Planificacion_cultivo, Planificacion_lote, Planificacion_etapas
from .models import Apli_costo_etapa
from .forms import PersonalInfoForm, MyPasswordChangeForm, CampoForm, LoteForm, ProductoForm, TipoProdForm, RubroProdForm, CostoProdForm
from .forms import CostoProd_o_Form, CampanaForm, PlanificacionCultivoForm, PlanificacionLoteForm, PlanificacionEtapaForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from operator import itemgetter
# Create your views here.
@login_required
def home(request):
    if request.user.profile.ciudad is None:
        ubicacion = 'Pinamar'
    else:
        ubicacion = request.user.profile.ciudad.nombre
    return render(request, 'index.html', {'ubicacion': ubicacion})

@login_required
def personal_details(request):
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, request.FILES, instance = request.user.profile)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.user.first_name = form.cleaned_data['nombre']
            perfil.user.last_name = form.cleaned_data['apellido']
            perfil.save()
            perfil.user.save()
            return redirect('/')
        else:
            messages.error(request, form.errors.as_data() )
            return render(request, 'personal_details.html', {'form': form})
    else:
        perfil = request.user.profile
        form = PersonalInfoForm(instance = perfil, initial={'apellido': request.user.last_name, 'nombre': request.user.first_name})
        return render(request, 'personal_details.html', {'form': form})





def login_page(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request,'login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                return redirect('/')
        
        # form is not valid or user is not authenticated
        messages.error(request,'Invalid username or password')
        return render(request,'login.html',{'form': form})


##Nuevo para loguear con google

def signup(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            user.profile.direccion1 = form.cleaned_data['direccion1']
            user.profile.direccion2 = form.cleaned_data['direccion1']
            user.profile.pais = form.cleaned_data['pais']
            user.profile.telefono = form.cleaned_data['telefono']
            user.profile.celular = form.cleaned_data['celular']
            empresa = Empresa(nombre = form.cleaned_data['nombre_empresa'], razon_social = form.cleaned_data['razon_social'], cuit = form.cleaned_data['cuit'])
            empresa.save()
            user.profile.empresa = empresa
            user.save()
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = SignupForm()  
    return render(request, 'register.html', {'form': form})  


def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')



@login_required
def ChangePassword(request):
   form = MyPasswordChangeForm(user=request.user, data=request.POST or None)
   if form.is_valid():
     form.save()
     update_session_auth_hash(request, form.user)
     return render(request, 'password_confirm.html', {})
   return render(request, 'password.html', {'form': form})




@login_required
def vista_campos(request):
    campos = Campo.objects.filter(empresa = request.user.profile.empresa)
    empresa = request.user.profile.empresa
    if request.method == 'POST':
        form = CampoForm(request.POST, request.FILES)
        if form.is_valid():
            campo = form.save(commit=False)
            campo.empresa = empresa
            campo.save()
            form = CampoForm()
    else:
        form = CampoForm()
    return render(request, 'vista_campo.html', {'form': form, 'campos': campos, 'empresa': empresa })


@login_required
def editar_campos(request, id_campo):
    campos = Campo.objects.filter(empresa = request.user.profile.empresa)
    try:
        campo = Campo.objects.get(id = id_campo)
    except:
        return redirect('/01')
    empresa = request.user.profile.empresa
    if campo.empresa ==empresa:
        if request.method == 'POST':
            form = CampoForm(request.POST, request.FILES, instance = campo)
            if form.is_valid():
                campo = form.save(commit=False)
                if request.POST.get('borrar') == '':
                    campo.delete()
                else:
                    campo.empresa = empresa
                    campo.save()
                return redirect('/01')
            else:
                messages.error(request, form.errors.as_data() )
        else:
            form = CampoForm(instance = campo)
        return render(request, 'vista_campo.html', {'form': form, 'campos': campos, 'empresa': empresa, 'modificacion': 'S'})
    else:
        return redirect('/01')
    

@login_required
def vista_lotes(request):
    campos = Campo.objects.filter(empresa = request.user.profile.empresa)
    lotes = Lote.objects.filter(campo__in = campos)
    empresa = request.user.profile.empresa
    if request.method == 'POST':
        form = LoteForm(empresa, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = LoteForm(empresa)
    else:
        form = LoteForm(empresa)
    return render(request, 'vista_lote.html', {'form': form, 'campos': campos, 'lotes':lotes, 'empresa':empresa })




@login_required
def editar_lote(request, id_lote):
    campos = Campo.objects.filter(empresa = request.user.profile.empresa)
    lotes = Lote.objects.filter(campo__in = campos)
    try:
        lote = Lote.objects.get(id = id_lote)
    except:
        return redirect('/0101')
    empresa = request.user.profile.empresa
    if lote.campo.empresa == empresa:
        if request.method == 'POST':
            form = LoteForm(empresa, request.POST, request.FILES, instance = lote)
            if form.is_valid():
                lote = form.save(commit=False)
                if request.POST.get('borrar') == '':
                    lote.delete()
                else:
                    lote.save()
                return redirect('/0101')
        else:
            form = LoteForm(empresa, instance = lote)
        return render(request, 'vista_lote.html', {'form': form, 'empresa': empresa, 'lotes':lotes, 'registro_lote':lote, 'modificacion': 'S'})
    else:
        return redirect('/0101')


@login_required
def vista_tipo_producto(request):
    tipos = Tipo.objects.filter(empresa = request.user.profile.empresa)
    empresa = request.user.profile.empresa
    if request.method == 'POST':
        form = TipoProdForm(request.POST)
        if form.is_valid():
            tipo = form.save(commit=False)
            tipo.empresa = empresa
            tipo.save()
            form = TipoProdForm()
        else:
            print(form.errors.as_data())
    else:
        form = TipoProdForm()
    return render(request, 'vista_tipo.html', {'form': form, 'tipos': tipos, 'empresa': empresa })

@login_required
def editar_tipo_producto(request, id_tipo):
    tipos = Tipo.objects.filter(empresa = request.user.profile.empresa)
    try:
        tipo = Tipo.objects.get(id = id_tipo)
    except:
        return redirect('vista_tipo_producto')
    empresa = request.user.profile.empresa
    if tipo.empresa == empresa:
        if request.method == 'POST':
            form = TipoProdForm(request.POST, instance = tipo)
            if form.is_valid():
                tipo = form.save(commit=False)
                if request.POST.get('borrar') == '':
                    tipo.delete()
                else:
                    tipo.save()
                return redirect('vista_tipo_producto')
        else:
            form = TipoProdForm(instance = tipo)
        return render(request, 'vista_tipo.html', {'form': form, 'empresa': empresa, 'tipos':tipos, 'modificacion': 'S'})
    else:
        return redirect('vista_tipo_producto')



@login_required
def vista_rubro_producto(request):
    rubros = Rubro.objects.filter(empresa = request.user.profile.empresa)
    empresa = request.user.profile.empresa
    if request.method == 'POST':
        form = RubroProdForm(request.POST)
        if form.is_valid():
            rubro = form.save(commit=False)
            rubro.empresa = empresa
            rubro.save()
            form = RubroProdForm()
    else:
        form = RubroProdForm()
    return render(request, 'vista_rubro.html', {'form': form, 'rubros': rubros, 'empresa': empresa })

@login_required
def editar_rubro_producto(request, id_rubro):
    rubros = Rubro.objects.filter(empresa = request.user.profile.empresa)
    try:
        rubro = Rubro.objects.get(id = id_rubro)
    except:
        return redirect('vista_rubro_producto')
    empresa = request.user.profile.empresa
    if rubro.empresa == empresa:
        if request.method == 'POST':
            form = RubroProdForm(request.POST, instance = rubro)
            if form.is_valid():
                rubro = form.save(commit=False)
                if request.POST.get('borrar') == '':
                    rubro.delete()
                else:
                    rubro.save()
                return redirect('vista_rubro_producto')
        else:
            form = RubroProdForm(instance = rubro)
        return render(request, 'vista_rubro.html', {'form': form, 'empresa': empresa, 'rubros':rubros, 'modificacion': 'S'})
    else:
        return redirect('vista_rubro_producto')



@login_required
def vista_producto(request):
    productos = Producto.objects.filter(empresa = request.user.profile.empresa)
    empresa = request.user.profile.empresa
    if request.method == 'POST':
        form = ProductoForm(empresa, request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.empresa = empresa
            producto.save()
            form = ProductoForm(empresa)
        else:
            print(form.errors.as_data)
    else:
        form = ProductoForm(empresa)
    return render(request, 'vista_producto.html', {'form': form, 'productos': productos, 'empresa': empresa })


@login_required
def editar_producto(request, id_prod):
    productos = Producto.objects.filter(empresa = request.user.profile.empresa)
    try:
        producto = Producto.objects.get(id = id_prod)
    except:
        return redirect('vista_producto')
    empresa = request.user.profile.empresa
    if producto.empresa == empresa:
        if request.method == 'POST':
            form = ProductoForm(empresa, request.POST, request.FILES, instance = producto)
            if form.is_valid():
                producto = form.save(commit=False)
                if request.POST.get('borrar') == '':
                    producto.delete()
                else:
                    producto.save()
                return redirect('vista_producto')
        else:
            form = ProductoForm(empresa, instance = producto)
        return render(request, 'vista_producto.html', {'form': form, 'empresa': empresa, 'productos':productos, 'prod':producto, 'modificacion': 'S'})
    else:
        return redirect('vista_producto')



@login_required
def vista_costo_prod(request):
    costos = CostoProd.objects.filter(empresa = request.user.profile.empresa)
    empresa = request.user.profile.empresa
    if request.method == 'POST':
        form = CostoProdForm(request.POST)
        if form.is_valid():
            costo = form.save(commit=False)
            costo.empresa = empresa
            costo.save()
            form = CostoProdForm()
    else:
        form = CostoProdForm()
    return render(request, 'vista_costo_prod.html', {'costos': costos, 'form': form, 'empresa': empresa })


def get_lista_costo(costo):
    costo_o = CostoProdo.objects.filter(costo_prod = costo)
    lista_costo = []
    totalabc = 0
    totalabcd = 0
    total = 0
    for co in costo_o:
        if co.origen == 'A':
            prod_descr = agro_Producto.objects.get(pk = co.producto_id)
        else:
            prod_descr = Producto.objects.get(pk = co.producto_id)
        if co.um.abreviado == '%':
            total = 0
        else:
            total = co.cantidad * co.precio_unitario
        if prod_descr.agro_rubro.letra in ('A','B','C'):
            totalabc += co.cantidad * co.precio_unitario
        if prod_descr.agro_rubro.letra in ('A','B','C', 'D'):
            totalabcd += co.cantidad * co.precio_unitario
        total = co.cantidad * co.precio_unitario
        linea = {
            'id': co.id,
            'orden': co.orden, 
            'prod_name': prod_descr, 
            'especificacion': co.especificacion, 
            'um':co.um, 
            'cantidad': co.cantidad, 
            'precio_unitario': co.precio_unitario,
            'moneda': co.moneda,
            'cotizacion': co.cotizacion,
            'total': total,
            'rubro_orden': prod_descr.agro_rubro.orden,
            'letra': prod_descr.agro_rubro.letra,
            'total_anterior': 0,
        }
        lista_costo.append(linea)
    if len(lista_costo) > 0:
        lista_costo.sort(key=(itemgetter('rubro_orden', 'orden')))
        totrubro = 0
        rubroant = lista_costo[0]['rubro_orden']
        total = 0
        for l in lista_costo:
            if l['um'].abreviado == '%':
                if l['precio_unitario'] == 1:
                    porcentaje = totalabc * l['cantidad'] / 100
                    l['total'] = porcentaje
                    if l['letra'] == 'D':
                        totalabcd += porcentaje
                    importe = porcentaje
                elif l['precio_unitario'] == 2:
                    l['total'] = totalabcd * l['cantidad'] / 100
                    importe = totalabcd * l['cantidad'] / 100
            else:
                importe = l['total']
            if rubroant != l['rubro_orden']:
                l['total_anterior'] = totrubro
                totrubro = importe
                rubroant = l['rubro_orden']
            else:
                totrubro += importe
            total += importe
        return lista_costo, total
    else:
        return lista_costo, 0

@login_required
def editar_costo_prod(request, id_costo):
    try:
        costo = CostoProd.objects.get(id = id_costo)
    except:
        return redirect('vista_costo_prod')
    lista_historica = agro_CostoProd.objects.filter(cultivo = costo.cultivo).filter(sistema_cultivo = costo.sistema_cultivo) 
    lista_costo, total = get_lista_costo(costo)
    empresa = request.user.profile.empresa
    precio_dia = 144
    calculo = total / precio_dia
    if costo.empresa == empresa:
        if request.method == 'POST':
            form = CostoProd_o_Form(request.POST)
            if form.is_valid():
                try:
                    especificacion = Especificacion_tipo.objects.get(id = form.cleaned_data['espec'])
                except:
                    especificacion = None
                renglon = form.save(commit=False)
                renglon.empresa = empresa
                renglon.costo_prod = costo
                renglon.origen = form.cleaned_data['producto'][0:1]
                renglon.producto_id = int(form.cleaned_data['producto'][1:])
                renglon.especificacion = especificacion
                renglon.save()
                form = CostoProd_o_Form()
                lista_costo, total = get_lista_costo(costo)
        else:
            form = CostoProd_o_Form()
        return render(request, 'editar_costo_prod.html', {'form': form, 'total': total, 'precio_dia':precio_dia, 'calculo':calculo, 'empresa': empresa, 'costo_os':lista_costo, 'costo':costo, 'lista_historica':lista_historica})
    else:
        return redirect('vista_costo_prod')


def ajax_get_costo(request):
    costos = agro_CostoProdo.objects.all()
    respuesta = []
    for costo in costos:
        linea = {'o': costo.orden}
        respuesta.append(linea)
    data = {'data': respuesta}
    return JsonResponse(data)

def ajax_get_espec(request):
    prod_param = request.GET.get('producto')
    origen = prod_param[0:1]
    id_prod = prod_param[1:]
    if origen == 'A':
        producto = agro_Producto.objects.get(id = id_prod)
    else:
        producto = Producto.objects.get(id = id_prod)
    tipo = producto.agro_tipo
    especificaciones = Especificacion_tipo.objects.filter(agro_tipo = tipo)
    respuesta = []
    for e in especificaciones:
        linea = {'id': e.id, 'nombre': e.nombre}
        respuesta.append(linea)
    data = {'data': respuesta}
    return JsonResponse(data)



@login_required
def load_costo_agro(request, id_costo, id_agro_costo):
    try:
        costo = CostoProd.objects.get(id = id_costo)
        agro_costo = agro_CostoProd.objects.get(pk=id_agro_costo)
        agro_costos = agro_CostoProdo.objects.filter(costo_prod = agro_costo)
    except:
        return redirect('vista_costo_prod')

    CostoProdo.objects.filter(costo_prod = costo).delete()
    o = 1
    for costoo in agro_costos:
        nuevo = CostoProdo(
            empresa = request.user.profile.empresa, 
            orden = costoo.orden, 
            costo_prod = costo, 
            producto_id = costoo.agro_producto.id,
            origen = 'A',
            um = costoo.um,
            cantidad = costoo.cantidad,
            precio_unitario = costoo.precio_unitario,
            moneda = costoo.moneda,
            cotizacion = costoo.cotizacion,
            especificacion = costoo.especificacion,
        )
        nuevo.save()
    return redirect('/03/' + str(id_costo))




@login_required
def editar_costo_prod_linea(request, id_costoo):
    try:
        costo = CostoProdo.objects.get(id = id_costoo)
    except:
        return redirect('vista_costo_prod')
    empresa = request.user.profile.empresa
    if costo.empresa == empresa:
        if request.method == 'POST':
            form = CostoProd_o_Form(request.POST, instance= costo)
            if form.is_valid():
                try:
                    especificacion = Especificacion_tipo.objects.get(id = form.cleaned_data['espec'])
                except:
                    especificacion = None
                renglon = form.save(commit=False)
                if request.POST.get('borrar') == '':
                    renglon.delete()
                else:
                    renglon.origen = form.cleaned_data['producto'][0:1]
                    renglon.producto_id = int(form.cleaned_data['producto'][1:])
                    renglon.especificacion = especificacion
                    renglon.save()
                return redirect('/03/' + str(costo.costo_prod.id))
        else:
            initial_data = {
                'producto': costo.origen + str(costo.producto_id),
                'espec': costo.especificacion.id
            }
            form = CostoProd_o_Form(instance = costo, initial = initial_data)
        return render(request, 'editar_costo_prod_linea.html', {'form': form, 'costoo': costo})
    else:
        return redirect('vista_costo_prod')



@login_required
def vista_campana(request):
    campanas = Campana.objects.filter(empresa = request.user.profile.empresa)
    empresa = request.user.profile.empresa
    if request.method == 'POST':
        form = CampanaForm(request.POST)
        if form.is_valid():
            campana = form.save(commit=False)
            campana.empresa = empresa
            campana.save()
            form = CampanaForm()
    else:
        form = CampanaForm()
    return render(request, 'vista_campana.html', {'campanas':campanas, 'form': form, 'empresa': empresa })

@login_required
def editar_campana(request, id_campana):
    campanas = Campana.objects.filter(empresa = request.user.profile.empresa)
    try:
        camp = Campana.objects.get(id = id_campana)
    except:
        return redirect('vista_campana')
    empresa = request.user.profile.empresa
    if camp.empresa == empresa:
        if request.method == 'POST':
            form = CampanaForm(request.POST, instance = camp)
            if form.is_valid():
                campana = form.save(commit=False)
                if request.POST.get('borrar') == '':
                    campana.delete()
                else:
                    campana.save()
                return redirect('vista_campana')
        else:
            form = CampanaForm(instance = camp)
        return render(request, 'vista_campana.html', {'form': form, 'empresa': empresa, 'campanas':campanas, 'modificacion': 'S'})
    else:
        return redirect('vista_campana')


@login_required
def vista_planificacion(request):
    planificaciones = Planificacion_cultivo.objects.filter(empresa = request.user.profile.empresa)
    empresa = request.user.profile.empresa
    if request.method == 'POST':
        form = PlanificacionCultivoForm(request.POST)
        if form.is_valid():
            plani = form.save(commit=False)
            plani.empresa = empresa
            plani.save()
            form = PlanificacionCultivoForm()
    else:
        form = PlanificacionCultivoForm()
    return render(request, 'vista_plani.html', {'planis': planificaciones, 'form': form, 'empresa': empresa })


@login_required
def editar_planificacion(request, id_plani):
    planificaciones = Planificacion_cultivo.objects.filter(empresa = request.user.profile.empresa)
    try:
        plani =Planificacion_cultivo.objects.get(id = id_plani)
    except:
        return redirect('vista_planificacion')
    empresa = request.user.profile.empresa
    if plani.empresa == empresa:
        if request.method == 'POST':
            form = PlanificacionCultivoForm(request.POST, instance = plani)
            if form.is_valid():
                plani = form.save(commit=False)
                if request.POST.get('borrar') == '':
                    plani.delete()
                else:
                    plani.save()
                return redirect('vista_planificacion')
        else:
            form = PlanificacionCultivoForm(instance = plani)
        return render(request, 'vista_plani.html', {'form': form, 'empresa': empresa, 'planis':planificaciones, 'modificacion': 'S'})
    else:
        return redirect('vista_planificacion')



@login_required
def vista_planificacion_lote(request, id_plani):
    try:
        planificacion =Planificacion_cultivo.objects.get(id = id_plani)
    except:
        return redirect('vista_planificacion')
    lotes = Planificacion_lote.objects.filter(planificacion = planificacion)
    empresa = request.user.profile.empresa
    if planificacion.empresa == empresa:
        if request.method == 'POST':
            form = PlanificacionLoteForm(empresa, request.POST)
            if form.is_valid():
                plani = form.save(commit=False)
                plani.empresa = empresa
                try:
                    new_lote = Lote.objects.get(id = form.cleaned_data['lote_campo'])
                    check_lote = Planificacion_lote.objects.filter(empresa = empresa).filter(planificacion = planificacion).filter(lote = new_lote)
                    if len(check_lote) > 0:
                        form.add_error('lote_campo', 'Este lote ya existe en esta planificacion')
                    else:
                        plani.lote = new_lote
                        plani.planificacion = planificacion
                        plani.save()
                        form = PlanificacionLoteForm(empresa)
                except:
                    form.add_error('lote_campo', 'Error inesperado, el lote no existe')
        else:
            form = PlanificacionLoteForm(empresa)
        return render(request, 'vista_planificacion_lote.html', {'lotes': lotes, 'planificacion':planificacion, 'form': form, 'cancel_url':'/05-1/'+str(id_plani) })
    else:
        return redirect('vista_planificacion')



def ajax_get_lote(request):
    campo_id = request.GET.get('campo')
    campo = Campo.objects.get(id = campo_id)
    lotes = Lote.objects.filter(campo = campo)
    respuesta = []
    for e in lotes:
        linea = {'id': e.id, 'nombre': e.nombre}
        respuesta.append(linea)
    data = {'data': respuesta}
    return JsonResponse(data)



@login_required
def vista_lote_eliminar(request, id_plani, id_lote):
    try:
        planificacion =Planificacion_cultivo.objects.get(id = id_plani)
        lote = Planificacion_lote.objects.get(id = id_lote)
        lote.delete()
        return redirect('/05-1/' + str(id_plani))
    except:
        return redirect('vista_planificacion')

def get_producto(origen, id):
    if origen == 'A':
        producto = agro_Producto.objects.get(id = id)
    else:
        producto = Producto.objects.get(id = id)
    return producto

def load_etapas(planificacion):
    costo = planificacion.costo
    items = CostoProdo.objects.filter(costo_prod = costo)
    for item in items:
        producto = get_producto(item.origen, item.producto_id)
        etapas = producto.agro_tipo.etapas.all()
        if len(etapas) == 1:
            etapa = etapas[0]
            lotes = Planificacion_lote.objects.filter(planificacion = planificacion)
            for lote in lotes:
                plani_etapa = Planificacion_etapas(
                    empresa = planificacion.empresa,
                    planificacion = planificacion,
                    lote = lote.lote,
                    etapa = etapa,
                    producto_id = item.producto_id,
                    origen = item.origen,
                    um = item.um,
                    cantidad = item.cantidad * lote.lote.ha_productivas,
                    precio_unitario = item.precio_unitario,
                    moneda = item.moneda,
                    cotizacion = item.cotizacion,
                    especificacion = item.especificacion  
                    )
                plani_etapa.save()
                apli = Apli_costo_etapa(plani_etapa = plani_etapa, plani_costoo = item)
                apli.save()
        

@login_required
def vista_planificacion_etapas(request, id_plani):
    try:
        planificacion =Planificacion_cultivo.objects.get(id = id_plani)
    except:
        return redirect('vista_planificacion')
    etapas = Planificacion_etapas.objects.filter(planificacion = planificacion)
    if len(etapas) == 0:
        load_etapas(planificacion)
        etapas = Planificacion_etapas.objects.filter(planificacion = planificacion)
    etapas_list = []
    for etapa in etapas:
        producto = get_producto(etapa.origen, etapa.producto_id)
        linea = {
            'etapa': etapa.etapa,
            'producto_desc': producto.descripcion,
            'producto_id': producto.id,
            'lote': etapa.lote,
            'cantidad': etapa.cantidad,
            'um': etapa.um,

        }
        etapas_list.append(linea)
    no_asig_list = []
    items = CostoProdo.objects.filter(costo_prod = planificacion.costo)
    for item in items:
        apli = Apli_costo_etapa.objects.filter(plani_costoo = item)
        if len(apli) == 0:
            producto = get_producto(item.origen, item.producto_id)
            linea = {
                'producto_desc': producto.descripcion,
                'producto_id': producto.id,
                'cantidad': item.cantidad
            }
            no_asig_list.append(linea)
    empresa = request.user.profile.empresa
    if planificacion.empresa == empresa:
        if request.method == 'POST':
            form = PlanificacionLoteForm(empresa, request.POST)
            if form.is_valid():
                plani = form.save(commit=False)
                plani.empresa = empresa
                try:
                    new_lote = Lote.objects.get(id = form.cleaned_data['lote_campo'])
                    check_lote = Planificacion_lote.objects.filter(empresa = empresa).filter(planificacion = planificacion).filter(lote = new_lote)
                    if len(check_lote) > 0:
                        form.add_error('lote_campo', 'Este lote ya existe en esta planificacion')
                    else:
                        plani.lote = new_lote
                        plani.planificacion = planificacion
                        plani.save()
                        form = PlanificacionLoteForm(empresa)
                except:
                    form.add_error('lote_campo', 'Error inesperado, el lote no existe')
        else:
            form = PlanificacionEtapaForm(empresa)
        return render(request, 'vista_planificacion_etapas.html', {'etapas': etapas_list, 'noasign':no_asig_list , 'planificacion':planificacion, 'form': form, 'cancel_url':'/05-3/'+str(id_plani) })
    else:
        return redirect('vista_planificacion')

@login_required
def vista_planificacion_etapas_reset(request, id_plani):
    try:
        planificacion =Planificacion_cultivo.objects.get(id = id_plani)
    except:
        return redirect('vista_planificacion')
    if planificacion.empresa != request.user.profile.empresa:
        return redirect('vista_planificacion')
    Planificacion_etapas.objects.filter(planificacion = planificacion).delete()
    load_etapas(planificacion)
    return redirect('/05-3/' + str(id_plani))
