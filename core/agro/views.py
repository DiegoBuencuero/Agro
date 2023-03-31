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
from django.http import HttpResponse  
from django.contrib.auth import get_user_model
from .tokens import account_activation_token  
from .models import Empresa, Campo
from .forms import PersonalInfoForm, MyPasswordChangeForm, CampoForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

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
            messages.error(request, form.errors.as_data() )
    else:
        form = CampoForm()
    return render(request, 'vista_campo.html', {'form': form, 'campos': campos, 'empresa': empresa })


@login_required
def editar_campos(request, id_campo):
    campos = Campo.objects.filter(empresa = request.user.profile.empresa)
    campo = Campo.objects.get(id = id_campo)
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