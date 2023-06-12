"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from agro.views import home, login_page, signup, activate, personal_details, ChangePassword, vista_campos, editar_campos, vista_lotes, editar_lote
from agro.views import vista_producto, vista_tipo_producto, editar_producto, editar_tipo_producto, vista_rubro_producto, editar_rubro_producto
from agro.views import vista_costo_prod, editar_costo_prod, ajax_get_costo, load_costo_agro, ajax_get_espec, editar_costo_prod_linea
from agro.views import vista_campana, editar_campana, vista_planificacion, editar_planificacion, vista_planificacion_lote
from agro.views import ajax_get_lote, vista_lote_eliminar, vista_planificacion_etapas, vista_planificacion_etapas_reset
from agro.views import vista_comprobantes, editar_comprobante, vista_numerador, editar_numerador, vista_deposito, editar_deposito
from agro.views import ajax_get_lote, vista_lote_eliminar, vista_planificacion_etapas, vista_lluvia
from django.conf import settings
from django.conf.urls.static import static
from .urls_leo import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login', login_page),
    path('signup/', signup),
    path('activate/<uidb64>/<token>', activate, name='activate'),  
    path("accounts/", include("django.contrib.auth.urls")),
    path("personal-info/", personal_details, name='personal_details'),
    path('password-reset/', ChangePassword, name='password-reset'),
    path('06/', vista_numerador, name='vista_numerador'),
    path('06/<int:id_num>', editar_numerador, name='editar_numerador'),
    path('07/<int:id_com>', editar_comprobante, name='editar_comprobante'),
    path('08/',vista_deposito, name='vista_deposito'),
    path('08/<int:id_depo>', editar_deposito, name='editar_deposito'),
    path('regLluvias/', vista_lluvia, name='vista_lluvia'),
]
urlpatterns += url_leo
# Only add this when we are in debug mode.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    