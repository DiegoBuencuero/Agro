from django import forms  
from .forms import BaseForm
from .models import Trazabilidad, agro_Producto, Producto, Especificacion_tipo, Campo, Lote


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
        model = Trazabilidad
        fields = '__all__'
        exclude = ['empresa','lote', 'origen_prod', 'producto_id', 'especificacion', 'perfil', 'id_mov']
        widgets = {
                'fecha': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            }
    producto = forms.ChoiceField()
    espec = forms.ChoiceField()
    campo = forms.ChoiceField()
    lote_campo = forms.ChoiceField()
