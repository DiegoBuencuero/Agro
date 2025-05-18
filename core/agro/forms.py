from django import forms  
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User  
from django.forms import ModelForm
from .models import Pais, Profile, Campo, Lote, Producto, Tipo, RubroProd, CostoProd, CostoProdo, agro_Producto, Especificacion_tipo
from .models import Campana, Planificacion_cultivo, Planificacion_lote, Planificacion_etapas
from .models import Campana, Planificacion_cultivo, Planificacion_lote, Planificacion_etapas, Com, Num
from .models import Deposito, RegistroLluvia, Prod, agro_Etapa
from string import Template
from datetime import datetime
from django.utils.translation import gettext_lazy as _
    
class SignupForm(UserCreationForm):  
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password confirmation'})        
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Email'})        
        self.fields['direccion1'].widget = forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Direccion 1'})        
        self.fields['direccion2'].widget = forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Direccion 2'})        
        self.fields['nombre_empresa'].widget = forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Nombre de la empresa'})        
        self.fields['razon_social'].widget = forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Razon social'})        
        self.fields['cuit'].widget = forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'CUIT'})        
        self.fields['telefono'].widget = forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Telefono'})        
        self.fields['celular'].widget = forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Celular'})        
    email = forms.EmailField(max_length=200, help_text='Required')  
    pais = forms.ModelChoiceField(queryset=Pais.objects.all(), empty_label='Seleccione pais', help_text='Required')
    observaciones = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Observaciones. Indiquenos todo lo que crea necesario para completar su perfil', 'rows': 5}))
    direccion1 = forms.CharField(max_length=100)
    direccion2 = forms.CharField(max_length=100)
    nombre_empresa = forms.CharField(max_length=100)
    razon_social = forms.CharField(max_length=100)
    cuit = forms.CharField(max_length=50)
    telefono = forms.CharField(max_length=30)
    celular = forms.CharField(max_length=30)
    
    class Meta:  
        model = User  
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')  
        widgets = {
            'username': forms.TextInput({'placeholder': 'User Name'}),
            'first_name': forms.TextInput({'placeholder': 'First Name'}),
            'last_name': forms.TextInput({'placeholder': 'Last Name'}),
        }

class BaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class SimpleForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SimpleForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-lg'
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

class BaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class PersonalInfoForm(BaseForm):
    class Meta:
        model = Profile
        fields = ['fecha_nacimiento', 'image', 'direccion', 'direccion2', 'pais', 'provincia', 'ciudad', 'cp', 'telefono', 'celular', 
                  'nacionalidad', 'tipodoc','documento', 'genero']
        widgets = {
                'fecha_nacimiento': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            }
    apellido = forms.CharField(max_length=150)
    nombre = forms.CharField(max_length=150)

class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(MyPasswordChangeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class CampoForm(BaseForm):
    class Meta:
        model = Campo
        fields = ['nombre', 'ciudad', 'descripcion', 'image', 'observaciones']

class LoteForm(BaseForm):
    def __init__(self,company,*args,**kwargs):
        super (LoteForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['campo'].queryset = Campo.objects.filter(empresa=company)

    class Meta:
        model = Lote
        fields = ['campo', 'nombre', 'image', 'ha_totales', 'ha_productivas']

class ProductoForm(BaseForm):
    def __init__(self,*args,**kwargs):
        super (ProductoForm,self ).__init__(*args,**kwargs) # populates the post
    class Meta:
        model = Prod
        fields = '__all__'
        exclude = [ 'add_date']

class TipoProdForm(BaseForm):
    class Meta:
        model = Tipo
        fields = '__all__'
        exclude = ['empresa', ]

class RubroProdForm(BaseForm):
    class Meta:
        model = RubroProd
        fields = '__all__'
        exclude = ['empresa', ]        

class CostoProdForm(BaseForm):
    class Meta:
        model = CostoProd
        fields = '__all__'
        exclude = ['empresa', ]
        widgets = {
                'fecha': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            }

class CostoProd_o_Form(BaseForm):
    def __init__(self,*args,**kwargs):
        super (CostoProd_o_Form,self ).__init__(*args,**kwargs) # populates the post
        opciones = []
        prods = agro_Producto.objects.all()
        for prod in prods:
            opciones.append(('A'+str(prod.id), prod.descripcion))
        prods = Producto.objects.all()
        for prod in prods:
            opciones.append(('U'+str(prod.id), prod.descripcion))
        self.fields['producto'].choices = opciones
        opciones = []
        esp = Especificacion_tipo.objects.all()
        for e in esp:
            opciones.append((e.id, e.nombre))
        self.fields['espec'].choices = opciones
    class Meta:
        model = CostoProdo
        fields = '__all__'
        exclude = ['empresa', 'costo_prod', 'origen', 'especificacion']
        widgets = {
                'fecha': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            }
    producto = forms.ChoiceField()
    espec = forms.ChoiceField()
    
class CampanaForm(BaseForm):
    class Meta:
        model = Campana
        fields = '__all__'
        exclude = ['empresa']
        widgets = {
                'fecha_desde': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
                'fecha_hasta': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            }

class PlanificacionCultivoForm(BaseForm):
    def __init__(self,*args,**kwargs):
        super (PlanificacionCultivoForm,self ).__init__(*args,**kwargs)
        self.fields['costo'].required = True
    class Meta:
        model = Planificacion_cultivo
        fields = '__all__'
        exclude = ['empresa']
        widgets = {
                'fecha_plani': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
                'fecha_desde': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
                'fecha_hasta': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            }

class PlanificacionLoteForm(BaseForm):
    def __init__(self,company,*args,**kwargs):
        super (PlanificacionLoteForm,self ).__init__(*args,**kwargs) # populates the post
        opciones = []
        campos = Campo.objects.filter(empresa = company)
        for e in campos:
            opciones.append((e.id, e.nombre))
        self.fields['campo'].choices = opciones
        lotes = Lote.objects.filter(campo__in = campos)
        opciones = []
        for l in lotes:
            opciones.append((l.id, l.nombre))
        self.fields['lote_campo'].choices = opciones
    class Meta:
        model = Planificacion_lote
        fields = '__all__'
        exclude = ['empresa', 'planificacion', 'lote']
    campo = forms.ChoiceField()
    lote_campo = forms.ChoiceField()

class FormAsignacionEtapaCosto(forms.Form):
    def __init__(self,*args,**kwargs):
        super (FormAsignacionEtapaCosto,self ).__init__(*args,**kwargs) # populates the post
        opciones = []
        etapas = agro_Etapa.objects.all()
        for e in etapas:
            opciones.append((e.id, e.nombre))
        self.fields['etapa'].choices = opciones
    etapa = forms.ChoiceField()
    cantidad = forms.IntegerField()
    identificador = forms.CharField(widget=forms.HiddenInput())

class ComprobantesForm(BaseForm):
    class Meta:
        model = Com
        fields = '__all__'
        exclude = ['empresa']

class NumeradorForm(BaseForm):
    class Meta:
        model = Num
        fields = '__all__'
        exclude = ['empresa']

class DepositoForm(BaseForm):
    class Meta:
        model = Deposito
        fields = '__all__'
        exclude = ['empresa']

class RegLluviaForm(BaseForm):
    class Meta:
        model =  RegistroLluvia
        fields = '__all__'
        exclude = ['empresa']

class RegLluviaCargaForm(forms.Form):
    def __init__(self, company, *args, **kwargs):
        super(RegLluviaCargaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['campo'].queryset = Campo.objects.filter(empresa=company)
        anio_actual = datetime.now().year
        tablita_anios = [(anio_actual -2, anio_actual -2), (anio_actual - 1, anio_actual - 1), (anio_actual, anio_actual)]
        self.fields['anio'].choices = tablita_anios

    campo = forms.ModelChoiceField(queryset=Campo.objects.all(), empty_label='Seleccione campo', help_text='Required')
    anio = forms.ChoiceField()

#  FORMS NUEVOS


class UploadArchivoForm(forms.Form):
    campo = forms.ModelChoiceField(
        queryset=Campo.objects.all(),
        required=True,
        label=_("Campo"),
        empty_label=_("Seleccione campo")
    )
    lote = forms.ModelChoiceField(
        queryset=Lote.objects.none(),
        required=True,
        label=_("Lote"),
        empty_label=_("Seleccione lote")
    )
    nombre = forms.CharField(
        max_length=100,
        required=True,
        label=_("Nombre del archivo")
    )
    dummy_archivos = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, empresa, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['campo'].queryset = Campo.objects.filter(empresa=empresa)

        if self.data.get('campo'):
            try:
                campo_id = int(self.data.get('campo'))
                self.fields['lote'].queryset = Lote.objects.filter(campo_id=campo_id)
            except (ValueError, TypeError):
                self.fields['lote'].queryset = Lote.objects.none()
        else:
            campos = Campo.objects.filter(empresa=empresa)
            if campos.count() == 1:
                campo_unico = campos.first()
                self.fields['campo'].initial = campo_unico
                self.fields['lote'].queryset = Lote.objects.filter(campo=campo_unico)
            else:
                self.fields['lote'].queryset = Lote.objects.none()
