# Primera entrega de algoritmo y programación 

## Miembros
Lizeth Dayana Valencia Higuita
Fortalezas en análisis de requisitos y documentación técnica
Jean Carlos Quinto Aguirre
Habilidades en lógica de programación en Python y gestión de versiones en GitHub
Ingeniería Industrial - Universidad de Antioquia

## Nombre del proyecto
### LizJean Market & Loans
<img width="693" height="416" alt="image" src="https://github.com/user-attachments/assets/da753e47-172f-4469-a0cf-99a72bf5a1fd" />

Este software de consola es un sistema integral de gestión de activos diseñado para organizar el inventario personal de Michael Jackson Gamboa

# Reporte de visión
Este software permite registrar usuarios con validaciones estrictas y categorizar artículos como videojuegos, libros o herramientas. Su función principal es monitorear los tiempos de préstamo; si un artículo no es devuelto tras 30 días, el sistema lo transforma automáticamente en una venta, calculando subtotales, totales y un "impuesto por conchudez" del 23%. Los datos se gestionan mediante archivos planos y se exportan a CSV para un control administrativo profesional.
### Objetivo: Crear un entorno visualmente amigable para gestionar artículos mediante archivos planos y exportación a CSV.
### Beneficio: Evitar la pérdida de activos de MJ mediante un control riguroso de fechas y un sistema de facturación automática

# Especificación de requisitos
Gestión de Usuarios y Perfiles de Riesgo:
El sistema permitirá registrar usuarios validando nombre, apellido (mínimo 3 letras), documento (3-15 dígitos) y correo electrónico.
Condiciones de Préstamo: Se integrará una validación de "Reportes en Entidades". Si el usuario es mayor de edad, se exigirá registrar una fuente de ingresos; si es menor de edad, el sistema obligará a vincular los datos de un acudiente responsable.
Gestión de Inventario Dinámico:
Registro de artículos con ID único, categoría, precio de compra y estado inicial mediante lógica difusa.
El inventario debe actualizarse automáticamente (en archivos planos) cada vez que un producto sea marcado como Nuevo, Vendido o Prestado.
Control de Préstamos y Contrato de Responsabilidad:
Al realizar un préstamo, el usuario deberá aceptar digitalmente un "Contrato de Responsabilidad". Este estipula que el artículo debe devolverse en el mismo estado de calidad registrado.
Veto del Sistema: Si un usuario devuelve un producto dañado y se niega a pagar el valor de reposición, el software lo marcará automáticamente como "Vetado", impidiendo futuros préstamos.
Automatización de Ventas e Impuestos:
El sistema monitoreará diariamente los plazos (5, 10, 15 o 30 días).
Si se superan los 30 días, el sistema ejecutará el proceso de Venta Forzosa, generando una factura que incluya el subtotal (precio de adquisición) más el "Impuesto por Conchudez" del 23%.
Generación de Documentos y Certificaciones:
Generación de certificados de devolución en formato `.txt` (o PDF para bonificación) al retornar el ítem a tiempo.
Generación de facturas de venta detalladas con la motivación del cobro y datos del cliente.
Módulo de Administración Protegido:
Acceso restringido mediante usuario y contraseña de administrador.
Visualización de reportes críticos: total de ventas, lista de usuarios vetados, y estadísticas de flujo de caja (pagos realizados).
### Los requisitos no funcionales especifican los criterios de operación y calidad del sistema:
Persistencia de Datos: Toda la información de usuarios, inventario y transacciones debe almacenarse en archivos planos (archivos de texto) para asegurar la persistencia sin necesidad de una base de datos externa.
Interfaz de Usuario: El sistema debe operar mediante una interfaz de consola (CLI) que sea visualmente organizada, jerárquica y fácil de navegar para MJ.
Portabilidad de Reportes: El sistema debe ser capaz de exportar las estadísticas generales y el estado de los préstamos a formato CSV para su lectura en herramientas como Excel.
Seguridad Básica: Las contraseñas del módulo administrativo deben estar validadas contra un listado interno para prevenir accesos no autorizados

# Plan de proyecto
https://www.canva.com/design/DAHFNGSpQRA/EN8RWHi9-A0ZqawABvaQxA/edit?utm_content=DAHFNGSpQRA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
Cronograma: Desarrollo en 16 semanas con entregas en semana 8 y 16.
Presupuesto: Basado en 150 horas de formación profesional valoradas según el SMLV.

# Acta
<img width="425" height="517" alt="image" src="https://github.com/user-attachments/assets/d0399cf1-f0ac-445c-bb0c-1805ae29d136" />
