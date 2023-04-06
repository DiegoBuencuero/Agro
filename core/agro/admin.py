from django.contrib import admin
from .models import Profile, Pais, Provincia, Ciudad, Tipodoc, Nacionalidad, Empresa, Genero, Campo, Tipo, Rubro, Cultivo, SistemaCultivo
from .models import Especificacion, UM, Moneda
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
