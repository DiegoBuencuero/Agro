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
from agro.views import vista_comprobantes
from agro.views import ajax_get_lote, vista_lote_eliminar, vista_planificacion_etapas, vista_delete_plani_etapa
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login', login_page),
    path('signup/', signup),
    path('activate/<uidb64>/<token>', activate, name='activate'),  
    path("accounts/", include("django.contrib.auth.urls")),
    path("personal-info/", personal_details, name='personal_details'),
    path('password-reset/', ChangePassword, name='password-reset'),
    path('01/', vista_campos, name='vista_campos'),
    path('01/<int:id_campo>', editar_campos, name='editar_campos'),
    path('0101/', vista_lotes, name='vista_lotes'),
    path('0101/<int:id_lote>', editar_lote, name='editar_lote'),
    path('02/', vista_producto, name='vista_producto'),
    path('02/<int:id_prod>', editar_producto, name='editar_producto'),
    path('02-tipo/', vista_tipo_producto, name='vista_tipo_producto'),
    path('02-tipo/<int:id_tipo>', editar_tipo_producto, name='editar_tipo_producto'),
    path('02-rubro/', vista_rubro_producto, name='vista_rubro_producto'),
    path('02-rubro/<int:id_rubro>', editar_rubro_producto, name='editar_rubro_producto'),
    path('03/', vista_costo_prod, name='vista_costo_prod'),
    path('03/<int:id_costo>', editar_costo_prod, name='editar_costo_prod'),
    path('03-linea/<int:id_costoo>', editar_costo_prod_linea, name='editar_costo_prod_linea'),
    path('03-getcosto', ajax_get_costo, name = 'ajax_get_costo'),
    path('get-prod-espec', ajax_get_espec, name = 'ajax_get_espec'),
    path('03-loadcosto/<int:id_costo>/<int:id_agro_costo>', load_costo_agro, name = 'load_costo_agro'),
    path('04/', vista_campana, name='vista_campana'),
    path('04/<int:id_campana>', editar_campana, name='editar_campana'),
    path('05/', vista_planificacion, name='vista_planificacion'),
    path('05/<int:id_plani>', editar_planificacion, name='editar_planificacion'),
    path('05-1/<int:id_plani>', vista_planificacion_lote, name='vista_planificacion_lote'),
    path('99-getlote', ajax_get_lote, name = 'ajax_get_lote'),
    path('05-2/<int:id_plani>/<int:id_lote>', vista_lote_eliminar, name='vista_lote_eliminar'),
    path('05-3/<int:id_plani>', vista_planificacion_etapas, name='vista_planificacion_etapas'),
    path('05-3-reset/<int:id_plani>', vista_planificacion_etapas_reset, name='vista_planificacion_etapas_reset'),
    path('05-3-unasign/<int:id_etapa>', vista_delete_plani_etapa, name='vista_delete_plani_etapa'),
    path('07/', vista_comprobantes, name='vista_comprobantes'),


]
# Only add this when we are in debug mode.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    