
LIZJEAN MARKET & LOANS
Sistema de Gestión de Préstamos e Inventario

MANUAL DE USUARIO — GUÍA COMPLETA DE OPERACIÓN

Versión 2.0  •  2026

 
1. Introducción
LizJean Market & Loans es un sistema de consola para gestionar préstamos de artículos e inventario. Permite registrar usuarios, artículos, préstamos y devoluciones, y ofrece herramientas de consulta y administración.

1.1 Estructura de archivos
Organización requerida en disco:
proyecto/
    jean.py              ← Script principal (ejecutar desde aquí)
    src/
        usuarios.txt     ← Base de datos de usuarios
        inventario.txt   ← Base de datos de artículos
        prestamos.txt    ← Registro de préstamos

1.2 Cómo ejecutar
Paso	Comando / Acción
1. Abrir terminal	Navegar hasta la carpeta donde está jean.py
2. Ejecutar	python jean.py
3. Limpieza automática	El sistema normaliza los .txt al arrancar
4. Menú principal	Seleccionar la opción deseada (1–8)

1.3 Formatos de los archivos .txt
Cada archivo almacena los datos separados por comas (,). No editar manualmente salvo que conozca el formato.

Archivo	Campos (en orden)
usuarios.txt	documento, nombre, apellido, correo, plazo, info_extra, vetado
inventario.txt	id, nombre, categoria, valor, disponible
prestamos.txt	documento, id_articulo, fecha_inicio, fecha_vencimiento, estado

 
2. Menú Principal
Al ejecutar el sistema, aparece el siguiente menú:

===================================
      LIZJEAN MARKET & LOANS
===================================
1. Registrar Usuario
2. Registrar Artículo
3. Registrar Préstamo
4. Registrar Devolución
5. Consultar Ítems con más de 30 días
6. Consultar Artículos Prestados
7. Administrador
8. Salir

Ingrese el número de la opción y presione Enter. Opciones inválidas muestran el mensaje: >> Opción inválida.

 
3. Opción 1 — Registrar Usuario
Registra un nuevo usuario en el sistema. El sistema solicita los siguientes datos en orden:

Campo	Descripción
Nombre	Nombre(s) del usuario
Apellido	Apellido(s) del usuario
Documento	Número de identificación único
Correo	Dirección de correo electrónico
Edad	Edad en años (número entero)
Fuente de ingresos / Acudiente	Si edad >= 18: fuente de ingresos. Si < 18: nombre del acudiente
Plazo	Días de préstamo: 5, 10, 15 o 30

3.1 Validaciones de registro
Se validan todos los campos antes de guardar. Si alguno falla, el registro se cancela y debe iniciarse de nuevo.

Campo	Regla	Ejemplo válido	Error si...
Nombre	Mínimo 3 caracteres, sin números	Carlos	< 3 caracteres o contiene dígitos
Apellido	Mínimo 3 caracteres, sin números	Gomez	< 3 caracteres o contiene dígitos
Documento	Solo dígitos, entre 3 y 15 caracteres	1027998021	Tiene letras o longitud fuera de rango
Documento	No duplicado en el sistema	999111222	Ya existe en usuarios.txt
Correo	Formato usuario@dominio.ext	user@gmail.com	Sin @, sin dominio o sin extensión
Edad	Número entero positivo	25	Contiene letras o símbolos
Plazo	Solo: 5, 10, 15 o 30	30	Cualquier otro valor

3.2 Mensajes de error
Mensaje del sistema	Causa
>> Error: El nombre debe tener minimo 3 caracteres.	Nombre con menos de 3 caracteres
>> Error: El nombre no puede contener numeros.	Nombre con dígitos (ej: Car3los)
>> Error: El apellido debe tener minimo 3 caracteres.	Apellido muy corto
>> Error: El documento debe ser numerico...	Documento con letras o fuera de 3–15 dígitos
>> Error: Ya existe un usuario con el documento X.	Documento duplicado
>> Error: El correo debe tener formato valido.	Correo sin @ o sin dominio válido
>> Error: La edad debe ser un numero.	Edad con letras o vacía
>> Error: Plazo invalido.	Plazo distinto a 5, 10, 15 o 30

3.3 Registro exitoso
Salida esperada:
>> Usuario 'Carlos Gomez' registrado exitosamente!

 
4. Opción 2 — Registrar Artículo
Agrega un nuevo artículo al inventario. El sistema solicita:

Campo	Descripción	Ejemplo
ID del artículo	Identificador único (se recomienda formato ART-XXX)	ART-004
Nombre	Descripción del artículo	Bicicleta
Categoría	Clasificación del artículo	Deportes
Valor estimado	Precio en pesos (solo dígitos enteros)	150000

4.1 Validaciones
Campo	Regla	Ejemplo válido	Error si...
ID	No puede estar vacío, sin duplicados	ART-004	Ya existe ese ID o está en blanco
Nombre	No puede estar vacío	Bicicleta	Campo en blanco
Valor	Solo dígitos enteros	150000	Contiene letras, puntos o comas

4.2 Mensajes de error y éxito
Mensaje	Causa
>> Error: El ID y el nombre son obligatorios.	ID o nombre vacío
>> Error: El valor debe ser un numero entero.	Valor con letras o decimales
>> Error: Ya existe un articulo con el ID 'X'.	ID duplicado
>> Articulo 'X' registrado exitosamente en el inventario!	Registro correcto

Los artículos se registran con disponibilidad = 1 (disponible). Este valor cambia automáticamente al prestarse o devolverse.

 
5. Opción 3 — Registrar Préstamo
Asocia un artículo disponible a un usuario registrado. Se calculan las fechas automáticamente según el plazo del usuario.

Campo	Descripción
Documento del usuario	Número de documento registrado en el sistema
ID del artículo	ID del artículo disponible en inventario
Aceptar contrato	S para confirmar, N para cancelar

5.1 Validaciones (en orden de ejecución)
Verificación	Condición requerida	Si pasa	Si falla
Usuario existe	Documento registrado en usuarios.txt	Continúa	Error: no encontrado
Usuario no vetado	Campo vetado = 0	Continúa	Error: usuario VETADO
Artículo existe	ID registrado en inventario.txt	Continúa	Error: no encontrado
Artículo disponible	Campo disponible = 1	Continúa	Error: no disponible
Contrato aceptado	Respuesta = S (mayúscula)	Préstamo registrado	Préstamo cancelado

5.2 Cálculo de fecha de vencimiento
Fórmula:
Fecha de vencimiento = Fecha actual + Plazo del usuario (días)

Ejemplo: Si hoy es 2026-05-30 y el usuario tiene plazo de 30 días,
         la fecha de vencimiento será: 2026-06-29

5.3 Mensajes de error y éxito
Mensaje	Causa
>> Error: No se encontro ningun usuario con el documento 'X'.	Documento no existe
>> Error: Este usuario esta VETADO...	Usuario marcado como vetado
>> Error: No se encontro ningun articulo con el ID 'X'.	ID no existe en inventario
>> Error: El articulo 'X' no esta disponible.	Artículo ya prestado
>> Prestamo cancelado.	Usuario respondió N al contrato
>> Prestamo registrado con exito! + detalles	Préstamo registrado correctamente

5.4 Efectos sobre el inventario
Al registrar un préstamo el sistema automáticamente:
• Crea una línea en prestamos.txt con estado = Activo
• Cambia disponible = 0 en inventario.txt para ese artículo
• El artículo no podrá prestarse de nuevo hasta que sea devuelto

 
6. Opción 4 — Registrar Devolución
Procesa la devolución de un artículo. El sistema lo busca por su ID en los préstamos activos.

Campo	Descripción
ID del artículo	ID del artículo que se está devolviendo
Estado de entrega	1 = Excelente, 2 = Bueno, 3 = Dañado

6.1 Validaciones
Verificación	Condición	Si pasa	Si falla
Préstamo activo	Existe en prestamos.txt con estado = Activo	Continúa	Error: no hay préstamo activo
Estado válido	Opción 1, 2 o 3	Continúa	Error: opción inválida

6.2 Estados de entrega y consecuencias
Opción	Estado	Consecuencia
1	Excelente	Devolución normal. Artículo disponible de nuevo.
2	Bueno	Devolución normal. Artículo disponible de nuevo.
3	Dañado	Artículo disponible de nuevo + usuario VETADO automáticamente.

6.3 Efectos automáticos
Al registrar una devolución el sistema:
• Cambia el estado del préstamo de Activo → Devuelto en prestamos.txt
• Cambia disponible = 1 en inventario.txt (artículo libre para prestar)
• Si estado = Dañado: cambia vetado = 1 en usuarios.txt
  → El usuario vetado ya no podrá realizar nuevos préstamos

 
7. Opción 5 — Consultar Ítems con más de 30 días (Venta Forzosa)
Muestra artículos cuyo préstamo activo superó los 30 días desde la fecha de vencimiento. Se aplica un impuesto del 23% sobre el valor estimado del artículo.

7.1 Criterio de inclusión
Un artículo aparece en esta lista si:
  • Estado del préstamo = Activo
  • Días transcurridos desde fecha de vencimiento > 30

Fórmula: Mora = Fecha actual − Fecha de vencimiento
         Precio final = Valor del artículo × 1.23

7.2 Información mostrada por artículo
Campo mostrado	Descripción
Doc	Documento del usuario que tiene el artículo
Artículo	ID y nombre del artículo
Venció	Fecha en que debió devolverse
Mora	Días de atraso desde el vencimiento
Valor	Valor estimado original del artículo
Con impuesto 23%	Valor total a cobrar en venta forzosa

 
8. Opción 6 — Consultar Artículos Prestados
Lista todos los artículos con estado Activo en el registro de préstamos, mostrando el estado del plazo en tiempo real.

Campo mostrado	Descripción
Doc	Documento del usuario que tiene el artículo
Artículo	ID y nombre del artículo
Inicio	Fecha en que se realizó el préstamo
Vence	Fecha límite de devolución
Estado del plazo	'Vence en X días' o 'VENCIDO hace X días'

Nota:
Si un artículo aparece como 'VENCIDO hace X días' y lleva más de
30 días, también aparecerá en la Opción 5 (Venta Forzosa).

 
9. Opción 7 — Módulo Administrador
Requiere credenciales válidas para acceder. Contiene funciones avanzadas de gestión.

9.1 Credenciales de acceso
Usuario	Contraseña
admin	1234
lizeth	udea2026
jean	industrial

9.2 Opciones del panel

Opción	Función	Descripción
1	Exportar Reporte CSV	Genera reporte_lizjean.csv con todos los préstamos (activos y devueltos)
2	Ver Usuarios Vetados	Lista todos los usuarios con vetado = 1

9.3 Reporte CSV
El archivo reporte_lizjean.csv se guarda en la misma carpeta que jean.py y contiene:
Columnas: Usuario, Item, Fecha Inicio, Fecha Vencimiento, Estado
Incluye tanto préstamos Activos como Devueltos
Se puede abrir con Excel, Google Sheets o cualquier editor de hojas de cálculo

9.4 Usuarios Vetados
Muestra: Documento, Nombre completo y Correo de cada usuario vetado.
Un usuario es vetado automáticamente al devolver un artículo en estado Dañado (Opción 4).
Los usuarios vetados reciben el mensaje de error al intentar hacer un préstamo:
>> Error: Este usuario esta VETADO y no puede realizar prestamos.

 
10. Limpieza Automática al Arranque
Cada vez que se ejecuta jean.py, el sistema revisa y normaliza los archivos .txt antes de mostrar el menú.

Archivo	Campos esperados	Acción si hay error
inventario.txt	5 campos exactos	Trunca campos extra o descarta la línea con aviso
prestamos.txt	5 campos exactos	Descarta la línea corrupta con aviso
usuarios.txt	7 campos exactos	Descarta la línea corrupta con aviso

Importante:
Las líneas descartadas se muestran en pantalla al inicio con el prefijo [Limpieza ...].
Si un registro fue descartado, deberá volver a registrarse desde el menú.
La limpieza también elimina caracteres de Windows (\r) que pueden causar errores de lectura.

 
11. Resumen General de Validaciones
Tabla consolidada de todas las validaciones del sistema:

Módulo	Campo / Condición	Válido si...	Mensaje de error
Reg. Usuario	Nombre	≥ 3 chars, sin números	Error: nombre inválido
Reg. Usuario	Apellido	≥ 3 chars, sin números	Error: apellido inválido
Reg. Usuario	Documento	Solo dígitos, 3–15 chars	Error: documento inválido
Reg. Usuario	Documento duplicado	No existe en sistema	Error: documento existente
Reg. Usuario	Correo	usuario@dominio.ext	Error: correo inválido
Reg. Usuario	Edad	Número entero	Error: edad inválida
Reg. Usuario	Plazo	5, 10, 15 o 30	Error: plazo inválido
Reg. Artículo	ID	No vacío, no duplicado	Error: ID inválido o duplicado
Reg. Artículo	Nombre	No vacío	Error: nombre obligatorio
Reg. Artículo	Valor	Solo enteros	Error: valor inválido
Reg. Préstamo	Usuario	Existe y no vetado	Error: no existe / VETADO
Reg. Préstamo	Artículo	Existe y disponible	Error: no existe / no disponible
Reg. Préstamo	Contrato	Respuesta = S	Préstamo cancelado si N
Devolución	Artículo	Préstamo activo existe	Error: sin préstamo activo
Devolución	Estado	Opción 1, 2 o 3	Error: opción inválida
Admin	Credenciales	Usuario y clave coinciden	Acceso denegado


