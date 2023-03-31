from django.contrib import admin
from .models import Profile, Pais, Provincia, Ciudad, Tipodoc, Nacionalidad, Empresa, Genero, Campo
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
