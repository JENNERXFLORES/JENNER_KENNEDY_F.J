import streamlit as st
import sqlite3
import random
import time
import pandas as pd
import smtplib
from streamlit_autorefresh import st_autorefresh
from email.mime.text import MIMEText
from datetime import datetime
from exportar_pdf import exportar_rerpe_pdf
import os
from datetime import datetime
from PIL import Image
# Importa los estilos y el fondo login según lo que usarás
from utils import (
    aplicar_css_estilo_clasico,        # Solo si usarás el tema clásico
    aplicar_css_estilo_universitario,  # Solo si usarás el tema universitario
    aplicar_css_moderno_adaptativo,    # Tema moderno responsivo
    aplicar_css_fondo_login,           # Fondo con imagen en login
    aplicar_css_botones_sidebar        # Botones modernos en menú
)




# ==============================
# Conexión y Creación de Tablas
# ==============================

def conectar_db():
    conn = sqlite3.connect('delegados.db', check_same_thread=False)
    return conn

def crear_tablas(conn):

    cursor = conn.cursor()

    # Tabla de Usuarios con roles
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            rol TEXT NOT NULL CHECK (rol IN ('ADMIN', 'PROFESOR', 'ALUMNO')),
            vinculoId INTEGER,  -- Puede ser id del alumno o profesor
            FOREIGN KEY (vinculoId) REFERENCES alumnos(id)  -- solo si ALUMNO
            FOREIGN KEY (vinculoId) REFERENCES profesores(id) -- solo si PROFESOR
        )
    ''')



  # Tabla de Alumnos (extendida)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            codigoAlumno TEXT NOT NULL UNIQUE,
            programaEstudio TEXT NOT NULL
        )
    ''')

    
    # Tabla de Profesores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profesores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT UNIQUE NOT NULL
        )
    ''')

    
        # Tabla de Asignaturas con relación a profesor
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS asignaturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            codigoAsignatura TEXT NOT NULL UNIQUE,
            profesorId INTEGER NOT NULL,
            FOREIGN KEY (profesorId) REFERENCES profesores(id)
        )
    ''')

    
    # Tabla de relación muchos a muchos entre alumnos y asignaturas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alumno_asignatura (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alumnoId INTEGER NOT NULL,
            asignaturaId INTEGER NOT NULL,
            FOREIGN KEY (alumnoId) REFERENCES alumnos(id),
            FOREIGN KEY (asignaturaId) REFERENCES asignaturas(id),
            UNIQUE (alumnoId, asignaturaId)
        )
    ''')
     


    # Tabla para postulaciones de delegados voluntarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS postulaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alumnoId INTEGER NOT NULL,
            asignaturaId INTEGER NOT NULL,
            estado TEXT DEFAULT 'PENDIENTE',
            FOREIGN KEY (alumnoId) REFERENCES alumnos(id),
            FOREIGN KEY (asignaturaId) REFERENCES asignaturas(id)
        )
    ''')

    # Tabla de Elecciones (por asignatura)
    # Asegúrate de que esta sea la tabla actualizada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS elecciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asignaturaId INTEGER NOT NULL,
            fechaEleccion TEXT NOT NULL,
            metodo TEXT NOT NULL DEFAULT 'VOTACION',  -- nuevo campo
            estado TEXT DEFAULT 'ACTIVA',
            totalVotantes INTEGER DEFAULT 0,
            votosDelegado INTEGER DEFAULT 0,
            votosSubdelegado INTEGER DEFAULT 0,
            abstenciones INTEGER DEFAULT 0,
            FOREIGN KEY (asignaturaId) REFERENCES asignaturas(id)
        )
    ''')

    
    # Tabla de EleccionesDetalle
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS elecciones_detalle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            eleccionId INTEGER NOT NULL,
            alumnoId INTEGER NOT NULL,
            rol TEXT NOT NULL,
            votosObtenidos INTEGER DEFAULT 0,
            FOREIGN KEY (eleccionId) REFERENCES elecciones(id),
            FOREIGN KEY (alumnoId) REFERENCES alumnos(id)
        )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS registro_votos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        eleccionId INTEGER NOT NULL,
        alumnoId INTEGER NOT NULL,
        rol TEXT NOT NULL,
        fechaVoto TEXT NOT NULL,
        UNIQUE (eleccionId, alumnoId, rol),
        FOREIGN KEY (eleccionId) REFERENCES elecciones(id),
        FOREIGN KEY (alumnoId) REFERENCES alumnos(id)
        )
    ''')


    # Si ya teníamos la tabla de candidatos (registro individual), podríamos reutilizarla.
    # Para este ejemplo, se usa 'alumnos' para registrar a los candidatos en cada elección.
    conn.commit()

# ====================
# Función de Notificación
# ====================

def enviar_email(destinatario, asunto, mensaje):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    remitente = "tucorreo@gmail.com"  # Cambiar por el correo real
    password = "tu_contraseña"         # Mejor usar variables de entorno
    
    msg = MIMEText(mensaje)
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destinatario

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(remitente, password)
        server.sendmail(remitente, [destinatario], msg.as_string())
        server.quit()
        st.success(f"Correo enviado a {destinatario}")
    except Exception as e:
        st.error(f"Error al enviar el correo: {e}")

# ==========================
# Módulos de la Aplicación
# ==========================

def registro_alumno_module(conn):
    st.header("👨‍🎓 Registro de Alumno")
    cursor = conn.cursor()

    with st.form("form_alumno", clear_on_submit=True):
        nombre = st.text_input("Apellidos y Nombres")
        codigoAlumno = st.text_input("Código de Alumno")
        telefono = st.text_input("Teléfono fijo")
        celular = st.text_input("Celular")
        email = st.text_input("Correo electrónico")

        enviar = st.form_submit_button("Registrar Alumno")
        if enviar:
            if nombre and codigoAlumno:
                try:
                    cursor.execute('''
                        INSERT INTO alumnos (nombre, codigoAlumno, telefono, celular, email)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (nombre, codigoAlumno, telefono, celular, email))
                    conn.commit()
                    st.success("Alumno registrado correctamente.")
                except sqlite3.IntegrityError:
                    st.error("El código de alumno ya existe.")
            else:
                st.error("Completa los campos obligatorios: nombre y código.")

    if st.session_state["usuario"]["rol"] == "ADMIN":
        st.subheader("📋 Lista de Alumnos Registrados")
        cursor.execute("SELECT id, nombre, codigoAlumno, telefono, celular, email FROM alumnos")
        alumnos = cursor.fetchall()
        if alumnos:
            import pandas as pd
            df = pd.DataFrame(alumnos, columns=["ID", "Nombre", "Código", "Teléfono", "Celular", "Email"])
            st.dataframe(df, use_container_width=True)

            # Eliminar alumno
            id_borrar = st.number_input("ID de alumno a eliminar", min_value=1, step=1, key="borrar_alumno")
            if st.button("❌ Eliminar Alumno"):
                cursor.execute("DELETE FROM alumnos WHERE id = ?", (id_borrar,))
                conn.commit()
                st.success("Alumno eliminado.")
                st.rerun()

            # Editar alumno
            st.markdown("---")
            id_editar = st.number_input("ID de alumno a editar", min_value=1, step=1, key="editar_alumno")
            cursor.execute("SELECT nombre, codigoAlumno, telefono, celular, email FROM alumnos WHERE id = ?", (id_editar,))
            alumno = cursor.fetchone()
            if alumno:
                with st.form("form_editar_alumno"):
                    nuevo_nombre = st.text_input("Nuevo nombre", value=alumno[0], key="nuevo_nombre")
                    nuevo_codigo = st.text_input("Nuevo código", value=alumno[1], key="nuevo_codigo")
                    nuevo_telefono = st.text_input("Nuevo teléfono", value=alumno[2], key="nuevo_telefono")
                    nuevo_celular = st.text_input("Nuevo celular", value=alumno[3], key="nuevo_celular")
                    nuevo_email = st.text_input("Nuevo email", value=alumno[4], key="nuevo_email")
                    guardar = st.form_submit_button("Guardar Cambios")
                    if guardar:
                        try:
                            cursor.execute('''
                                UPDATE alumnos
                                SET nombre = ?, codigoAlumno = ?, telefono = ?, celular = ?, email = ?
                                WHERE id = ?
                            ''', (nuevo_nombre, nuevo_codigo, nuevo_telefono, nuevo_celular, nuevo_email, id_editar))
                            conn.commit()
                            st.success("✅ Alumno actualizado correctamente.")
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.error("❌ El código de alumno ya existe.")
        else:
            st.info("No hay alumnos registrados.")
#==================================================================

def registro_asignatura_module(conn):
    st.header("📚 Registro de Asignatura")
    cursor = conn.cursor()
    usuario = st.session_state['usuario']

    with st.form("form_asignatura", clear_on_submit=True):
        nombre = st.text_input("Nombre de la Asignatura")
        codigo = st.text_input("Código de la Asignatura")

        profesorId = None

        if usuario['rol'] == "ADMIN":
            cursor.execute("SELECT id, nombre FROM profesores")
            profesores = cursor.fetchall()
            if profesores:
                seleccion = st.selectbox(
                    "Selecciona Profesor",
                    options=[f"{nombre} (ID: {id})" for id, nombre in profesores]
                )
                profesorId = int(seleccion.split("ID: ")[1].replace(")", ""))
            else:
                st.warning("No hay profesores registrados.")
                profesorId = None

        elif usuario['rol'] == "PROFESOR":
            profesorId = usuario['vinculoId']

        enviar = st.form_submit_button("Registrar Asignatura")

        if enviar:
            if nombre.strip() and codigo.strip() and profesorId:
                try:
                    print("DEBUG → nombre:", nombre)
                    print("DEBUG → codigo:", codigo)
                    print("DEBUG → profesorId:", profesorId)
                    cursor.execute('''
                        INSERT INTO asignaturas (nombre, codigoAsignatura, profesorId)
                        VALUES (?, ?, ?)
                    ''', (nombre.strip(), codigo.strip(), profesorId))
                    conn.commit()
                    st.success("Asignatura registrada correctamente.")
                except sqlite3.IntegrityError as e:
                    st.error("Error: ese código de asignatura ya existe o profesor no válido.")
                    st.exception(e)
            else:
                st.warning("Completa todos los campos.")
#===============================================================
def registro_profesor_module(conn):
    st.header("👨‍🏫 Registro de Profesor")
    cursor = conn.cursor()

    with st.form("form_profesor", clear_on_submit=True):
        nombre = st.text_input("Nombre del Profesor")
        correo = st.text_input("Correo del Profesor")
        enviar = st.form_submit_button("Registrar Profesor")

        if enviar:
            if nombre and correo:
                try:
                    cursor.execute('''
                        INSERT INTO profesores (nombre, correo)
                        VALUES (?, ?)
                    ''', (nombre, correo))
                    conn.commit()
                    st.success("Profesor registrado correctamente.")
                except sqlite3.IntegrityError:
                    st.error("Ese correo ya está registrado.")
            else:
                st.warning("Completa todos los campos.")

    if st.session_state["usuario"]["rol"] == "ADMIN":
        st.subheader("📋 Profesores Registrados")
        cursor.execute("SELECT id, nombre, correo FROM profesores")
        profesores = cursor.fetchall()
        if profesores:
            import pandas as pd
            df = pd.DataFrame(profesores, columns=["ID", "Nombre", "Correo"])
            st.dataframe(df, use_container_width=True)

            id_eliminar = st.number_input("ID de profesor a eliminar", min_value=1, step=1, key="profesor_borrar")
            if st.button("❌ Eliminar Profesor"):
                cursor.execute("DELETE FROM profesores WHERE id = ?", (id_eliminar,))
                conn.commit()
                st.success("Profesor eliminado.")
                st.rerun()

            st.markdown("---")
            id_editar = st.number_input("ID de profesor a editar", min_value=1, step=1, key="profesor_editar")
            cursor.execute("SELECT nombre, correo FROM profesores WHERE id = ?", (id_editar,))
            profesor = cursor.fetchone()
            if profesor:
                with st.form("form_editar_profesor"):
                    nuevo_nombre = st.text_input("Nuevo nombre", value=profesor[0], key="nuevo_nombre_profesor")
                    nuevo_correo = st.text_input("Nuevo correo", value=profesor[1], key="nuevo_correo_profesor")
                    guardar = st.form_submit_button("Guardar Cambios")
                    if guardar:
                        try:
                            cursor.execute('''
                                UPDATE profesores
                                SET nombre = ?, correo = ?
                                WHERE id = ?
                            ''', (nuevo_nombre, nuevo_correo, id_editar))
                            conn.commit()
                            st.success("✅ Profesor actualizado correctamente.")
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.error("❌ El correo ya está registrado.")
        else:
            st.info("No hay profesores registrados.")
#===============================================================

def registro_usuario_module(conn):
    st.header("👤 Registro de Usuario del Sistema")
    cursor = conn.cursor()

    with st.form("form_usuario", clear_on_submit=True):
        username = st.text_input("Nombre de Usuario (único)")
        password = st.text_input("Contraseña", type="password")
        rol = st.selectbox("Rol del Usuario", ["ADMIN", "PROFESOR", "ALUMNO"])

        vinculoId = None
        if rol == "ALUMNO":
            cursor.execute("SELECT id, nombre FROM alumnos")
            alumnos = cursor.fetchall()
            if alumnos:
                opciones = {f"{nombre} (ID: {id})": id for id, nombre in alumnos}
                seleccion = st.selectbox("Selecciona el Alumno asociado", list(opciones.keys()))
                vinculoId = opciones[seleccion]
            else:
                st.warning("No hay alumnos registrados para vincular.")

        submit = st.form_submit_button("Registrar Usuario")
        if submit:
            try:
                cursor.execute('''
                    INSERT INTO usuarios (username, password, rol, vinculoId)
                    VALUES (?, ?, ?, ?)
                ''', (username, password, rol, vinculoId))
                conn.commit()
                st.success(f"Usuario '{username}' registrado correctamente como {rol}.")
            except sqlite3.IntegrityError:
                st.error("El nombre de usuario ya está en uso.")

    if st.session_state["usuario"]["rol"] == "ADMIN":
        st.subheader("📋 Usuarios Registrados")
        cursor.execute("SELECT id, username, rol, vinculoId FROM usuarios")
        usuarios = cursor.fetchall()
        if usuarios:
            import pandas as pd
            df = pd.DataFrame(usuarios, columns=["ID", "Usuario", "Rol", "VinculoId"])
            st.dataframe(df, use_container_width=True)

            id_eliminar = st.number_input("ID de usuario a eliminar", min_value=1, step=1, key="usuario_borrar")
            if st.button("❌ Eliminar Usuario"):
                cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_eliminar,))
                conn.commit()
                st.success("Usuario eliminado.")
                st.rerun()

            st.markdown("---")
            id_editar = st.number_input("ID de usuario a editar", min_value=1, step=1, key="usuario_editar")
            cursor.execute("SELECT username, password, rol FROM usuarios WHERE id = ?", (id_editar,))
            usuario = cursor.fetchone()
            if usuario:
                with st.form("form_editar_usuario"):
                    nuevo_username = st.text_input("Nuevo username", value=usuario[0], key="nuevo_usuario")
                    nueva_contra = st.text_input("Nueva contraseña", value=usuario[1], key="nueva_contra")
                    nuevo_rol = st.selectbox("Nuevo rol", ["ADMIN", "PROFESOR", "ALUMNO"], index=["ADMIN", "PROFESOR", "ALUMNO"].index(usuario[2]), key="nuevo_rol")
                    guardar = st.form_submit_button("Guardar Cambios")
                    if guardar:
                        try:
                            cursor.execute('''
                                UPDATE usuarios
                                SET username = ?, password = ?, rol = ?
                                WHERE id = ?
                            ''', (nuevo_username, nueva_contra, nuevo_rol, id_editar))
                            conn.commit()
                            st.success("✅ Usuario actualizado correctamente.")
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.error("❌ El username ya está en uso.")
        else:
            st.info("No hay usuarios registrados.")
#==============================================================
def registro_profesor_con_usuario_module(conn):
    st.header("👨‍🏫 Registro de Profesor con Cuenta de Usuario")

    with st.form("form_profesor_usuario", clear_on_submit=True):
        nombre = st.text_input("Nombre del Profesor")
        correo = st.text_input("Correo del Profesor")
        username = st.text_input("Nombre de Usuario para el Profesor")
        password = st.text_input("Contraseña", type="password")
        enviar = st.form_submit_button("Registrar Profesor y Usuario")

        if enviar:
            if nombre and correo and username and password:
                cursor = conn.cursor()

                try:
                    # 1. Registrar profesor
                    cursor.execute('''
                        INSERT INTO profesores (nombre, correo)
                        VALUES (?, ?)
                    ''', (nombre, correo))
                    conn.commit()
                    profesor_id = cursor.lastrowid

                    # 2. Crear usuario vinculado al profesor
                    cursor.execute('''
                        INSERT INTO usuarios (username, password, rol, vinculoId)
                        VALUES (?, ?, 'PROFESOR', ?)
                    ''', (username, password, profesor_id))
                    conn.commit()

                    st.success("Profesor y cuenta de usuario registrados correctamente.")
                except sqlite3.IntegrityError as e:
                    st.error("Error: Ese correo o nombre de usuario ya está registrado.")
            else:
                st.warning("Completa todos los campos.")
#===============================================================
# Modulo asociar alumno  asignatura modulo 
def asociar_alumno_asignatura_module(conn):
    st.header("🔗 Asociar Alumno a Asignatura")
    cursor = conn.cursor()

    if "usuario" not in st.session_state:
        st.warning("Inicia sesión para continuar.")
        return

    usuario = st.session_state["usuario"]
    rol = usuario["rol"]

    # Filtrar asignaturas según el rol
    if rol == "PROFESOR":
        profesor_id = usuario.get("vinculoId", None)
        if not profesor_id:
            st.error("⚠️ Tu cuenta no está vinculada a un profesor.")
            return
        cursor.execute("SELECT id, nombre FROM asignaturas WHERE profesorId = ?", (profesor_id,))
    else:
        cursor.execute("SELECT id, nombre FROM asignaturas")

    asignaturas = cursor.fetchall()

    if not asignaturas:
        st.info("No hay asignaturas disponibles para asociar.")
        return

    asignatura_dict = {f"{nombre} (ID: {id})": id for id, nombre in asignaturas}
    asignatura_sel = st.selectbox("Selecciona una asignatura", list(asignatura_dict.keys()))
    asignatura_id = asignatura_dict[asignatura_sel]

    st.subheader("👤 Asociar un nuevo alumno")

    # Alumnos no asociados aún
    cursor.execute('''
        SELECT id, nombre FROM alumnos
        WHERE id NOT IN (
            SELECT alumnoId FROM alumno_asignatura WHERE asignaturaId = ?
        )
    ''', (asignatura_id,))
    alumnos_disponibles = cursor.fetchall()

    if alumnos_disponibles:
        alumno_dict = {f"{a[1]} (ID: {a[0]})": a[0] for a in alumnos_disponibles}
        alumno_sel = st.selectbox("Selecciona un alumno para asociar", list(alumno_dict.keys()))

        if st.button("📎 Asociar Alumno"):
            try:
                cursor.execute('''
                    INSERT INTO alumno_asignatura (alumnoId, asignaturaId)
                    VALUES (?, ?)
                ''', (alumno_dict[alumno_sel], asignatura_id))
                conn.commit()
                st.success("✅ Alumno asociado correctamente.")
                st.rerun()
            except sqlite3.IntegrityError:
                st.warning("⚠️ Este alumno ya está asociado.")
    else:
        st.info("Todos los alumnos ya están asociados a esta asignatura.")

    st.subheader("📋 Alumnos ya asociados")
    # Mostrar alumnos ya asociados
    cursor.execute('''
        SELECT a.id, a.nombre, a.codigoAlumno
        FROM alumnos a
        JOIN alumno_asignatura aa ON a.id = aa.alumnoId
        WHERE aa.asignaturaId = ?
    ''', (asignatura_id,))
    alumnos_asociados = cursor.fetchall()

    if alumnos_asociados:
        for alumno_id, nombre, codigo in alumnos_asociados:
            col1, col2, col3 = st.columns([4, 3, 2])
            col1.markdown(f"**{nombre}** (`{codigo}`)")
            with col3:
                if st.button(f"❌ Quitar", key=f"quitar_{alumno_id}"):
                    cursor.execute('''
                        DELETE FROM alumno_asignatura
                        WHERE alumnoId = ? AND asignaturaId = ?
                    ''', (alumno_id, asignatura_id))
                    conn.commit()
                    st.success(f"Alumno {nombre} fue desvinculado.")
                    st.rerun()
    else:
        st.info("Aún no hay alumnos asociados a esta asignatura.")
######===========================================================
def crear_eleccion_module(conn):
    st.header("🗳️ Crear Elección")
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre FROM asignaturas")
    asignaturas = cursor.fetchall()

    if asignaturas:
        opciones = {nombre: id for id, nombre in asignaturas}
        asignatura_seleccionada = st.selectbox("📘 Selecciona la Asignatura", list(opciones.keys()))
        metodo = st.selectbox("⚙️ Método de elección", ["VOTACION", "ALEATORIO", "VOLUNTARIO"])

        if st.button("✅ Crear Elección"):
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            asignatura_id = opciones[asignatura_seleccionada]

            cursor.execute('''
                INSERT INTO elecciones (asignaturaId, fechaEleccion, metodo, estado)
                VALUES (?, ?, ?, 'ACTIVA')
            ''', (asignatura_id, fecha, metodo))
            conn.commit()

            st.success(f"✅ Elección creada con método: {metodo}")

            # Si el método es aleatorio, hacer la selección
            if metodo == "ALEATORIO":
                st.subheader("🎡 Selección Aleatoria con Ruleta Visual")
                cursor.execute('''
                    SELECT alumnos.id, alumnos.nombre
                    FROM alumnos
                    JOIN alumno_asignatura aa ON alumnos.id = aa.alumnoId
                    WHERE aa.asignaturaId = ?
                ''', (asignatura_id,))
                alumnos = cursor.fetchall()

                if len(alumnos) < 2:
                    st.warning("⚠️ Se requieren al menos 2 alumnos para usar el método aleatorio.")
                    return

                nombres = [a[1] for a in alumnos]
                id_dict = {a[1]: a[0] for a in alumnos}

                # Ruleta visual para Delegado
                delegado_nombre = random.choice(nombres)
                with st.spinner("🎯 Seleccionando delegado..."):
                    for _ in range(15):
                        st.write("🎡", random.choice(nombres))
                        time.sleep(0.1)
                st.success(f"🎉 Delegado seleccionado: **{delegado_nombre}**")

                # Ruleta visual para Subdelegado
                nombres_sub = [n for n in nombres if n != delegado_nombre]
                subdelegado_nombre = random.choice(nombres_sub)
                with st.spinner("🎯 Seleccionando subdelegado..."):
                    for _ in range(15):
                        st.write("🎡", random.choice(nombres_sub))
                        time.sleep(0.1)
                st.success(f"🎉 Subdelegado seleccionado: **{subdelegado_nombre}**")

                # Insertar en elecciones_detalle
                eleccion_id = cursor.lastrowid
                cursor.execute('''
                    INSERT INTO elecciones_detalle (eleccionId, alumnoId, rol, votosObtenidos)
                    VALUES (?, ?, 'DELEGADO', ?)
                ''', (eleccion_id, id_dict[delegado_nombre], random.randint(3, 10)))  # votos ficticios

                cursor.execute('''
                    INSERT INTO elecciones_detalle (eleccionId, alumnoId, rol, votosObtenidos)
                    VALUES (?, ?, 'SUBDELEGADO', ?)
                ''', (eleccion_id, id_dict[subdelegado_nombre], random.randint(1, 8)))

                # Marcar elección como inactiva
                cursor.execute('''
                    UPDATE elecciones SET estado = 'INACTIVA', totalVotantes = 1
                    WHERE id = ?
                ''', (eleccion_id,))
                conn.commit()

                st.success("✅ Elección finalizada automáticamente y marcada como INACTIVA.")
    else:
        st.info("Primero debes registrar una asignatura.")
#===========================================================================================================
def votacion_module(conn):
    st.header("🗳️ Módulo de Elecciones por Asignatura")
    cursor = conn.cursor()

    usuario = st.session_state["usuario"]
    if usuario["rol"] != "ALUMNO":
        st.warning("Este módulo es solo para alumnos.")
        return

    alumno_id = usuario["vinculoId"]

    cursor.execute('''
        SELECT e.id, a.nombre, e.metodo
        FROM elecciones e
        JOIN asignaturas a ON e.asignaturaId = a.id
        JOIN alumno_asignatura aa ON aa.asignaturaId = e.asignaturaId
        WHERE aa.alumnoId = ?
        ORDER BY e.fechaEleccion DESC
    ''', (alumno_id,))
    elecciones = cursor.fetchall()

    if not elecciones:
        st.info("No tienes elecciones activas en tus asignaturas.")
        return

    elecciones_dict = {f"{nombre} - {metodo} (ID: {id})": id for id, nombre, metodo in elecciones}
    eleccion_sel = st.selectbox("Selecciona la elección:", list(elecciones_dict.keys()))
    eleccion_id = elecciones_dict[eleccion_sel]

    cursor.execute('''
        SELECT e.asignaturaId, e.metodo, e.estado, a.nombre, p.nombre, e.esDesempate
        FROM elecciones e
        JOIN asignaturas a ON e.asignaturaId = a.id
        JOIN profesores p ON a.profesorId = p.id
        WHERE e.id = ?
    ''', (eleccion_id,))
    eleccion_data = cursor.fetchone()
    asignatura_id, metodo, estado, asig_nombre, profesor_nombre, es_desempate = eleccion_data

    st.write(f"📘 **Asignatura:** {asig_nombre}")
    st.write(f"👨‍🏫 **Profesor:** {profesor_nombre}")
    st.write(f"⚙️ **Método de Elección:** {metodo}")
    st.write(f"🔒 **Estado:** {'ACTIVA' if estado == 'ACTIVA' else 'INACTIVA'}")
    if es_desempate:
        st.markdown("📌 **Esta es una elección de desempate (segunda ronda)**")

    # =========================
    # MOSTRAR RESULTADO FINAL
    # =========================
    if estado == "INACTIVA":
        # Verificar si la elección tiene registros en empates
        cursor.execute("SELECT COUNT(*) FROM empates WHERE eleccionId = ?", (eleccion_id,))
        tiene_empates = cursor.fetchone()[0] > 0

        if tiene_empates:
            st.warning("⚠️ Esta elección terminó en empate. Se está a la espera de una nueva votación de desempate.")
            return

        # Mostrar delegado y subdelegado
        st.info("📌 La elección está cerrada. A continuación se muestran los resultados finales:")
        cursor.execute('''
            SELECT al.nombre, ed.rol
            FROM elecciones_detalle ed
            JOIN alumnos al ON ed.alumnoId = al.id
            WHERE ed.eleccionId = ?
        ''', (eleccion_id,))
        resultados = cursor.fetchall()

        roles_vistos = set()
        for nombre, rol in resultados:
            if rol not in roles_vistos:
                st.markdown(f"**{rol}**: {nombre}")
                roles_vistos.add(rol)
        return

    # =========================
    # SI ESTÁ ACTIVA → VOTACIÓN
    # =========================
    if metodo == "VOTACION":
        st.subheader("🗳️ Votación por candidato")
        codigo_alumno = st.text_input("Tu código de alumno")

        if codigo_alumno:
            cursor.execute("SELECT id, nombre FROM alumnos WHERE codigoAlumno = ?", (codigo_alumno,))
            alumno = cursor.fetchone()
            if alumno:
                alumno_id_confirmado, nombre = alumno
                cursor.execute("SELECT * FROM alumno_asignatura WHERE alumnoId = ? AND asignaturaId = ?", (alumno_id_confirmado, asignatura_id))
                if cursor.fetchone():
                    if es_desempate:
                        cursor.execute('''
                            SELECT al.id, al.nombre
                            FROM elecciones_detalle ed
                            JOIN alumnos al ON ed.alumnoId = al.id
                            WHERE ed.eleccionId = ?
                        ''', (eleccion_id,))
                    else:
                        cursor.execute('''
                            SELECT al.id, al.nombre
                            FROM alumno_asignatura aa
                            JOIN alumnos al ON aa.alumnoId = al.id
                            WHERE aa.asignaturaId = ?
                        ''', (asignatura_id,))
                    candidatos = cursor.fetchall()

                    if candidatos:
                        opciones = {nombre: id for id, nombre in candidatos}
                        candidato_sel = st.selectbox("Selecciona candidato:", list(opciones.keys()))
                        rol_sel = st.selectbox("Rol:", ["DELEGADO", "SUBDELEGADO"])

                        if st.button("Votar"):
                            cursor.execute('''
                                SELECT id FROM registro_votos
                                WHERE eleccionId = ? AND alumnoId = ? AND rol = ?
                            ''', (eleccion_id, alumno_id_confirmado, rol_sel))
                            ya_voto = cursor.fetchone()

                            if ya_voto:
                                st.warning(f"⚠️ Ya votaste como {rol_sel} en esta elección.")
                                return

                            candidato_id = opciones[candidato_sel]

                            cursor.execute('''
                                SELECT id FROM elecciones_detalle
                                WHERE eleccionId = ? AND alumnoId = ? AND rol = ?
                            ''', (eleccion_id, candidato_id, rol_sel))
                            ya_existe = cursor.fetchone()

                            if ya_existe:
                                cursor.execute("UPDATE elecciones_detalle SET votosObtenidos = votosObtenidos + 1 WHERE id = ?", (ya_existe[0],))
                            else:
                                cursor.execute('''
                                    INSERT INTO elecciones_detalle (eleccionId, alumnoId, rol, votosObtenidos)
                                    VALUES (?, ?, ?, 1)
                                ''', (eleccion_id, candidato_id, rol_sel))

                            cursor.execute('''
                                INSERT INTO registro_votos (eleccionId, alumnoId, rol, fechaVoto)
                                VALUES (?, ?, ?, datetime('now'))
                            ''', (eleccion_id, alumno_id_confirmado, rol_sel))

                            if rol_sel == "DELEGADO":
                                cursor.execute('''
                                    UPDATE elecciones SET votosDelegado = votosDelegado + 1, totalVotantes = totalVotantes + 1
                                    WHERE id = ?
                                ''', (eleccion_id,))
                            else:
                                cursor.execute('''
                                    UPDATE elecciones SET votosSubdelegado = votosSubdelegado + 1, totalVotantes = totalVotantes + 1
                                    WHERE id = ?
                                ''', (eleccion_id,))

                            conn.commit()
                            st.success(f"✅ Voto registrado para {candidato_sel} como {rol_sel}")
                    else:
                        st.warning("⚠️ No hay candidatos registrados.")
                else:
                    st.error("No estás inscrito en esta asignatura.")
            else:
                st.error("Código de alumno incorrecto.")
                
    elif metodo == "ALEATORIO":
        st.subheader("🎲 Selección aleatoria")
        if st.button("Seleccionar delegado al azar"):
            cursor.execute('''
                SELECT alumnos.id, alumnos.nombre FROM alumnos
                JOIN alumno_asignatura aa ON alumnos.id = aa.alumnoId
                WHERE aa.asignaturaId = ?
            ''', (asignatura_id,))
            posibles = cursor.fetchall()
            if posibles:
                import random
                elegido = random.choice(posibles)
                elegido_id, nombre = elegido

                cursor.execute("INSERT INTO elecciones_detalle (eleccionId, alumnoId, rol, votosObtenidos) VALUES (?, ?, 'DELEGADO', 1)", (eleccion_id, elegido_id))
                conn.commit()
                st.success(f"🎉 Delegado seleccionado al azar: {nombre}")
                st.rerun()
            else:
                st.warning("No hay alumnos inscritos.")

    elif metodo == "VOLUNTARIO":
        st.subheader("✋ Postulación voluntaria")

        # Asegurarse que la tabla tenga la columna "rol"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS postulaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alumnoId INTEGER,
                asignaturaId INTEGER,
                estado TEXT DEFAULT 'PENDIENTE',
                rol TEXT DEFAULT 'DELEGADO',
                FOREIGN KEY (alumnoId) REFERENCES alumnos(id),
                FOREIGN KEY (asignaturaId) REFERENCES asignaturas(id)
            )
        ''')

        # Consultar si ya hay postulaciones para el alumno
        cursor.execute('''
            SELECT rol, estado FROM postulaciones
            WHERE alumnoId = ? AND asignaturaId = ?
        ''', (alumno_id, asignatura_id))
        postulaciones = cursor.fetchall()

        if postulaciones:
            st.markdown("📋 Ya te postulaste:")
            for rol, estado in postulaciones:
                st.info(f"🔹 Como {rol}: Estado actual → **{estado}**")
        else:
            st.success("✅ Aún no te postulaste a ningún rol.")

        st.markdown("### 📝 Nueva postulación")
        rol_postulacion = st.selectbox("¿A qué rol deseas postularte?", ["DELEGADO", "SUBDELEGADO"])

        if st.button("📨 Postularme"):
            cursor.execute('''
                SELECT 1 FROM postulaciones
                WHERE alumnoId = ? AND asignaturaId = ? AND rol = ?
            ''', (alumno_id, asignatura_id, rol_postulacion))
            ya_postulado = cursor.fetchone()

            if ya_postulado:
                st.warning(f"⚠️ Ya te postulaste como {rol_postulacion}.")
            else:
                cursor.execute('''
                    INSERT INTO postulaciones (alumnoId, asignaturaId, estado, rol)
                    VALUES (?, ?, 'PENDIENTE', ?)
                ''', (alumno_id, asignatura_id, rol_postulacion))
                conn.commit()
                st.success(f"Tu postulación como **{rol_postulacion}** ha sido registrada.")



#=======================================================================================000
def gestionar_elecciones_profesor(conn):
    st.header("📋 Gestión de Elecciones por Asignatura")
    cursor = conn.cursor()

    if "usuario" not in st.session_state or st.session_state["usuario"]["rol"] != "PROFESOR":
        st.warning("Este módulo es exclusivo para profesores.")
        return

    profesor_id = st.session_state["usuario"].get("vinculoId")
    if not profesor_id:
        st.error("Tu cuenta no está vinculada a un profesor.")
        return

    # 🔧 Reparar empates no registrados en elecciones antiguas
    cursor.execute('''
        SELECT id, asignaturaId
        FROM elecciones
        WHERE estado = 'INACTIVA' AND esDesempate = 0
    ''')
    elecciones = cursor.fetchall()

    for eleccion_id, _ in elecciones:
        for rol in ["DELEGADO", "SUBDELEGADO"]:
            cursor.execute('''
                SELECT alumnoId, votosObtenidos
                FROM elecciones_detalle
                WHERE eleccionId = ? AND rol = ?
                ORDER BY votosObtenidos DESC
            ''', (eleccion_id, rol))
            resultados = cursor.fetchall()
            if not resultados:
                continue
            max_votos = resultados[0][1]
            empatados = [r for r in resultados if r[1] == max_votos]
            if len(empatados) > 1:
                for alumno_id, votos in empatados:
                    cursor.execute('''
                        SELECT 1 FROM empates
                        WHERE eleccionId = ? AND alumnoId = ? AND rol = ?
                    ''', (eleccion_id, alumno_id, rol))
                    ya_existe = cursor.fetchone()
                    if not ya_existe:
                        cursor.execute('''
                            INSERT INTO empates (eleccionId, alumnoId, rol, votos)
                            VALUES (?, ?, ?, ?)
                        ''', (eleccion_id, alumno_id, rol, votos))
    conn.commit()

    # Obtener elecciones del profesor
    cursor.execute('''
        SELECT e.id, a.nombre, e.fechaEleccion, e.metodo, e.estado, e.esDesempate
        FROM elecciones e
        JOIN asignaturas a ON e.asignaturaId = a.id
        WHERE a.profesorId = ?
        ORDER BY e.fechaEleccion DESC
    ''', (profesor_id,))
    elecciones = cursor.fetchall()

    if not elecciones:
        st.info("No hay elecciones creadas aún para tus asignaturas.")
        return

    for eleccion_id, asig_nombre, fecha, metodo, estado, es_desempate in elecciones:
        etiqueta = "🌀 [Desempate]" if es_desempate else ""
        with st.expander(f"📘 {asig_nombre} {etiqueta} ({metodo}) — {fecha[:10]} — Estado: {estado}"):
            col1, col2 = st.columns([2, 1])
            col1.markdown(f"**Método:** {metodo}  \n**Estado actual:** `{estado}`")

            if es_desempate:
                col1.markdown("📌 **Esta es una elección de desempate (segunda ronda)**")

            if estado == "ACTIVA":
                if col2.button("🔒 Desactivar", key=f"desactivar_{eleccion_id}"):
                    cursor.execute("UPDATE elecciones SET estado = 'INACTIVA' WHERE id = ?", (eleccion_id,))
                    conn.commit()
                    st.success("Elección desactivada.")
                    st.rerun()
            else:
                if col2.button("🔓 Activar", key=f"activar_{eleccion_id}"):
                    cursor.execute("UPDATE elecciones SET estado = 'ACTIVA' WHERE id = ?", (eleccion_id,))
                    conn.commit()
                    st.success("Elección activada.")
                    st.rerun()

            # Empates detectados
            cursor.execute("SELECT COUNT(*) FROM empates WHERE eleccionId = ?", (eleccion_id,))
            tiene_empates = cursor.fetchone()[0] > 0

            if tiene_empates:
                st.markdown("---")
                st.markdown("### ⚖️ Empates registrados")

                for rol in ["DELEGADO", "SUBDELEGADO"]:
                    cursor.execute('''
                        SELECT al.nombre, al.codigoAlumno, em.votos
                        FROM empates em
                        JOIN alumnos al ON em.alumnoId = al.id
                        WHERE em.eleccionId = ? AND em.rol = ?
                    ''', (eleccion_id, rol))
                    empatados = cursor.fetchall()
                    if empatados:
                        st.markdown(f"**{rol}:**")
                        for nombre, codigo, votos in empatados:
                            st.info(f"{nombre} ({codigo}) — {votos} votos")
                    else:
                        st.info(f"No hay empates para {rol}.")

                if st.button("🚀 Crear nueva elección de desempate", key=f"desempate_{eleccion_id}"):
                    cursor.execute("SELECT asignaturaId FROM elecciones WHERE id = ?", (eleccion_id,))
                    asignatura = cursor.fetchone()
                    if asignatura:
                        asignatura_id = asignatura[0]
                        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        cursor.execute('''
                            INSERT INTO elecciones (
                                asignaturaId, fechaEleccion, totalVotantes,
                                votosDelegado, votosSubdelegado, abstenciones,
                                estado, metodo, esDesempate
                            )
                            VALUES (?, ?, 0, 0, 0, 0, 'ACTIVA', 'VOTACION', 1)
                        ''', (asignatura_id, fecha_actual))
                        nueva_eleccion_id = cursor.lastrowid

                        cursor.execute('''
                            SELECT alumnoId, rol FROM empates WHERE eleccionId = ?
                        ''', (eleccion_id,))
                        empatados = cursor.fetchall()
                        for alumno_id, rol in empatados:
                            cursor.execute('''
                                INSERT INTO elecciones_detalle (eleccionId, alumnoId, rol, votosObtenidos)
                                VALUES (?, ?, ?, 0)
                            ''', (nueva_eleccion_id, alumno_id, rol))

                        cursor.execute("DELETE FROM empates WHERE eleccionId = ?", (eleccion_id,))
                        conn.commit()

                        st.success(f"✅ Segunda elección de desempate creada (ID: {nueva_eleccion_id})")
                        st.rerun()

            # Opciones de eliminación
            st.markdown("---")
            st.markdown("### ⚠️ Eliminar esta elección")
            st.warning("Esta acción eliminará también los votos y postulaciones asociadas.")
            confirmar = st.checkbox(f"Confirmo eliminar elección ID {eleccion_id}", key=f"chk_{eleccion_id}")
            if st.button("🗑️ Eliminar elección", key=f"eliminar_{eleccion_id}") and confirmar:
                cursor.execute("DELETE FROM elecciones_detalle WHERE eleccionId = ?", (eleccion_id,))
                cursor.execute("DELETE FROM registro_votos WHERE eleccionId = ?", (eleccion_id,))
                cursor.execute("DELETE FROM postulaciones WHERE asignaturaId = (SELECT asignaturaId FROM elecciones WHERE id = ?)", (eleccion_id,))
                cursor.execute("DELETE FROM elecciones WHERE id = ?", (eleccion_id,))
                conn.commit()
                st.success("✅ Elección eliminada con éxito.")
                st.rerun()
##========================================================================================
def admin_panel_module(conn):
    st.header("📊 Panel de Administración de Elecciones")
    cursor = conn.cursor()

    # 🔧 BLOQUE DE REPARACIÓN AUTOMÁTICA
    def reparar_errores_delegado_duplicado():
        corregidas = 0
        cursor.execute('''
            SELECT e.id
            FROM elecciones e
            WHERE e.estado = 'INACTIVA'
        ''')
        elecciones = cursor.fetchall()

        for eleccion_id, in elecciones:
            cursor.execute('''
                SELECT alumnoId FROM elecciones_detalle
                WHERE eleccionId = ? AND rol = 'DELEGADO'
            ''', (eleccion_id,))
            delegado = cursor.fetchone()

            cursor.execute('''
                SELECT alumnoId FROM elecciones_detalle
                WHERE eleccionId = ? AND rol = 'SUBDELEGADO'
            ''', (eleccion_id,))
            subdelegado = cursor.fetchone()

            if delegado and subdelegado and delegado[0] == subdelegado[0]:
                cursor.execute('''
                    SELECT alumnoId, votosObtenidos
                    FROM elecciones_detalle
                    WHERE eleccionId = ? AND rol = 'SUBDELEGADO'
                    ORDER BY votosObtenidos DESC
                ''', (eleccion_id,))
                subdelegados = cursor.fetchall()
                for alumno_id, votos in subdelegados:
                    if alumno_id != delegado[0]:
                        cursor.execute('''
                            DELETE FROM elecciones_detalle
                            WHERE eleccionId = ? AND rol = 'SUBDELEGADO'
                        ''', (eleccion_id,))
                        cursor.execute('''
                            INSERT INTO elecciones_detalle (eleccionId, alumnoId, rol, votosObtenidos)
                            VALUES (?, ?, 'SUBDELEGADO', ?)
                        ''', (eleccion_id, alumno_id, votos))
                        conn.commit()
                        corregidas += 1
                        st.success(f"🛠️ Se corrigió elección ID {eleccion_id}. Nuevo subdelegado asignado.")
                        break
        if corregidas == 0:
            st.info("✔️ No se detectaron elecciones con errores de duplicación.")

    reparar_errores_delegado_duplicado()
    # FIN DEL BLOQUE DE REPARACIÓN
    # Luego continúa TODO tu código normal como ya lo tienes:
    cursor.execute('''
        SELECT e.id, a.nombre, a.codigoAsignatura, e.fechaEleccion,
               e.totalVotantes, e.votosDelegado, e.votosSubdelegado,
               e.abstenciones, e.estado, e.esDesempate
        FROM elecciones e
        JOIN asignaturas a ON e.asignaturaId = a.id
        ORDER BY e.fechaEleccion DESC
    ''')
    elecciones = cursor.fetchall()
    # ================================
    # 🛠️ BOTÓN MANUAL DE REPARACIÓN
    # ================================
    with st.expander("🛠️ Reparar elecciones con errores (delegado = subdelegado)"):
        if st.button("🔁 Ejecutar reparación manual"):
            corregidas = 0
            cursor.execute('''
                SELECT e.id
                FROM elecciones e
                WHERE e.estado = 'INACTIVA'
            ''')
            elecciones_error = cursor.fetchall()

            for eleccion_id, in elecciones_error:
                cursor.execute('''
                    SELECT alumnoId FROM elecciones_detalle
                    WHERE eleccionId = ? AND rol = 'DELEGADO'
                ''', (eleccion_id,))
                delegado = cursor.fetchone()

                cursor.execute('''
                    SELECT alumnoId FROM elecciones_detalle
                    WHERE eleccionId = ? AND rol = 'SUBDELEGADO'
                ''', (eleccion_id,))
                subdelegado = cursor.fetchone()

                if delegado and subdelegado and delegado[0] == subdelegado[0]:
                    # Buscar otro subdelegado posible
                    cursor.execute('''
                        SELECT alumnoId, votosObtenidos
                        FROM elecciones_detalle
                        WHERE eleccionId = ? AND rol = 'SUBDELEGADO'
                        ORDER BY votosObtenidos DESC
                    ''', (eleccion_id,))
                    candidatos = cursor.fetchall()
                    for alumno_id, votos in candidatos:
                        if alumno_id != delegado[0]:
                            cursor.execute('''
                                DELETE FROM elecciones_detalle
                                WHERE eleccionId = ? AND rol = 'SUBDELEGADO'
                            ''', (eleccion_id,))
                            cursor.execute('''
                                INSERT INTO elecciones_detalle (eleccionId, alumnoId, rol, votosObtenidos)
                                VALUES (?, ?, 'SUBDELEGADO', ?)
                            ''', (eleccion_id, alumno_id, votos))
                            conn.commit()
                            corregidas += 1
                            st.success(f"✅ Elección ID {eleccion_id}: subdelegado corregido.")
                            break
                    else:
                        st.warning(f"⚠️ Elección ID {eleccion_id}: no hay otro subdelegado válido.")
            if corregidas == 0:
                st.info("✔️ No se detectaron elecciones con errores de duplicación.")

    if elecciones:

        df = pd.DataFrame(elecciones, columns=[
            "ID", "Asignatura", "Código", "Fecha", "Total Votantes",
            "Votos Delegado", "Votos Subdelegado", "Abstenciones", "Estado", "Desempate"
        ])
        st.dataframe(df, use_container_width=True)

        st.markdown("---")
        st.subheader("📄 Acciones para una Elección")

        eleccion_id = st.number_input("ID de Elección", min_value=1, step=1)

        cursor.execute("SELECT estado, esDesempate, asignaturaId FROM elecciones WHERE id = ?", (eleccion_id,))
        fila = cursor.fetchone()
        if fila:
            estado_actual, es_desempate, asignatura_id = fila

            st.info(f"🔒 Estado actual: **{estado_actual}**")
            if es_desempate:
                st.markdown("📌 **Esta es una elección de desempate (segunda ronda)**")

            nuevo_estado = "INACTIVA" if estado_actual == "ACTIVA" else "ACTIVA"

            if st.button(f"Cambiar estado a {nuevo_estado}"):
                if nuevo_estado == "INACTIVA":

                    def obtener_top(rol):
                        cursor.execute('''
                            SELECT alumnoId, votosObtenidos
                            FROM elecciones_detalle
                            WHERE eleccionId = ? AND rol = ?
                            ORDER BY votosObtenidos DESC
                        ''', (eleccion_id, rol))
                        return cursor.fetchall()

                    def detectar_empate_y_registrar(lista, rol):
                        if not lista:
                            return False
                        max_votos = lista[0][1]
                        empatados = [item for item in lista if item[1] == max_votos]
                        if len(empatados) > 1:
                            for alumno_id, votos in empatados:
                                cursor.execute('''
                                    SELECT 1 FROM empates
                                    WHERE eleccionId = ? AND alumnoId = ? AND rol = ?
                                ''', (eleccion_id, alumno_id, rol))
                                ya_existe = cursor.fetchone()
                                if not ya_existe:
                                    cursor.execute('''
                                        INSERT INTO empates (eleccionId, alumnoId, rol, votos)
                                        VALUES (?, ?, ?, ?)
                                    ''', (eleccion_id, alumno_id, rol, votos))
                            conn.commit()
                            st.error(f"⚠️ Empate detectado en {rol}. Se ha registrado para nueva votación de desempate.")
                            return True
                        return False

                    if es_desempate:
                        st.markdown("🔁 Finalizando segunda vuelta (desempate)...")

                        def obtener_ganador_unico(rol):
                            cursor.execute('''
                                SELECT alumnoId, votosObtenidos
                                FROM elecciones_detalle
                                WHERE eleccionId = ? AND rol = ?
                                ORDER BY votosObtenidos DESC
                            ''', (eleccion_id, rol))
                            resultados = cursor.fetchall()
                            if not resultados:
                                return None
                            max_votos = resultados[0][1]
                            empatados = [r for r in resultados if r[1] == max_votos]
                            return None if len(empatados) > 1 else resultados[0]

                        ganador_delegado = obtener_ganador_unico("DELEGADO")
                        ganador_subdelegado = obtener_ganador_unico("SUBDELEGADO")

                        if not ganador_delegado or not ganador_subdelegado:
                            st.error("❌ No se puede finalizar. Aún hay empate en esta ronda.")
                            return

                        # Validar que no sean la misma persona
                        if ganador_delegado[0] == ganador_subdelegado[0]:
                            # Buscar otro subdelegado
                            cursor.execute('''
                                SELECT alumnoId, votosObtenidos
                                FROM elecciones_detalle
                                WHERE eleccionId = ? AND rol = 'SUBDELEGADO'
                                ORDER BY votosObtenidos DESC
                            ''', (eleccion_id,))
                            subdelegados = cursor.fetchall()
                            subdelegado_id = None
                            for alumno_id, votos in subdelegados:
                                if alumno_id != ganador_delegado[0]:
                                    subdelegado_id = alumno_id
                                    subdelegado_votos = votos
                                    break
                            if subdelegado_id is None:
                                st.error("❌ Delegado y subdelegado no pueden ser la misma persona y no hay otro candidato.")
                                return
                        else:
                            subdelegado_id = ganador_subdelegado[0]
                            subdelegado_votos = ganador_subdelegado[1]

                        cursor.execute("DELETE FROM elecciones_detalle WHERE eleccionId = ?", (eleccion_id,))
                        cursor.execute('''
                            INSERT INTO elecciones_detalle (eleccionId, alumnoId, rol, votosObtenidos)
                            VALUES (?, ?, 'DELEGADO', ?)
                        ''', (eleccion_id, ganador_delegado[0], ganador_delegado[1]))
                        cursor.execute('''
                            INSERT INTO elecciones_detalle (eleccionId, alumnoId, rol, votosObtenidos)
                            VALUES (?, ?, 'SUBDELEGADO', ?)
                        ''', (eleccion_id, subdelegado_id, subdelegado_votos))

                        # Limpiar empates relacionados
                        cursor.execute('''
                            DELETE FROM empates
                            WHERE eleccionId IN (
                                SELECT id FROM elecciones
                                WHERE asignaturaId = ? AND esDesempate = 0
                            )
                        ''', (asignatura_id,))

                        conn.commit()
                        st.success("✅ Segunda ronda cerrada correctamente con ganadores únicos.")
                        st.rerun()

                    else:
                        top_delegados = obtener_top("DELEGADO")
                        top_subdelegados = obtener_top("SUBDELEGADO")

                        if not top_delegados or not top_subdelegados:
                            st.error("❌ No se puede finalizar la elección. Faltan votos registrados.")
                            return

                        if detectar_empate_y_registrar(top_delegados, "DELEGADO"):
                            return
                        if detectar_empate_y_registrar(top_subdelegados, "SUBDELEGADO"):
                            return

                        delegado_id, delegado_votos = top_delegados[0]
                        subdelegado_id, subdelegado_votos = top_subdelegados[0]

                        if delegado_id == subdelegado_id:
                            if len(top_subdelegados) > 1:
                                subdelegado_id, subdelegado_votos = top_subdelegados[1]
                            else:
                                st.error("⚠️ Delegado y subdelegado no pueden ser el mismo alumno y no hay otro.")
                                return

                        cursor.execute("DELETE FROM elecciones_detalle WHERE eleccionId = ?", (eleccion_id,))
                        cursor.execute('''
                            INSERT INTO elecciones_detalle (eleccionId, alumnoId, rol, votosObtenidos)
                            VALUES (?, ?, 'DELEGADO', ?)
                        ''', (eleccion_id, delegado_id, delegado_votos))
                        cursor.execute('''
                            INSERT INTO elecciones_detalle (eleccionId, alumnoId, rol, votosObtenidos)
                            VALUES (?, ?, 'SUBDELEGADO', ?)
                        ''', (eleccion_id, subdelegado_id, subdelegado_votos))

                        conn.commit()
                        st.success("✅ Delegado y Subdelegado asignados correctamente.")
                        st.rerun()

                cursor.execute("UPDATE elecciones SET estado = ? WHERE id = ?", (nuevo_estado, eleccion_id))
                conn.commit()
                st.success(f"✅ Estado actualizado a {nuevo_estado}")
                st.rerun()

            # === VISTA PREVIA Y PDF ===
            if estado_actual == "INACTIVA":
                cursor.execute("SELECT COUNT(*) FROM elecciones_detalle WHERE eleccionId = ? AND rol = 'DELEGADO'", (eleccion_id,))
                total_delegados = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM elecciones_detalle WHERE eleccionId = ? AND rol = 'SUBDELEGADO'", (eleccion_id,))
                total_subdelegados = cursor.fetchone()[0]

                if total_delegados != 1 or total_subdelegados != 1:
                    st.error("❌ No se puede generar el PDF. Se requiere un único delegado y subdelegado.")
                else:
                    st.markdown("### 🧾 Vista Previa de Resultados Finales")
                    cursor.execute('''
                        SELECT a.nombre, ed.votosObtenidos
                        FROM elecciones_detalle ed
                        JOIN alumnos a ON ed.alumnoId = a.id
                        WHERE ed.eleccionId = ? AND ed.rol = 'DELEGADO'
                    ''', (eleccion_id,))
                    delegado = cursor.fetchone()

                    cursor.execute('''
                        SELECT a.nombre, ed.votosObtenidos
                        FROM elecciones_detalle ed
                        JOIN alumnos a ON ed.alumnoId = a.id
                        WHERE ed.eleccionId = ? AND ed.rol = 'SUBDELEGADO'
                    ''', (eleccion_id,))
                    subdelegado = cursor.fetchone()

                    if delegado:
                        st.info(f"👔 Delegado: **{delegado[0]}** ({delegado[1]} votos)")
                    if subdelegado:
                        st.info(f"🧑‍💼 Subdelegado: **{subdelegado[0]}** ({subdelegado[1]} votos)")

                    if st.button("📥 Generar Reporte RERPE (PDF)"):
                        from exportar_pdf import exportar_rerpe_pdf
                        ruta = exportar_rerpe_pdf(conn, eleccion_id)
                        if ruta:
                            st.success("📄 PDF generado correctamente.")
                            with open(ruta, "rb") as f:
                                st.download_button("📄 Descargar PDF", f.read(), file_name=os.path.basename(ruta))
            else:
                st.warning("🔐 Solo se puede generar el reporte cuando la elección esté **INACTIVA**.")
        else:
            st.warning("⚠️ ID de elección no encontrado.")
    else:
        st.info("No hay elecciones registradas aún.")


#========================================================================================
def reporte_historial_module(conn):
    st.header("📊 Reporte de Historial de Elecciones")
    cursor = conn.cursor()

    modo = st.radio("Buscar historial por:", ["Alumno", "Asignatura"])

    if modo == "Alumno":
        alumno_id = None
        nombre = None

        if st.session_state['usuario']['rol'] == "ALUMNO":
            alumno_id = st.session_state['usuario']['vinculoId']
            cursor.execute("SELECT nombre FROM alumnos WHERE id = ?", (alumno_id,))
            resultado = cursor.fetchone()
            if resultado:
                nombre = resultado[0]
                st.write(f"Mostrando historial para: **{nombre}**")
            else:
                st.error("Tu cuenta no está vinculada a una ficha de alumno.")
                return
        else:
            codigo = st.text_input("Ingresa el código de alumno")
            if st.button("Buscar Historial por Alumno", key="buscar_historial_alumno"):
                cursor.execute("SELECT id, nombre FROM alumnos WHERE codigoAlumno = ?", (codigo,))
                alumno = cursor.fetchone()
                if alumno:
                    alumno_id, nombre = alumno
                    st.write(f"Mostrando historial para: **{nombre}**")
                else:
                    st.error("Código de alumno no encontrado.")
                    return

        if alumno_id:
            cursor.execute("""
                SELECT ed.rol, ed.votosObtenidos, e.fechaEleccion, a.nombre AS Asignatura, p.nombre AS Profesor
                FROM elecciones_detalle ed
                JOIN elecciones e ON ed.eleccionId = e.id
                JOIN asignaturas a ON e.asignaturaId = a.id
                JOIN profesores p ON a.profesorId = p.id
                WHERE ed.alumnoId = ?
                ORDER BY e.fechaEleccion DESC
            """, (alumno_id,))
            resultados = cursor.fetchall()

            st.subheader(f"Historial de elecciones para: {nombre}")
            if resultados:
                df = pd.DataFrame(resultados, columns=["Rol", "Votos Obtenidos", "Fecha", "Asignatura", "Profesor"])
                st.dataframe(df, use_container_width=True)

                # Visualización gráfica
                conteo_roles = df["Rol"].value_counts()
                st.markdown("### 📊 Participación total por rol")
                st.bar_chart(conteo_roles)
            else:
                st.info("Este alumno no ha participado en ninguna elección.")

    elif modo == "Asignatura":
        cursor.execute("SELECT id, nombre FROM asignaturas")
        asignaturas = cursor.fetchall()
        if asignaturas:
            opciones = {f"{nombre} (ID: {id})": id for id, nombre in asignaturas}
            seleccion = st.selectbox("Selecciona una asignatura:", list(opciones.keys()))
            if st.button("Buscar Historial por Asignatura", key="buscar_historial_asignatura"):
                asignatura_id = opciones[seleccion]

                cursor.execute("""
                    SELECT e.id, e.fechaEleccion, ed.rol, al.nombre, ed.votosObtenidos
                    FROM elecciones e
                    JOIN elecciones_detalle ed ON e.id = ed.eleccionId
                    JOIN alumnos al ON ed.alumnoId = al.id
                    WHERE e.asignaturaId = ?
                    ORDER BY e.fechaEleccion DESC
                """, (asignatura_id,))
                resultados = cursor.fetchall()

                st.subheader(f"Historial de elecciones para la asignatura: {seleccion}")
                if resultados:
                    df = pd.DataFrame(resultados, columns=["ID Elección", "Fecha", "Rol", "Alumno", "Votos Obtenidos"])
                    st.dataframe(df, use_container_width=True)

                    conteo_roles_asig = df["Rol"].value_counts()
                    st.markdown("### 📊 Participación por rol en esta asignatura")
                    st.bar_chart(conteo_roles_asig)
                else:
                    st.info("No hay elecciones registradas para esta asignatura.")

#===========================================================================================

def generar_reporte(conn, eleccion_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM elecciones WHERE id = ?", (eleccion_id,))
    eleccion = cursor.fetchone()
    if not eleccion:
        st.error("Elección no encontrada.")
        return
    cursor.execute("""
        SELECT e.id, e.fechaEleccion, a.nombre AS asignatura, p.nombre AS profesor
        FROM elecciones e
        JOIN asignaturas a ON e.asignaturaId = a.id
        JOIN profesores p ON a.profesorId = p.id
        WHERE e.id = ?
    """, (eleccion_id,))
    eleccion = cursor.fetchone()

    detalles = cursor.fetchall()
    st.subheader("Reporte de Elección (RERPE)")
    st.write(f"**ID Elección:** {eleccion_id}")
    st.write("**Resultados:**")
    if detalles:
        df_detalles = pd.DataFrame(detalles, columns=["Rol", "Nombre", "Votos Obtenidos"])
        st.dataframe(df_detalles)
    else:
        st.write("No se han registrado resultados para esta elección.")
#========================================================================================
def aprobar_postulaciones_module(conn):
    st.header("✅ Aprobación de Postulaciones Voluntarias")
    cursor = conn.cursor()

    # Obtener postulaciones pendientes
    cursor.execute('''
        SELECT p.id, a.nombre, al.nombre, al.codigoAlumno, p.rol, p.estado, p.asignaturaId
        FROM postulaciones p
        JOIN alumnos al ON p.alumnoId = al.id
        JOIN asignaturas a ON p.asignaturaId = a.id
        WHERE p.estado = 'PENDIENTE'
    ''')
    postulaciones = cursor.fetchall()

    if not postulaciones:
        st.info("No hay postulaciones pendientes.")
        return

    for id_post, nombre_asig, nombre_alumno, codigo_alumno, rol, estado, asignatura_id in postulaciones:
        with st.expander(f"📝 {nombre_alumno} ({codigo_alumno}) — {rol} — {nombre_asig}"):
            st.write(f"📚 **Asignatura:** {nombre_asig}")
            st.write(f"🙋 **Alumno:** {nombre_alumno}")
            st.write(f"📌 **Rol postulado:** {rol}")
            st.write(f"🕓 **Estado:** {estado}")

            votos_simulados = st.number_input("Asignar cantidad de votos", min_value=1, max_value=100, value=3, step=1, key=f"votos_{id_post}")

            if st.button("✅ Aprobar postulación", key=f"aprobar_{id_post}"):
                # Buscar elección activa para esa asignatura
                cursor.execute('''
                    SELECT id FROM elecciones
                    WHERE asignaturaId = ? AND estado = 'INACTIVA'
                    ORDER BY fechaEleccion DESC
                    LIMIT 1
                ''', (asignatura_id,))
                eleccion = cursor.fetchone()

                if not eleccion:
                    st.error("❌ No se encontró una elección finalizada para esta asignatura.")
                    continue

                eleccion_id = eleccion[0]

                # Insertar en elecciones_detalle
                cursor.execute('''
                    INSERT INTO elecciones_detalle (eleccionId, alumnoId, rol, votosObtenidos)
                    VALUES (?, (SELECT alumnoId FROM postulaciones WHERE id = ?), ?, ?)
                ''', (eleccion_id, id_post, rol, votos_simulados))

                # Actualizar votos y total votantes en elecciones
                if rol == "DELEGADO":
                    cursor.execute('''
                        UPDATE elecciones
                        SET votosDelegado = votosDelegado + ?, totalVotantes = totalVotantes + ?
                        WHERE id = ?
                    ''', (votos_simulados, votos_simulados, eleccion_id))
                else:
                    cursor.execute('''
                        UPDATE elecciones
                        SET votosSubdelegado = votosSubdelegado + ?, totalVotantes = totalVotantes + ?
                        WHERE id = ?
                    ''', (votos_simulados, votos_simulados, eleccion_id))

                # Marcar como aprobada
                cursor.execute("UPDATE postulaciones SET estado = 'APROBADA' WHERE id = ?", (id_post,))
                conn.commit()
                st.success(f"✅ Postulación aprobada e integrada a la elección #{eleccion_id}")

#========================================================================================
def registro_publico_module(conn):
    st.header("📝 Registro de Usuario")

    cursor = conn.cursor()

    with st.form("form_registro_publico", clear_on_submit=True):
        username = st.text_input("Nombre de Usuario (único)")
        password = st.text_input("Contraseña", type="password")
        rol = st.selectbox("Rol", ["ALUMNO", "PROFESOR"])

        vinculoId = None
        if rol == "ALUMNO":
            cursor.execute("SELECT id, nombre FROM alumnos")
            alumnos = cursor.fetchall()
            if alumnos:
                opciones = {f"{nombre} (ID: {id})": id for id, nombre in alumnos}
                opciones["Mi nombre no está en la lista"] = None
                seleccion = st.selectbox("Selecciona tu nombre de alumno:", list(opciones.keys()))
                vinculoId = opciones[seleccion]
            else:
                st.warning("No hay alumnos registrados todavía. Consulta con tu profesor o admin.")

        submit = st.form_submit_button("Crear Cuenta")

        if submit:
            try:
                cursor.execute('''
                    INSERT INTO usuarios (username, password, rol, vinculoId)
                    VALUES (?, ?, ?, ?)
                ''', (username, password, rol, vinculoId))
                conn.commit()
                st.success("Cuenta creada correctamente. Ahora puedes iniciar sesión.")
                st.info("Haz clic en el botón 'Volver al Login' para continuar.")
            except sqlite3.IntegrityError:
                st.error("Ese nombre de usuario ya está en uso.")
    
    if st.button("Volver al Login"):
        st.session_state["vista"] = "login"


# Modulo ligin 
from PIL import Image
import streamlit as st

def login_module(conn):
    # Imagen decorativa en el cuerpo principal
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.image("image.png", caption="Sistema de Elecciones Académicas", width=800)

    st.sidebar.subheader("Iniciar Sesión")
    
    if 'vista' not in st.session_state:
        st.session_state["vista"] = "login"

    if st.session_state["vista"] == "login":
        username = st.sidebar.text_input("Usuario")
        password = st.sidebar.text_input("Contraseña", type="password")

        if st.sidebar.button("Ingresar"):
            cursor = conn.cursor()
            cursor.execute("SELECT id, rol, vinculoId FROM usuarios WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            if user:
                st.session_state['usuario'] = {
                    "id": user[0],
                    "rol": user[1],
                    "vinculoId": user[2],
                    "username": username
                }
                st.success(f"Sesión iniciada como: {username} ({user[1]})")
            else:
                st.error("Usuario o contraseña incorrectos.")

        st.sidebar.markdown("---")
        if st.sidebar.button("¿No tienes cuenta? Regístrate aquí"):
            st.session_state["vista"] = "registro"

    elif st.session_state["vista"] == "registro":
        registro_publico_module(conn)

##=======================================
def inicializar_admin(conn):
    cursor = conn.cursor()
    # Verificar si ya existe un usuario con rol ADMIN
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE rol = 'ADMIN'")
    existe_admin = cursor.fetchone()[0]
    if existe_admin == 0:
        cursor.execute('''
            INSERT INTO usuarios (username, password, rol, vinculoId)
            VALUES (?, ?, ?, ?)
        ''', ("admin", "admin123", "ADMIN", None))
        conn.commit()
        print("Usuario admin creado.")
##======================================================
def vincular_profesor_module(conn):
    st.header("🔗 Vincular Cuenta con Ficha de Profesor")

    usuario = st.session_state["usuario"]
    if usuario["rol"] != "PROFESOR":
        st.warning("Este módulo solo está disponible para usuarios con rol PROFESOR.")
        return

    cursor = conn.cursor()

    # Verificar si ya tiene vínculo
    if usuario["vinculoId"]:
        st.success("Tu cuenta ya está vinculada con una ficha de profesor.")
        return

    cursor.execute("SELECT id, nombre FROM profesores")
    profesores = cursor.fetchall()

    if profesores:
        opciones = {f"{nombre} (ID: {id})": id for id, nombre in profesores}
        seleccion = st.selectbox("Selecciona tu ficha de profesor", list(opciones.keys()))
        profesor_id = opciones[seleccion]

        if st.button("Vincular"):
            try:
                cursor.execute('''
                    UPDATE usuarios
                    SET vinculoId = ?
                    WHERE id = ?
                ''', (profesor_id, usuario["id"]))
                conn.commit()
                st.success("Cuenta vinculada correctamente. Recarga para continuar.")
                st.session_state["usuario"]["vinculoId"] = profesor_id
            except Exception as e:
                st.error("Error al vincular. Intenta nuevamente.")
    else:
        st.warning("No hay fichas de profesor disponibles para vincular.")
#================================================================================
def vincular_alumno_module(conn):
    st.header("🎓 Vincular Cuenta con Ficha de Alumno")

    usuario = st.session_state["usuario"]
    if usuario["rol"] != "ALUMNO":
        st.warning("Este módulo solo está disponible para usuarios con rol ALUMNO.")
        return

    if usuario["vinculoId"]:
        st.success("Tu cuenta ya está vinculada con una ficha de alumno.")
        return

    cursor = conn.cursor()

    # Mostrar lista de alumnos no vinculados aún
    cursor.execute('''
        SELECT id, nombre, codigoAlumno
        FROM alumnos
        WHERE id NOT IN (
            SELECT vinculoId FROM usuarios WHERE rol = 'ALUMNO' AND vinculoId IS NOT NULL
        )
    ''')
    alumnos = cursor.fetchall()

    if not alumnos:
        st.info("No hay fichas de alumno disponibles para vincular.")
        return

    opciones = {
        f"{nombre} - {codigo} (ID: {id})": id
        for id, nombre, codigo in alumnos
    }
    seleccion = st.selectbox("Selecciona tu ficha de alumno:", list(opciones.keys()))
    alumno_id = opciones[seleccion]

    if st.button("Vincular"):
        try:
            cursor.execute(
                "UPDATE usuarios SET vinculoId = ? WHERE id = ?",
                (alumno_id, usuario["id"])
            )
            conn.commit()
            st.success("✅ Cuenta vinculada correctamente. Recarga para continuar.")
            st.session_state["usuario"]["vinculoId"] = alumno_id
        except Exception as e:
            st.error("❌ Error al vincular. Intenta nuevamente.")
            st.exception(e)




# =====================
# Función Principal
# =====================

def main():
    from utils import (
        aplicar_css_moderno_adaptativo,
        aplicar_css_fondo_login,
        aplicar_css_botones_sidebar,
    )
    conn = conectar_db()
    crear_tablas(conn)
    inicializar_admin(conn)

    # ============ LOGIN CON FONDO DE IMAGEN =============
    if 'usuario' not in st.session_state:
        aplicar_css_fondo_login()
        login_module(conn)
        return

    # ============ APP CON ESTILO MODERNO Y BOTONES =========
    aplicar_css_moderno_adaptativo()
    aplicar_css_botones_sidebar()

    usuario = st.session_state['usuario']
    rol = usuario["rol"]

    st.sidebar.title(f"Navegación - {rol}")
    st.sidebar.write(f"Sesión iniciada como: {usuario['username']}")
    if rol == "ALUMNO" and usuario.get("vinculoId"):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nombre, codigoAlumno, programaEstudio FROM alumnos WHERE id = ?",
            (usuario["vinculoId"],))
        alumno = cursor.fetchone()
        if alumno:
            st.sidebar.markdown("---")
            st.sidebar.markdown(f"👤 **Alumno:** {alumno[0]}")
            st.sidebar.markdown(f"🧾 **Código:** {alumno[1]}")
            st.sidebar.markdown(f"🏫 **Carrera:** {alumno[2]}")

    # Menús según rol
    opciones = []
    if rol == "ADMIN":
        opciones = [
            "Registro Alumno",
            "Registro Asignatura",
            "Asociar Alumno a Asignatura",
            "Crear Elección",
            "Votación/Selección",
            "Administración",
            "Reporte Historial",
            "Registro de Usuarios",
            "Registro de Profesores",
            "Registro de Profesor + Usuario"
        ]
    elif rol == "PROFESOR":
        opciones = [
            "Registro de Profesores",
            "Registro Asignatura",
            "Crear Elección",
            "Asociar Alumno a Asignatura",
            "Administración",
            "Reporte Historial",
            "Vincular con Ficha de Profesor",
            "Aprobación de Postulaciones",
            "Gestionar Elecciones"
        ]
    elif rol == "ALUMNO":
        opciones = [
            "Registro Alumno",
            "Votación/Selección",
            "Reporte Historial",
            "Vincular con Ficha de Alumno"
        ]

    # ============ MENÚ DE BOTONES MODERNOS ============
    if opciones:
        if "menu_nav" not in st.session_state or st.session_state.get("last_rol") != rol:
            st.session_state["menu_nav"] = opciones[0]
            st.session_state["last_rol"] = rol

        st.sidebar.markdown("Ir a:")
        for opcion_btn in opciones:
            if st.sidebar.button(opcion_btn, key=f"btn_{opcion_btn}", use_container_width=True):
                st.session_state["menu_nav"] = opcion_btn

        opcion = st.session_state["menu_nav"]

        # Lógica de módulos
        if opcion == "Registro Alumno":
            registro_alumno_module(conn)
        elif opcion == "Registro Asignatura":
            registro_asignatura_module(conn)
        elif opcion == "Asociar Alumno a Asignatura":
            asociar_alumno_asignatura_module(conn)
        elif opcion == "Crear Elección":
            crear_eleccion_module(conn)
        elif opcion == "Votación/Selección":
            votacion_module(conn)
        elif opcion == "Administración":
            admin_panel_module(conn)
        elif opcion == "Reporte Historial":
            reporte_historial_module(conn)
        elif opcion == "Registro de Usuarios":
            registro_usuario_module(conn)
        elif opcion == "Registro de Profesores":
            registro_profesor_module(conn)
        elif opcion == "Registro de Profesor + Usuario":
            registro_profesor_con_usuario_module(conn)
        elif opcion == "Vincular con Ficha de Profesor":
            vincular_profesor_module(conn)
        elif opcion == "Vincular con Ficha de Alumno":
            vincular_alumno_module(conn)
        elif opcion == "Aprobación de Postulaciones":
            aprobar_postulaciones_module(conn)
        elif opcion == "Gestionar Elecciones":
            gestionar_elecciones_profesor(conn)
    else:
        st.warning("No tienes opciones disponibles para este rol.")

    # ============ BOTÓN CERRAR SESIÓN ============
    if st.sidebar.button("Cerrar Sesión"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("Sesión cerrada. Recargando...")
        st.rerun()

if __name__ == "__main__":
    main()
