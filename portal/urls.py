from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contactanos/', views.contactanos, name='contactanos'),
    path('seguimiento/', views.buscar_seguimiento, name='buscar_seguimiento'),
    path('nuestras-oficinas/', views.nuestras_oficinas, name='nuestras_oficinas'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('intro/', views.intro, name='intro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('recuperar-contrasena/', views.recuperar_contrasena, name='recuperar_contrasena'),
    path('restablecer-contrasena/<str:token>/', views.restablecer_contrasena, name='restablecer_contrasena'),
    
    # Gestión de empleados
    path('empleados/crear/', views.crear_empleado, name='crear_empleado'),
    path('empleados/', views.listar_empleados, name='listar_empleados'),
    path('empleados/<int:id_empleado>/', views.ver_empleado, name='ver_empleado'),
    path('empleados/<int:id_empleado>/editar/', views.editar_empleado, name='editar_empleado'),
    path('empleados/<int:id_empleado>/eliminar/', views.eliminar_empleado, name='eliminar_empleado'),
    path('empleados/<int:id_empleado>/reenviar-credenciales/', views.reenviar_credenciales_empleado, name='reenviar_credenciales_empleado'),
    path('recursos-humanos/direcciones/', views.listar_direcciones, name='listar_direcciones'),
    path('recursos-humanos/direcciones/crear/', views.crear_direccion, name='crear_direccion'),
    path('recursos-humanos/direcciones/<int:iddireccion>/editar/', views.editar_direccion, name='editar_direccion'),
    path('recursos-humanos/direcciones/<int:iddireccion>/estado/', views.cambiar_estado_direccion, name='cambiar_estado_direccion'),
    path('recursos-humanos/departamentos/', views.listar_departamentos, name='listar_departamentos'),
    path('recursos-humanos/departamentos/crear/', views.crear_departamento, name='crear_departamento'),
    path('recursos-humanos/departamentos/<int:iddepartamento>/editar/', views.editar_departamento, name='editar_departamento'),
    path('recursos-humanos/departamentos/<int:iddepartamento>/estado/', views.cambiar_estado_departamento, name='cambiar_estado_departamento'),
    path('recursos-humanos/puestos/', views.listar_puestos, name='listar_puestos'),
    path('recursos-humanos/puestos/crear/', views.crear_puesto, name='crear_puesto'),
    path('recursos-humanos/puestos/<int:idpuesto>/editar/', views.editar_puesto, name='editar_puesto'),
    path('recursos-humanos/puestos/<int:idpuesto>/estado/', views.cambiar_estado_puesto, name='cambiar_estado_puesto'),
    path('recursos-humanos/tipos-contratacion/', views.listar_tipos_contratacion, name='listar_tipos_contratacion'),
    path('recursos-humanos/tipos-contratacion/crear/', views.crear_tipo_contratacion, name='crear_tipo_contratacion'),
    path('recursos-humanos/tipos-contratacion/<int:idtipodecontratacion>/editar/', views.editar_tipo_contratacion, name='editar_tipo_contratacion'),
    path('recursos-humanos/tipos-contratacion/<int:idtipodecontratacion>/estado/', views.cambiar_estado_tipo_contratacion, name='cambiar_estado_tipo_contratacion'),
    
    # Patrimonio
    path('patrimonio/bienes/', views.listar_bienes, name='listar_bienes'),
    path('patrimonio/bienes/crear/', views.crear_bien, name='crear_bien'),
    path('patrimonio/bienes/<int:idbien>/editar/', views.editar_bien, name='editar_bien'),
    path('patrimonio/bienes/<int:idbien>/estado/', views.cambiar_estado_bien, name='cambiar_estado_bien'),
    path('patrimonio/bienes/analizar-excel/', views.analizar_excel_bienes, name='analizar_excel_bienes'),
    path('patrimonio/bienes/importar-excel/', views.importar_bienes_excel, name='importar_bienes_excel'),
    
    # Patrimonio - Catálogos
    path('patrimonio/marcas/', views.listar_marcas, name='listar_marcas'),
    path('patrimonio/marcas/crear/', views.crear_marca, name='crear_marca'),
    path('patrimonio/marcas/<int:idmarca>/editar/', views.editar_marca, name='editar_marca'),
    path('patrimonio/marcas/analizar-excel/', views.analizar_excel_marcas, name='analizar_excel_marcas'),
    path('patrimonio/marcas/importar-excel/', views.importar_marcas_excel, name='importar_marcas_excel'),
    path('patrimonio/marcas/<int:idmarca>/estado/', views.cambiar_estado_marca, name='cambiar_estado_marca'),
    
    path('patrimonio/proveedores/', views.listar_proveedores, name='listar_proveedores'),
    path('patrimonio/proveedores/crear/', views.crear_proveedor, name='crear_proveedor'),
    path('patrimonio/proveedores/<int:idproveedor>/editar/', views.editar_proveedor, name='editar_proveedor'),
    path('patrimonio/proveedores/<int:idproveedor>/estado/', views.cambiar_estado_proveedor, name='cambiar_estado_proveedor'),
    path('patrimonio/proveedores/analizar-excel/', views.analizar_excel_proveedores, name='analizar_excel_proveedores'),
    path('patrimonio/proveedores/importar-excel/', views.importar_proveedores_excel, name='importar_proveedores_excel'),
    
    path('patrimonio/clasificaciones-serap/', views.listar_clasificaciones_serap, name='listar_clasificaciones_serap'),
    path('patrimonio/clasificaciones-serap/crear/', views.crear_clasificacion_serap, name='crear_clasificacion_serap'),
    path('patrimonio/clasificaciones-serap/<int:idclasificacion_serap>/editar/', views.editar_clasificacion_serap, name='editar_clasificacion_serap'),
    path('patrimonio/clasificaciones-serap/<int:idclasificacion_serap>/estado/', views.cambiar_estado_clasificacion_serap, name='cambiar_estado_clasificacion_serap'),
    
    path('patrimonio/clasificaciones-contraloria/', views.listar_clasificaciones_contraloria, name='listar_clasificaciones_contraloria'),
    path('patrimonio/clasificaciones-contraloria/crear/', views.crear_clasificacion_contraloria, name='crear_clasificacion_contraloria'),
    path('patrimonio/clasificaciones-contraloria/<int:idclasificacion_contraloria>/editar/', views.editar_clasificacion_contraloria, name='editar_clasificacion_contraloria'),
    path('patrimonio/clasificaciones-contraloria/<int:idclasificacion_contraloria>/estado/', views.cambiar_estado_clasificacion_contraloria, name='cambiar_estado_clasificacion_contraloria'),
    
    # Resguardos Internos
    path('patrimonio/resguardos/', views.listar_resguardos, name='listar_resguardos'),
    path('patrimonio/resguardos/asignar/', views.asignar_resguardo, name='asignar_resguardo'),
    path('patrimonio/resguardos/<int:idresguardo>/devolver/', views.devolver_resguardo, name='devolver_resguardo'),
    path('patrimonio/resguardos/<int:idresguardo>/descargar-oficio/', views.descargar_oficio_resguardo, name='descargar_oficio_resguardo'),
    path('patrimonio/resguardos/bien/<int:idbien>/historial/', views.historial_resguardo_bien, name='historial_resguardo_bien'),
    path('patrimonio/resguardos/empleado/<int:idempleado>/historial/', views.historial_resguardo_empleado, name='historial_resguardo_empleado'),
    path('patrimonio/resguardos/api/verificar-bien/<int:idbien>/', views.verificar_resguardo_bien, name='verificar_resguardo_bien'),

    # Entrega-Recepción por Departamento
    path('patrimonio/entregas-departamento/', views.listar_entregas_departamento, name='listar_entregas_departamento'),
    path('patrimonio/entregas-departamento/crear/', views.crear_entrega_departamento, name='crear_entrega_departamento'),
    path('patrimonio/entregas-departamento/<int:identrega>/', views.detalle_entrega_departamento, name='detalle_entrega_departamento'),
    
    # Seguridad del Sistema
    path('seguridad/usuarios/', views.listar_usuarios_sistema, name='listar_usuarios_sistema'),
    path('seguridad/usuarios/crear/', views.crear_usuario_sistema, name='crear_usuario_sistema'),
    path('seguridad/usuarios/<int:id_usuario>/editar/', views.editar_usuario_sistema, name='editar_usuario_sistema'),
    path('seguridad/configuracion/', views.configuracion_sistema, name='configuracion_sistema'),
    path('seguridad/configuracion/probar-smtp/', views.probar_smtp, name='probar_smtp'),
    path('seguridad/cola-correos/', views.monitor_cola_correos, name='monitor_cola_correos'),
    path('seguridad/cola-correos/procesar/', views.procesar_cola_ahora, name='procesar_cola_ahora'),
    
    # AJAX
    path('api/departamentos-por-direccion/', views.get_departamentos_por_direccion, name='get_departamentos_por_direccion'),
    path('api/estadisticas-cola/', views.api_estadisticas_cola, name='api_estadisticas_cola'),

    # Tickets de Servicio
    path('tickets/', views.listar_tickets, name='listar_tickets'),
    path('tickets/nuevo/', views.crear_ticket, name='crear_ticket'),
    path('tickets/<int:id_ticket>/', views.ver_ticket, name='ver_ticket'),
    path('tickets/archivos/<int:id_archivo>/descargar/', views.descargar_archivo_ticket, name='descargar_archivo_ticket'),
    path('tickets/archivos/<int:id_archivo>/eliminar/', views.eliminar_archivo_ticket, name='eliminar_archivo_ticket'),
]