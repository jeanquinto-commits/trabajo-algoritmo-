import os
import csv
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE PERSISTENCIA ---
PATH = "src/"
USERS_FILE  = f"{PATH}usuarios.txt"
ITEMS_FILE  = f"{PATH}inventario.txt"
LOANS_FILE  = f"{PATH}prestamos.txt"

# --- BASE DE DATOS DE ADMINISTRADORES ---
ADMINS = [
    {"usuario": "admin",  "clave": "1234"},
    {"usuario": "lizeth", "clave": "udea2026"},
    {"usuario": "jean",   "clave": "industrial"}
]

# ---------------------------------------------------------------------------
# UTILIDADES DE LECTURA / ESCRITURA (corrigen \r\n y líneas corruptas)
# ---------------------------------------------------------------------------

def _leer_lineas(filepath):
    """Lee un archivo y retorna lista de listas (campos por línea), ignorando vacías y \r."""
    resultado = []
    with open(filepath, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\r\n").strip()
            if line:
                resultado.append(line.split(","))
    return resultado

def _escribir_lineas(filepath, lista_de_campos):
    """Escribe lista de listas al archivo con formato correcto (sin \r)."""
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        for campos in lista_de_campos:
            f.write(",".join(campos) + "\n")

# ---------------------------------------------------------------------------

def inicializar_sistema():
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    for f in [USERS_FILE, ITEMS_FILE, LOANS_FILE]:
        if not os.path.exists(f):
            with open(f, "w", encoding="utf-8") as file:
                pass

# --- VALIDACIONES ---
def validar_datos(nombre, apellido, doc, correo):
    if len(nombre) < 3:
        print(">> Error: El nombre debe tener minimo 3 caracteres.")
        return False
    if any(c.isdigit() for c in nombre):
        print(">> Error: El nombre no puede contener numeros.")
        return False
    if len(apellido) < 3:
        print(">> Error: El apellido debe tener minimo 3 caracteres.")
        return False
    if any(c.isdigit() for c in apellido):
        print(">> Error: El apellido no puede contener numeros.")
        return False
    if not doc.isdigit() or not (3 <= len(doc) <= 15):
        print(">> Error: El documento debe ser numerico y tener entre 3 y 15 digitos.")
        return False
    if "@" not in correo or correo.index("@") == 0 or correo.index("@") == len(correo) - 1:
        print(">> Error: El correo debe tener formato valido (ej: usuario@dominio.com).")
        return False
    partes_correo = correo.split("@")
    if len(partes_correo) != 2 or "." not in partes_correo[1]:
        print(">> Error: El correo debe tener un dominio valido (ej: usuario@dominio.com).")
        return False
    return True

# --- OPCIÓN 1: REGISTRAR USUARIO ---
def registrar_usuario():
    print("\n--- Registro LizJean Market & Loans ---")
    nom  = input("Nombre: ").strip()
    ape  = input("Apellido: ").strip()
    doc  = input("Documento: ").strip()
    mail = input("Correo: ").strip()

    if not validar_datos(nom, ape, doc, mail):
        return

    # Verificar documento duplicado
    for campos in _leer_lineas(USERS_FILE):
        if campos[0] == doc:
            print(f">> Error: Ya existe un usuario con el documento {doc}.")
            return

    edad_str = input("Edad: ").strip()
    if not edad_str.isdigit():
        print(">> Error: La edad debe ser un numero.")
        return
    edad = int(edad_str)

    if edad >= 18:
        info_extra = input("Fuente de ingresos: ").strip()
    else:
        info_extra = input("Nombre del acudiente: ").strip()

    print("Plazos disponibles: 5, 10, 15, 30 dias")
    plazo = input("Seleccione plazo: ").strip()
    if plazo not in ["5", "10", "15", "30"]:
        print(">> Error: Plazo invalido. Debe ser 5, 10, 15 o 30.")
        return

    # Formato: doc,nom,ape,mail,plazo,info_extra,vetado(0=no,1=si)
    with open(USERS_FILE, "a", encoding="utf-8", newline="\n") as f:
        f.write(f"{doc},{nom},{ape},{mail},{plazo},{info_extra},0\n")
    print(f">> Usuario '{nom} {ape}' registrado exitosamente!")

# --- OPCIÓN 2: REGISTRAR ARTÍCULO ---
def registrar_articulo():
    print("\n--- Registrar Articulo ---")
    art_id    = input("ID del articulo (ej: ART-001): ").strip()
    nombre    = input("Nombre del articulo: ").strip()
    categoria = input("Categoria: ").strip()
    valor     = input("Valor estimado ($): ").strip()

    if not art_id or not nombre:
        print(">> Error: El ID y el nombre son obligatorios.")
        return
    if not valor.isdigit():
        print(">> Error: El valor debe ser un numero entero.")
        return

    # Verificar ID duplicado
    for campos in _leer_lineas(ITEMS_FILE):
        if campos[0] == art_id:
            print(f">> Error: Ya existe un articulo con el ID '{art_id}'.")
            return

    # Formato: id,nombre,categoria,valor,disponible(1=si,0=no)
    with open(ITEMS_FILE, "a", encoding="utf-8", newline="\n") as f:
        f.write(f"{art_id},{nombre},{categoria},{valor},1\n")
    print(f">> Articulo '{nombre}' registrado exitosamente en el inventario!")

# --- OPCIÓN 3: REGISTRAR PRÉSTAMO ---
def registrar_prestamo():
    print("\n--- Nuevo Prestamo ---")
    doc     = input("Documento del usuario: ").strip()
    item_id = input("ID del articulo: ").strip()

    # Verificar usuario
    usuario_ok     = False
    plazo_usuario  = "15"
    nombre_usuario = ""
    for campos in _leer_lineas(USERS_FILE):
        if len(campos) >= 7 and campos[0] == doc:
            if campos[6] == "1":
                print(">> Error: Este usuario esta VETADO y no puede realizar prestamos.")
                return
            usuario_ok     = True
            nombre_usuario = f"{campos[1]} {campos[2]}"
            plazo_usuario  = campos[4]
            break

    if not usuario_ok:
        print(f">> Error: No se encontro ningun usuario con el documento '{doc}'.")
        return

    # Verificar artículo — requiere exactamente 5 campos y disponible == "1"
    articulo_ok     = False
    nombre_articulo = ""
    for campos in _leer_lineas(ITEMS_FILE):
        if len(campos) >= 5 and campos[0] == item_id:
            if campos[4] != "1":
                print(f">> Error: El articulo '{campos[1]}' no esta disponible.")
                return
            articulo_ok     = True
            nombre_articulo = campos[1]
            break

    if not articulo_ok:
        print(f">> Error: No se encontro ningun articulo con el ID '{item_id}'.")
        return

    print("\nCONTRATO DE RESPONSABILIDAD: Me comprometo a devolver el item en buen estado.")
    acepta = input("Acepta el contrato? (S/N): ").strip().upper()

    if acepta == "S":
        fecha      = datetime.now().strftime("%Y-%m-%d")
        fecha_venc = (datetime.now() + timedelta(days=int(plazo_usuario))).strftime("%Y-%m-%d")
        with open(LOANS_FILE, "a", encoding="utf-8", newline="\n") as f:
            # Formato: doc,item_id,fecha_inicio,fecha_vencimiento,estado
            f.write(f"{doc},{item_id},{fecha},{fecha_venc},Activo\n")
        _actualizar_disponibilidad(item_id, "0")
        print(f">> Prestamo registrado con exito!")
        print(f"   Usuario  : {nombre_usuario}")
        print(f"   Articulo : {nombre_articulo}")
        print(f"   Devolver antes del: {fecha_venc}")
    else:
        print(">> Prestamo cancelado.")

# --- OPCIÓN 4: REGISTRAR DEVOLUCIÓN ---
def registrar_devolucion():
    print("\n--- Registro de Devolucion ---")
    item_id = input("ID del articulo que devuelve: ").strip()

    # Buscar préstamo activo
    doc_usuario = None
    for campos in _leer_lineas(LOANS_FILE):
        if len(campos) >= 5 and campos[1] == item_id and campos[4] == "Activo":
            doc_usuario = campos[0]
            break

    if not doc_usuario:
        print(f">> Error: No hay un prestamo activo para el articulo '{item_id}'.")
        return

    print("Estado de entrega:")
    print("  1. Excelente")
    print("  2. Bueno")
    print("  3. Dañado")
    op_estado = input("Seleccione (1/2/3): ").strip()
    estados = {"1": "Excelente", "2": "Bueno", "3": "Dañado"}
    if op_estado not in estados:
        print(">> Error: Opcion invalida.")
        return
    estado = estados[op_estado]

    _actualizar_estado_prestamo(item_id)
    _actualizar_disponibilidad(item_id, "1")

    if estado == "Dañado":
        _vetar_usuario(doc_usuario)
        print(f">> ATENCION! El articulo fue devuelto DAÑADO.")
        print(f">> El usuario con documento '{doc_usuario}' ha sido VETADO del sistema.")
    else:
        print(f">> Devolucion procesada exitosamente! Estado recibido: {estado}.")

# --- OPCIÓN 5: CONSULTAR ÍTEMS +30 DÍAS (VENTA FORZOSA) ---
def consultar_venta_forzosa():
    print("\n--- Articulos en Venta Forzosa (mora > 30 dias, Impuesto 23%) ---")
    hoy = datetime.now().date()
    encontrados = 0

    # Cargar inventario en memoria para búsqueda rápida
    inventario = {}
    for campos in _leer_lineas(ITEMS_FILE):
        if len(campos) >= 4:
            val = campos[3] if campos[3].isdigit() else "0"
            inventario[campos[0]] = {"nombre": campos[1], "valor": int(val)}

    for campos in _leer_lineas(LOANS_FILE):
        if len(campos) >= 5 and campos[4] == "Activo":
            try:
                fecha_venc = datetime.strptime(campos[3], "%Y-%m-%d").date()
                dias_mora  = (hoy - fecha_venc).days
                if dias_mora > 30:
                    encontrados += 1
                    info_art = inventario.get(campos[1], {"nombre": campos[1], "valor": 0})
                    valor          = info_art["valor"]
                    valor_impuesto = round(valor * 1.23)
                    print(f"  - Doc: {campos[0]} | Articulo: {campos[1]} ({info_art['nombre']}) | Vencio: {campos[3]} | Mora: {dias_mora} dias")
                    print(f"    Valor: ${valor:,} | Con impuesto 23%: ${valor_impuesto:,}")
            except ValueError:
                continue

    if encontrados == 0:
        print(">> No hay articulos con mas de 30 dias en mora.")

# --- OPCIÓN 6: CONSULTAR ARTÍCULOS PRESTADOS ---
def consultar_prestados():
    print("\n--- Inventario en Prestamo ---")
    hoy = datetime.now().date()
    encontrados = 0

    # Cargar inventario en memoria
    inventario = {}
    for campos in _leer_lineas(ITEMS_FILE):
        if len(campos) >= 2:
            inventario[campos[0]] = campos[1]

    for campos in _leer_lineas(LOANS_FILE):
        if len(campos) >= 5 and campos[4] == "Activo":
            encontrados += 1
            nombre_art = inventario.get(campos[1], campos[1])
            try:
                fecha_venc   = datetime.strptime(campos[3], "%Y-%m-%d").date()
                dias         = (fecha_venc - hoy).days
                estado_plazo = f"VENCIDO hace {abs(dias)} dias" if dias < 0 else f"Vence en {dias} dias"
            except ValueError:
                estado_plazo = "Fecha invalida"
            print(f"  - Doc: {campos[0]} | Articulo: {campos[1]} ({nombre_art}) | Inicio: {campos[2]} | Vence: {campos[3]} | {estado_plazo}")

    if encontrados == 0:
        print(">> No hay articulos prestados actualmente.")

# --- OPCIÓN 7: ADMINISTRADOR ---
def modulo_admin():
    print("\n--- Acceso Administrador ---")
    user_log = input("Usuario Admin: ").strip()
    pass_log = input("Clave: ").strip()

    acceso = any(a["usuario"] == user_log and a["clave"] == pass_log for a in ADMINS)

    if acceso:
        print(f"\n>> Bienvenido, {user_log}.")
        print("\n--- PANEL ADMIN ---")
        print("1. Exportar Reporte CSV")
        print("2. Ver Usuarios Vetados")
        op = input("Seleccione: ").strip()
        if op == "1":
            exportar_csv()
        elif op == "2":
            ver_vetados()
        else:
            print(">> Opcion invalida.")
    else:
        print(">> Acceso denegado. Credenciales incorrectas.")

def exportar_csv():
    with open("reporte_lizjean.csv", "w", newline="", encoding="utf-8") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["Usuario", "Item", "Fecha Inicio", "Fecha Vencimiento", "Estado"])
        for campos in _leer_lineas(LOANS_FILE):
            if len(campos) >= 5:
                writer.writerow(campos[:5])
    print(">> CSV exportado exitosamente como 'reporte_lizjean.csv'!")

def ver_vetados():
    print("\n--- Usuarios Vetados ---")
    encontrados = 0
    for campos in _leer_lineas(USERS_FILE):
        if len(campos) >= 7 and campos[6] == "1":
            encontrados += 1
            print(f"  - Doc: {campos[0]} | Nombre: {campos[1]} {campos[2]} | Correo: {campos[3]}")
    if encontrados == 0:
        print(">> No hay usuarios vetados actualmente.")

# --- FUNCIONES AUXILIARES ---
def _actualizar_disponibilidad(item_id, valor):
    """Actualiza el campo disponibilidad (índice 4) de un artículo. Siempre normaliza a 5 campos."""
    lineas = _leer_lineas(ITEMS_FILE)
    for campos in lineas:
        if campos[0] == item_id:
            # Normalizar a 5 campos exactos (por si había campos extra)
            campos_norm = campos[:5] if len(campos) >= 5 else campos + ["1"] * (5 - len(campos))
            campos_norm[4] = valor
            campos[:] = campos_norm
    _escribir_lineas(ITEMS_FILE, lineas)

def _actualizar_estado_prestamo(item_id):
    """Cambia el estado del primer préstamo Activo del artículo a Devuelto."""
    lineas    = _leer_lineas(LOANS_FILE)
    actualizado = False
    for campos in lineas:
        if not actualizado and len(campos) >= 5 and campos[1] == item_id and campos[4] == "Activo":
            campos[4]   = "Devuelto"
            actualizado = True
    _escribir_lineas(LOANS_FILE, lineas)

def _vetar_usuario(doc):
    """Pone el campo vetado (índice 6) en '1' para el usuario indicado."""
    lineas = _leer_lineas(USERS_FILE)
    for campos in lineas:
        if campos[0] == doc and len(campos) >= 7:
            campos[6] = "1"
    _escribir_lineas(USERS_FILE, lineas)

# ---------------------------------------------------------------------------
# LIMPIEZA DE DATOS EXISTENTES
# Corrige los archivos .txt que pueden tener registros corruptos o \r\n
# ---------------------------------------------------------------------------
def limpiar_datos_existentes():
    """
    Normaliza los archivos actuales:
    - Elimina \r (saltos de Windows)
    - Fuerza inventario a 5 campos exactos (id,nombre,cat,valor,disponible)
    - Fuerza prestamos a 5 campos exactos (doc,item_id,f_inicio,f_venc,estado)
    - Fuerza usuarios a 7 campos exactos (doc,nom,ape,mail,plazo,info,vetado)
    - Descarta líneas con número incorrecto de campos (con aviso)
    """
    # --- INVENTARIO (5 campos) ---
    lineas_inv = []
    for campos in _leer_lineas(ITEMS_FILE):
        if len(campos) == 5:
            lineas_inv.append(campos)
        elif len(campos) > 5:
            # Truncar campos extra
            print(f"  [Limpieza inventario] Campos extra en '{campos[0]}', normalizando a 5.")
            lineas_inv.append(campos[:5])
        else:
            print(f"  [Limpieza inventario] Linea con {len(campos)} campos descartada: {campos}")
    _escribir_lineas(ITEMS_FILE, lineas_inv)

    # --- PRÉSTAMOS (5 campos) ---
    lineas_pre = []
    for campos in _leer_lineas(LOANS_FILE):
        if len(campos) == 5:
            lineas_pre.append(campos)
        else:
            print(f"  [Limpieza prestamos] Linea con {len(campos)} campos descartada: {campos}")
    _escribir_lineas(LOANS_FILE, lineas_pre)

    # --- USUARIOS (7 campos) ---
    lineas_usr = []
    for campos in _leer_lineas(USERS_FILE):
        if len(campos) == 7:
            lineas_usr.append(campos)
        else:
            print(f"  [Limpieza usuarios] Linea con {len(campos)} campos descartada: {campos}")
    _escribir_lineas(USERS_FILE, lineas_usr)

    print(">> Limpieza de datos completada.\n")

# --- MENÚ PRINCIPAL ---
def menu():
    while True:
        print("\n" + "="*35)
        print("      LIZJEAN MARKET & LOANS ")
        print("="*35)
        print("1. Registrar Usuario")
        print("2. Registrar Articulo")
        print("3. Registrar Prestamo")
        print("4. Registrar Devolucion")
        print("5. Consultar Items con mas de 30 dias")
        print("6. Consultar Articulos Prestados")
        print("7. Administrador")
        print("8. Salir")

        op = input("\nSeleccione opcion: ").strip()

        if   op == "1": registrar_usuario()
        elif op == "2": registrar_articulo()
        elif op == "3": registrar_prestamo()
        elif op == "4": registrar_devolucion()
        elif op == "5": consultar_venta_forzosa()
        elif op == "6": consultar_prestados()
        elif op == "7": modulo_admin()
        elif op == "8": print("\nHasta luego!\n"); break
        else: print(">> Opcion invalida.")

if __name__ == "__main__":
    inicializar_sistema()
    print(">> Iniciando limpieza y normalizacion de datos...")
    limpiar_datos_existentes()
    menu()