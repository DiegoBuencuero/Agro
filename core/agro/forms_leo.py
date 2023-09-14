from django import forms  
from .forms import BaseForm
from .models import TrazaLote, agro_Producto, Producto, Especificacion_tipo, RubroProd
from .models import Contactos, EstadoLote, Planificacion_cultivo
from .models import Prod_Conf, TrazaLote, TrazaLoteItem
from datetime import datetime
from django.forms import inlineformset_factory

class TrazabilidadForm(BaseForm):
    def __init__(self, company, *args,**kwargs):
        super (TrazabilidadForm,self ).__init__(*args,**kwargs)
        self.fields['fecha'].widget.attrs['value'] = datetime.now().strftime('%Y-%m-%d')
    class Meta:
        model = TrazaLote
        fields = '__all__'
        exclude = ['empresa', 'perfil']
        widgets = {
                'fecha': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            }

TrazaLoteItemFormSet = inlineformset_factory(TrazaLote, TrazaLoteItem, fields='__all__', extra=1)

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



class ProdConfForm(BaseForm):
    def __init__(self, company, *args,**kwargs):
        super (ProdConfForm,self ).__init__(*args,**kwargs)
        self.fields['rubro'].queryset = RubroProd.objects.filter(empresa = company)
    class Meta:
        model = Prod_Conf
        fields = '__all__'
        exclude = ['empresa']


