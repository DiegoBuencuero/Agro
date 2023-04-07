from django.contrib import admin
from .models import Profile, Pais, Provincia, Ciudad, Tipodoc, Nacionalidad, Empresa, Genero, Campo, Tipo, Rubro, Cultivo, SistemaCultivo
from .models import Especificacion, UM, Moneda, agro_CostoProd, agro_CostoProdo, agro_Producto, agro_TipoProd, agro_RubroProd, Especificacion_tipo
from .models import CostoProd, CostoProdo
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
