from django.contrib import admin
from .models import Profile, Pais, Provincia, Ciudad, Tipodoc, Nacionalidad, Empresa, Genero, Campo, Tipo, Rubro, Cultivo, SistemaCultivo
from .models import Especificacion, UM, Moneda, agro_CostoProd, agro_CostoProdo, agro_Producto, agro_TipoProd, agro_RubroProd, Especificacion_tipo
from .models import CostoProd, CostoProdo, Producto, agro_Etapa, Lote, Planificacion_etapas, Actividad
from .models import Com, Num, RegistroLluvia, agro_CategoriaContacto, EstadoLote, TrazaLote, TrazaLoteItem
from .models import Prod, TipoProd, RubroProd, ClaseProd, ArchivoDato, DatoGeo, ArchivoLote
# Register your models here.

admin.site.register(Profile)
admin.site.register(Pais)
admin.site.register(Provincia)
admin.site.register(Ciudad)
admin.site.register(Tipodoc)
admin.site.register(Nacionalidad)
admin.site.register(Empresa)
admin.site.register(Genero)
admin.site.register(Campo)
admin.site.register(Tipo)
admin.site.register(Rubro)
admin.site.register(Cultivo)
admin.site.register(SistemaCultivo) 
admin.site.register(Especificacion) 
admin.site.register(UM) 
admin.site.register(Moneda) 
admin.site.register(agro_CostoProd) 
admin.site.register(agro_CostoProdo) 
admin.site.register(agro_Producto) 
admin.site.register(agro_TipoProd) 
admin.site.register(agro_RubroProd) 
admin.site.register(Especificacion_tipo) 
admin.site.register(CostoProd) 
admin.site.register(CostoProdo) 
admin.site.register(Producto) 
admin.site.register(agro_Etapa) 
admin.site.register(Lote) 
admin.site.register(Planificacion_etapas)
admin.site.register(Com)
admin.site.register(Num)
admin.site.register(RegistroLluvia)
admin.site.register(agro_CategoriaContacto)
admin.site.register(Actividad)
admin.site.register(EstadoLote)
admin.site.register(TrazaLote)
admin.site.register(TrazaLoteItem)
admin.site.register(Prod)
admin.site.register(RubroProd)
admin.site.register(TipoProd)
admin.site.register(ClaseProd)

@admin.register(ArchivoDato)
class ArchivoDatoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'lote', 'tipo', 'formato', 'usuario', 'archivo']
    search_fields = ['nombre', 'lote__nombre', 'usuario__username']
    list_filter = ['tipo', 'formato', 'lote']
    ordering = ['-id']


@admin.register(DatoGeo)
class DatoGeoAdmin(admin.ModelAdmin):
    list_display = ['id', 'archivo', 'latitud', 'longitud', 'valor', 'unidad', 'tipo']
    search_fields = ['archivo__nombre', 'valor']
    list_filter = ['tipo', 'unidad']
    ordering = ['-id']

admin.site.register(ArchivoLote)