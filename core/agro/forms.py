from django import forms  
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User  
from django.forms import ModelForm
from .models import Pais, Profile, Campo, Lote, Producto, Tipo, Rubro, CostoProd, CostoProdo, agro_Producto, Especificacion_tipo
from .models import Campana, Planificacion_cultivo, Planificacion_lote, Planificacion_etapas
from .models import Apli_costo_etapa
from string import Template

    
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
        fields = ['nombre', 'descripcion', 'image', 'observaciones']

class LoteForm(BaseForm):
    def __init__(self,company,*args,**kwargs):
        super (LoteForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['campo'].queryset = Campo.objects.filter(empresa=company)

    class Meta:
        model = Lote
        fields = ['campo', 'nombre', 'image', 'ha_totales', 'ha_productivas']


class ProductoForm(BaseForm):
    def __init__(self,company,*args,**kwargs):
        super (ProductoForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['tipo'].queryset = Tipo.objects.filter(empresa=company)
        self.fields['rubro'].queryset = Rubro.objects.filter(empresa=company)
    class Meta:
        model = Producto
        fields = '__all__'
        exclude = ['empresa', 'add_date']

class TipoProdForm(BaseForm):
    class Meta:
        model = Tipo
        fields = '__all__'
        exclude = ['empresa', ]

class RubroProdForm(BaseForm):
    class Meta:
        model = Rubro
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



class PlanificacionEtapaForm(BaseForm):
    def __init__(self,company,*args,**kwargs):
        super (PlanificacionEtapaForm,self ).__init__(*args,**kwargs) # populates the post
    class Meta:
        model = Planificacion_etapas
        fields = '__all__'
        exclude = ['empresa', 'planificacion']


