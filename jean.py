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

def inicializar_sistema():
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    for f in [USERS_FILE, ITEMS_FILE, LOANS_FILE]:
        if not os.path.exists(f):
            with open(f, "w", encoding="utf-8") as file:
                pass

# --- VALIDACIONES (mensajes detallados) ---
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
        print(">> Error: El documento debe ser numérico y tener entre 3 y 15 digitos.")
        return False
    if "@" not in correo:
        print(">> Error: El correo debe contener '@'.")
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
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip() and line.strip().split(",")[0] == doc:
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

    print("Plazos disponibles: 5, 10, 15, 30 días")
    plazo = input("Seleccione plazo: ").strip()
    if plazo not in ["5", "10", "15", "30"]:
        print(">> Error: Plazo inválido. Debe ser 5, 10, 15 o 30.")
        return

    with open(USERS_FILE, "a", encoding="utf-8") as f:
        # formato: doc,nom,ape,mail,plazo,info_extra,vetado(0=no,1=si)
        f.write(f"{doc},{nom},{ape},{mail},{plazo},{info_extra},0\n")
    print(f">> ¡Usuario '{nom} {ape}' registrado exitosamente!")

# --- OPCIÓN 2: REGISTRAR ARTÍCULO ---
def registrar_articulo():
    print("\n--- Registrar Artículo ---")
    art_id   = input("ID del artículo (ej: ART-001): ").strip()
    nombre   = input("Nombre del artículo: ").strip()
    categoria = input("Categoría: ").strip()
    valor    = input("Valor estimado ($): ").strip()

    if not art_id or not nombre:
        print(">> Error: El ID y el nombre son obligatorios.")
        return

    # Verificar ID duplicado
    with open(ITEMS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip() and line.strip().split(",")[0] == art_id:
                print(f">> Error: Ya existe un artículo con el ID '{art_id}'.")
                return

    with open(ITEMS_FILE, "a", encoding="utf-8") as f:
        # formato: id,nombre,categoria,valor,disponible(1=si,0=no)
        f.write(f"{art_id},{nombre},{categoria},{valor},1\n")
    print(f">> ¡Artículo '{nombre}' registrado exitosamente en el inventario!")

# --- OPCIÓN 3: REGISTRAR PRÉSTAMO ---
def registrar_prestamo():
    print("\n--- Nuevo Prestamo ---")
    doc     = input("Documento del usuario: ").strip()
    item_id = input("ID del artículo: ").strip()

    # Verificar usuario
    usuario_ok    = False
    plazo_usuario = "15"
    nombre_usuario = ""
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            partes = line.split(",")
            if partes[0] == doc:
                if len(partes) >= 7 and partes[6] == "1":
                    print(">> Error: Este usuario está VETADO y no puede realizar prestamos.")
                    return
                usuario_ok     = True
                nombre_usuario = f"{partes[1]} {partes[2]}"
                plazo_usuario  = partes[4]
                break

    if not usuario_ok:
        print(f">> Error: No se encontro ningun usuario con el documento '{doc}'.")
        return

    # Verificar artículo
    articulo_ok     = False
    nombre_articulo = ""
    with open(ITEMS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            partes = line.split(",")
            if partes[0] == item_id:
                if len(partes) >= 5 and partes[4] == "0":
                    print(f">> Error: El articulo '{partes[1]}' no está disponible.")
                    return
                articulo_ok     = True
                nombre_articulo = partes[1]
                break

    if not articulo_ok:
        print(f">> Error: No se encontro ningun articulo con el ID '{item_id}'.")
        return

    print("\nCONTRATO DE RESPONSABILIDAD: Me comprometo a devolver el item en buen estado.")
    acepta = input("¿Acepta el contrato? (S/N): ").strip().upper()

    if acepta == "S":
        fecha      = datetime.now().strftime("%Y-%m-%d")
        fecha_venc = (datetime.now() + timedelta(days=int(plazo_usuario))).strftime("%Y-%m-%d")
        with open(LOANS_FILE, "a", encoding="utf-8") as f:
            # formato: doc,item_id,fecha_inicio,fecha_vencimiento,estado
            f.write(f"{doc},{item_id},{fecha},{fecha_venc},Activo\n")
        _actualizar_disponibilidad(item_id, "0")
        print(f">> ¡Préstamo registrado con éxito!")
        print(f"   Usuario  : {nombre_usuario}")
        print(f"   Artículo : {nombre_articulo}")
        print(f"   Devolver antes del: {fecha_venc}")
    else:
        print(">> Prestamo cancelado.")

# --- OPCIÓN 4: REGISTRAR DEVOLUCIÓN ---
def registrar_devolucion():
    print("\n--- Registro de Devolucion ---")
    item_id = input("ID del articulo que devuelve: ").strip()

    # Buscar préstamo activo
    doc_usuario = None
    with open(LOANS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            partes = line.split(",")
            if len(partes) >= 5 and partes[1] == item_id and partes[4] == "Activo":
                doc_usuario = partes[0]
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
        print(f">> ¡ATENCIoN! El articulo fue devuelto DAÑADO.")
        print(f">> El usuario con documento '{doc_usuario}' ha sido VETADO del sistema.")
    else:
        print(f">> ¡Devolucion procesada exitosamente! Estado recibido: {estado}.")

# --- OPCIÓN 5: CONSULTAR ÍTEMS +30 DÍAS (VENTA FORZOSA) ---
def consultar_venta_forzosa():
    print("\n--- Articulos en Venta Forzosa (mora > 30 dias, Impuesto 23%) ---")
    hoy = datetime.now().date()
    encontrados = 0
    with open(LOANS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            partes = line.split(",")
            if len(partes) >= 5 and partes[4] == "Activo":
                try:
                    fecha_venc = datetime.strptime(partes[3], "%Y-%m-%d").date()
                    dias_mora  = (hoy - fecha_venc).days
                    if dias_mora > 30:
                        encontrados += 1
                        valor = 0
                        with open(ITEMS_FILE, "r", encoding="utf-8") as fi:
                            for li in fi:
                                li = li.strip()
                                if not li:
                                    continue
                                pi = li.split(",")
                                if pi[0] == partes[1] and len(pi) >= 4:
                                    valor = int(pi[3]) if pi[3].isdigit() else 0
                        valor_impuesto = round(valor * 1.23)
                        print(f"  - Doc: {partes[0]} | Articulo: {partes[1]} | Venció: {partes[3]} | Mora: {dias_mora} dias")
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
    with open(LOANS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            partes = line.split(",")
            if len(partes) >= 5 and partes[4] == "Activo":
                encontrados += 1
                try:
                    fecha_venc   = datetime.strptime(partes[3], "%Y-%m-%d").date()
                    dias         = (fecha_venc - hoy).days
                    estado_plazo = f"VENCIDO hace {abs(dias)} días" if dias < 0 else f"Vence en {dias} días"
                except ValueError:
                    estado_plazo = "Fecha inválida"
                print(f"  - Doc: {partes[0]} | Artículo: {partes[1]} | Inicio: {partes[2]} | Vence: {partes[3]} | {estado_plazo}")
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
            print(">> Opción inválida.")
    else:
        print(">> Acceso denegado. Credenciales incorrectas.")

def exportar_csv():
    with open(LOANS_FILE, "r", encoding="utf-8") as f_in, \
         open("reporte_lizjean.csv", "w", newline="", encoding="utf-8") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["Usuario", "Item", "Fecha Inicio", "Fecha Vencimiento", "Estado"])
        for line in f_in:
            if line.strip():
                writer.writerow(line.strip().split(","))
    print(">> ¡CSV exportado exitosamente como 'reporte_lizjean.csv'!")

def ver_vetados():
    print("\n--- Usuarios Vetados ---")
    encontrados = 0
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            partes = line.split(",")
            if len(partes) >= 7 and partes[6] == "1":
                encontrados += 1
                print(f"  - Doc: {partes[0]} | Nombre: {partes[1]} {partes[2]} | Correo: {partes[3]}")
    if encontrados == 0:
        print(">> No hay usuarios vetados actualmente.")

# --- FUNCIONES AUXILIARES ---
def _actualizar_disponibilidad(item_id, valor):
    lineas = []
    with open(ITEMS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            partes = line.strip().split(",")
            if partes[0] == item_id and len(partes) >= 5:
                partes[4] = valor
            lineas.append(",".join(partes) + "\n")
    with open(ITEMS_FILE, "w", encoding="utf-8") as f:
        f.writelines(lineas)

def _actualizar_estado_prestamo(item_id):
    lineas = []
    actualizado = False
    with open(LOANS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            partes = line.strip().split(",")
            if not actualizado and len(partes) >= 5 and partes[1] == item_id and partes[4] == "Activo":
                partes[4] = "Devuelto"
                actualizado = True
            lineas.append(",".join(partes) + "\n")
    with open(LOANS_FILE, "w", encoding="utf-8") as f:
        f.writelines(lineas)

def _vetar_usuario(doc):
    lineas = []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            partes = line.strip().split(",")
            if partes[0] == doc and len(partes) >= 7:
                partes[6] = "1"
            lineas.append(",".join(partes) + "\n")
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        f.writelines(lineas)

# --- MENÚ PRINCIPAL ---
def menu():
    while True:
        print("\n" + "="*35)
        print("      LIZJEAN MARKET & LOANS ")
        print("="*35)
        print("1. Registrar Usuario")
        print("2. Registrar Artículo")
        print("3. Registrar Préstamo")
        print("4. Registrar Devolución")
        print("5. Consultar Ítems con más de 30 días")
        print("6. Consultar Artículos Prestados")
        print("7. Administrador")
        print("8. Salir")

        op = input("\nSeleccione opción: ").strip()

        if   op == "1": registrar_usuario()
        elif op == "2": registrar_articulo()
        elif op == "3": registrar_prestamo()
        elif op == "4": registrar_devolucion()
        elif op == "5": consultar_venta_forzosa()
        elif op == "6": consultar_prestados()
        elif op == "7": modulo_admin()
        elif op == "8": print("\n¡Hasta luego!\n"); break
        else: print(">> Opción inválida.")

if __name__ == "__main__":
    inicializar_sistema()
    menu()