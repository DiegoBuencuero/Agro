from django import forms  
from .forms import BaseForm
from .models import Trazabilidad, agro_Producto, Producto, Especificacion_tipo, Campo, Lote
from .models import Contactos, agro_CategoriaContacto, EstadoLote, Planificacion_cultivo
from datetime import datetime

class TrazabilidadForm(BaseForm):
    def __init__(self, company, *args,**kwargs):
        super (TrazabilidadForm,self ).__init__(*args,**kwargs)
        opciones = []
        prods = agro_Producto.objects.all()
        for prod in prods:
            opciones.append(('A'+str(prod.id), prod.descripcion))
        prods = Producto.objects.filter(empresa = company)
        for prod in prods:
            opciones.append(('U'+str(prod.id), prod.descripcion))
        self.fields['producto'].choices = opciones
        opciones = []
        esp = Especificacion_tipo.objects.all()
        for e in esp:
            opciones.append((e.id, e.nombre))
        self.fields['espec'].choices = opciones
        self.fields['fecha'].widget.attrs['value'] = datetime.now().strftime('%Y-%m-%d')
        self.fields['moneda'].initial = company.moneda.id
    class Meta:
        model = Trazabilidad
        fields = '__all__'
        exclude = ['empresa', 'origen_prod', 'producto_id', 'especificacion', 'perfil', 'id_mov']
        widgets = {
                'fecha': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            }
    producto = forms.ChoiceField()
    espec = forms.ChoiceField()


class ContactoForm(BaseForm):
    class Meta:
        model = Contactos
        fields = '__all__'
        exclude = ['empresa']


class EstadoLoteForm(BaseForm):
    def __init__(self, company, *args,**kwargs):
        super (EstadoLoteForm,self ).__init__(*args,**kwargs)
        self.fields['planificacion'].queryset = Planificacion_cultivo.objects.filter(empresa = company)
    class Meta:
        model = EstadoLote
        fields = '__all__'
        exclude = ['lote', 'estado']
        widgets = {
                'fecha_desde': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
                'fecha_hasta': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            }
