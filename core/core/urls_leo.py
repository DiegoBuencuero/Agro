from django.urls import path
from agro.views import home, login_page, signup, activate, personal_details, ChangePassword, vista_campos, editar_campos, vista_lotes, editar_lote
from agro.views import vista_producto, editar_producto, vista_rubro_producto, editar_rubro_producto
from agro.views import vista_costo_prod, editar_costo_prod, ajax_get_costo, load_costo_agro, ajax_get_espec, editar_costo_prod_linea
from agro.views import vista_campana, editar_campana, vista_planificacion, editar_planificacion, vista_planificacion_lote
from agro.views import ajax_get_lote, vista_lote_eliminar, vista_planificacion_etapas, vista_planificacion_etapas_reset
from agro.views import vista_comprobantes
from agro.views import ajax_get_lote, vista_lote_eliminar, vista_planificacion_etapas
from agro.views_leo import  vista_contactos, editar_contacto
from agro.views_leo import vista_estado_lote, vista_asign_lote, ajax_get_planificacion
from agro.views_leo import vista_lote_trazabilidad, vista_trazabilidad_lote, ajax_get_prods_actividad
from agro.views_leo import vista_conf_producto, editar_conf_producto, vista_resumen_trazabilidad

url_leo = [

    path('01/', vista_campos, name='vista_campos'),
    path('01/<int:id_campo>', editar_campos, name='editar_campos'),
    path('0101/', vista_lotes, name='vista_lotes'),
    path('0101/<int:id_lote>', editar_lote, name='editar_lote'),
    path('02/', vista_producto, name='vista_producto'),
    path('02/<int:id_prod>', editar_producto, name='editar_producto'),
    path('02-conf/', vista_conf_producto, name='vista_conf_producto'),
    path('02-conf/<int:id_prod>', editar_conf_producto, name='editar_conf_producto'),
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
    path('07/', vista_comprobantes, name='vista_comprobantes'),
    path('general/contactos/', vista_contactos, name='vista_contactos'),
    path('general/contacto/<int:id_contacto>', editar_contacto, name='editar_contacto'),
    path('estado-lote', vista_estado_lote, name='vista_estado_lote'),
    path('asign-lote/<int:id_lote>', vista_asign_lote, name='vista_asign_lote'),
    path('statuslote', ajax_get_planificacion, name = 'ajax_get_planificacion'),
    path('add-traza-lote/<int:id_estado>', vista_trazabilidad_lote, name='vista_trazabilidad_lote'),
    path('99-getprods', ajax_get_prods_actividad, name = 'ajax_get_prods_actividad'),
    path('trazabilidad/', vista_lote_trazabilidad, name = 'vista_trazabilidad'),
    path('traza-lote/<int:id_estado>', vista_resumen_trazabilidad, name='vista_resumen_trazabilidad'),

]