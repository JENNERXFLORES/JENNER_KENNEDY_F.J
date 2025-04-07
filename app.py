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
        nombre = st.text_input("Nombre completo")
        codigoAlumno = st.text_input("Código de Alumno")
        programaEstudio = st.text_input("Programa de Estudios")
        enviar = st.form_submit_button("Registrar Alumno")
        if enviar:
            if nombre and codigoAlumno and programaEstudio:
                try:
                    cursor.execute('''
                        INSERT INTO alumnos (nombre, codigoAlumno, programaEstudio)
                        VALUES (?, ?, ?)
                    ''', (nombre, codigoAlumno, programaEstudio))
                    conn.commit()
                    st.success("Alumno registrado correctamente.")
                except sqlite3.IntegrityError:
                    st.error("El código de alumno ya existe.")
            else:
                st.error("Completa todos los campos.")

    # Solo ADMIN puede ver la tabla y eliminar
    if st.session_state["usuario"]["rol"] == "ADMIN":
        st.subheader("📋 Lista de Alumnos Registrados")
        cursor.execute("SELECT id, nombre, codigoAlumno, programaEstudio FROM alumnos")
        alumnos = cursor.fetchall()
        if alumnos:
            import pandas as pd
            df = pd.DataFrame(alumnos, columns=["ID", "Nombre", "Código", "Programa"])
            st.dataframe(df, use_container_width=True)

            id_borrar = st.number_input("ID de alumno a eliminar", min_value=1, step=1)
            if st.button("❌ Eliminar Alumno"):
                cursor.execute("DELETE FROM alumnos WHERE id = ?", (id_borrar,))
                conn.commit()
                st.success("Alumno eliminado.")
                st.experimental_rerun()
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
            id_eliminar = st.number_input("ID de profesor a eliminar", min_value=1, step=1)
            if st.button("❌ Eliminar Profesor"):
                cursor.execute("DELETE FROM profesores WHERE id = ?", (id_eliminar,))
                conn.commit()
                st.success("Profesor eliminado.")
                st.rerun()

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

    # Mostrar tabla solo para ADMIN
    if st.session_state["usuario"]["rol"] == "ADMIN":
        st.subheader("📋 Usuarios Registrados")
        cursor.execute("SELECT id, username, rol, vinculoId FROM usuarios")
        usuarios = cursor.fetchall()
        if usuarios:
            import pandas as pd
            df = pd.DataFrame(usuarios, columns=["ID", "Usuario", "Rol", "VinculoId"])
            st.dataframe(df, use_container_width=True)
            id_eliminar = st.number_input("ID de usuario a eliminar", min_value=1, step=1)
            if st.button("❌ Eliminar Usuario"):
                cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_eliminar,))
                conn.commit()
                st.success("Usuario eliminado.")
                st.rerun()

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

    # Obtener datos de la elección seleccionada
    cursor.execute('''
        SELECT e.asignaturaId, e.metodo, e.estado, a.nombre, p.nombre
        FROM elecciones e
        JOIN asignaturas a ON e.asignaturaId = a.id
        JOIN profesores p ON a.profesorId = p.id
        WHERE e.id = ?
    ''', (eleccion_id,))
    eleccion_data = cursor.fetchone()
    asignatura_id, metodo, estado, asig_nombre, profesor_nombre = eleccion_data

    st.write(f"📘 **Asignatura:** {asig_nombre}")
    st.write(f"👨‍🏫 **Profesor:** {profesor_nombre}")
    st.write(f"⚙️ **Método de Elección:** {metodo}")
    st.write(f"🔒 **Estado:** {'ACTIVA' if estado == 'ACTIVA' else 'INACTIVA'}")

    if estado == "INACTIVA":
        st.info("📌 Esta elección está cerrada. A continuación se muestran los resultados:")
        cursor.execute('''
            SELECT al.nombre, ed.rol
            FROM elecciones_detalle ed
            JOIN alumnos al ON ed.alumnoId = al.id
            WHERE ed.eleccionId = ?
        ''', (eleccion_id,))
        resultados = cursor.fetchall()
        if resultados:
            for nombre, rol in resultados:
                st.markdown(f"**{rol}**: {nombre}")
        else:
            st.warning("No se han registrado delegados aún.")
        return

    # =============================
    # SI LA ELECCIÓN ESTÁ ACTIVA:
    # =============================
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
                            # Validar si ya votó en esta elección y rol
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
                                cursor.execute("INSERT INTO elecciones_detalle (eleccionId, alumnoId, rol, votosObtenidos) VALUES (?, ?, ?, 1)", (eleccion_id, candidato_id, rol_sel))

                            # Registrar el voto único
                            cursor.execute("INSERT INTO registro_votos (eleccionId, alumnoId, rol, fechaVoto) VALUES (?, ?, ?, datetime('now'))", (eleccion_id, alumno_id_confirmado, rol_sel))

                            if rol_sel == "DELEGADO":
                                cursor.execute("UPDATE elecciones SET votosDelegado = votosDelegado + 1, totalVotantes = totalVotantes + 1 WHERE id = ?", (eleccion_id,))
                            else:
                                cursor.execute("UPDATE elecciones SET votosSubdelegado = votosSubdelegado + 1, totalVotantes = totalVotantes + 1 WHERE id = ?", (eleccion_id,))

                            conn.commit()
                            st.success(f"✅ Voto registrado para {candidato_sel} como {rol_sel}")
                    else:
                        st.warning("No hay candidatos registrados.")
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS postulaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alumnoId INTEGER,
                asignaturaId INTEGER,
                estado TEXT DEFAULT 'PENDIENTE',
                FOREIGN KEY (alumnoId) REFERENCES alumnos(id),
                FOREIGN KEY (asignaturaId) REFERENCES asignaturas(id)
            )
        ''')
        cursor.execute('''
            SELECT id, estado FROM postulaciones
            WHERE alumnoId = ? AND asignaturaId = ?
        ''', (alumno_id, asignatura_id))
        postulacion = cursor.fetchone()

        if postulacion:
            estado = postulacion[1]
            st.info(f"Ya te postulaste. Estado actual: **{estado}**")
        else:
            if st.button("📨 Postularme como delegado"):
                cursor.execute('''
                    INSERT INTO postulaciones (alumnoId, asignaturaId, estado)
                    VALUES (?, ?, 'PENDIENTE')
                ''', (alumno_id, asignatura_id))
                conn.commit()
                st.success("Tu postulación ha sido registrada.")


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

    # Obtener elecciones del profesor
    cursor.execute('''
        SELECT e.id, a.nombre, e.fechaEleccion, e.metodo, e.estado
        FROM elecciones e
        JOIN asignaturas a ON e.asignaturaId = a.id
        WHERE a.profesorId = ?
        ORDER BY e.fechaEleccion DESC
    ''', (profesor_id,))
    elecciones = cursor.fetchall()

    if not elecciones:
        st.info("No hay elecciones creadas aún para tus asignaturas.")
        return

    for eleccion_id, asig_nombre, fecha, metodo, estado in elecciones:
        with st.expander(f"📘 {asig_nombre} ({metodo}) — {fecha[:10]} — Estado: {estado}"):
            col1, col2 = st.columns([2, 1])
            col1.markdown(f"**Método:** {metodo}  \n**Estado actual:** `{estado}`")

            # Cambiar estado
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

            st.markdown("---")
            st.markdown("### ⚠️ Eliminar esta elección")
            st.warning("Esta acción eliminará también los votos y postulaciones asociadas.")
            confirmar = st.checkbox(f"Confirmo eliminar elección ID {eleccion_id}", key=f"chk_{eleccion_id}")
            if st.button("🗑️ Eliminar elección", key=f"eliminar_{eleccion_id}") and confirmar:
                # Eliminar datos relacionados
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

    # Obtener elecciones
    cursor.execute('''
        SELECT e.id, a.nombre, a.codigoAsignatura, e.fechaEleccion,
               e.totalVotantes, e.votosDelegado, e.votosSubdelegado,
               e.abstenciones, e.estado
        FROM elecciones e
        JOIN asignaturas a ON e.asignaturaId = a.id
        ORDER BY e.fechaEleccion DESC
    ''')
    elecciones = cursor.fetchall()

    if elecciones:
        import pandas as pd
        import os

        df = pd.DataFrame(elecciones, columns=[
            "ID", "Asignatura", "Código", "Fecha", "Total Votantes",
            "Votos Delegado", "Votos Subdelegado", "Abstenciones", "Estado"
        ])
        st.dataframe(df, use_container_width=True)

        st.markdown("---")
        st.subheader("📄 Acciones para una Elección")

        eleccion_id = st.number_input("ID de Elección", min_value=1, step=1)

        # Mostrar estado actual
        cursor.execute("SELECT estado FROM elecciones WHERE id = ?", (eleccion_id,))
        fila = cursor.fetchone()
        if fila:
            estado_actual = fila[0]
            st.info(f"🔒 Estado actual: **{estado_actual}**")

            # Botón para cambiar estado
            nuevo_estado = "INACTIVA" if estado_actual == "ACTIVA" else "ACTIVA"
            if st.button(f"Cambiar estado a {nuevo_estado}"):
                if nuevo_estado == "INACTIVA":
                    # Validar empate antes de permitir cambio
                    def verificar_ganador_unico(rol):
                        cursor.execute('''
                            SELECT alumnoId, SUM(votosObtenidos) as total_votos
                            FROM elecciones_detalle
                            WHERE eleccionId = ? AND rol = ?
                            GROUP BY alumnoId
                            ORDER BY total_votos DESC
                        ''', (eleccion_id, rol))
                        resultado = cursor.fetchall()
                        if not resultado:
                            return False, None
                        max_votos = resultado[0][1]
                        ganadores = [r for r in resultado if r[1] == max_votos]
                        return len(ganadores) == 1, (ganadores[0] if ganadores else None)

                    delegado_unico, delegado = verificar_ganador_unico("DELEGADO")
                    subdelegado_unico, subdelegado = verificar_ganador_unico("SUBDELEGADO")

                    if not delegado_unico or not subdelegado_unico:
                        st.error("❌ No se puede finalizar la elección. Debe haber un único delegado y subdelegado.")
                        return

                    # Limpiar y registrar solo el ganador
                    cursor.execute("DELETE FROM elecciones_detalle WHERE eleccionId = ? AND rol = 'DELEGADO'", (eleccion_id,))
                    cursor.execute("INSERT INTO elecciones_detalle (eleccionId, alumnoId, rol, votosObtenidos) VALUES (?, ?, 'DELEGADO', ?)", (eleccion_id, delegado[0], delegado[1]))

                    cursor.execute("DELETE FROM elecciones_detalle WHERE eleccionId = ? AND rol = 'SUBDELEGADO'", (eleccion_id,))
                    cursor.execute("INSERT INTO elecciones_detalle (eleccionId, alumnoId, rol, votosObtenidos) VALUES (?, ?, 'SUBDELEGADO', ?)", (eleccion_id, subdelegado[0], subdelegado[1]))

                    conn.commit()
                    st.success("✅ Delegado y Subdelegado únicos definidos correctamente.")

                cursor.execute("UPDATE elecciones SET estado = ? WHERE id = ?", (nuevo_estado, eleccion_id))
                conn.commit()
                st.success(f"✅ Estado actualizado a {nuevo_estado}")
                st.rerun()

            # Generar PDF solo si está inactiva
            if estado_actual == "INACTIVA":
                # Verificar si hay un único delegado y subdelegado
                cursor.execute("SELECT COUNT(*) FROM elecciones_detalle WHERE eleccionId = ? AND rol = 'DELEGADO'", (eleccion_id,))
                total_delegados = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM elecciones_detalle WHERE eleccionId = ? AND rol = 'SUBDELEGADO'", (eleccion_id,))
                total_subdelegados = cursor.fetchone()[0]

                if total_delegados != 1 or total_subdelegados != 1:
                    st.error("❌ No se puede generar el PDF. Se requiere un único delegado y subdelegado.")
                else:
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
                st.error("Tu cuenta no está vinculada a una ficha de alumno. Por favor, vincúlala o crea una.")
                return
            st.write(f"Mostrando historial para: **{nombre}**")
        else:
            codigo = st.text_input("Ingresa el código de alumno")
            buscar = st.button("Buscar Historial por Alumno", key="buscar_historial_alumno")
            if buscar:
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
                SELECT ed.rol, ed.votosObtenidos, e.fechaEleccion, a.nombre as Asignatura, p.nombre as profesor
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
                st.dataframe(df)
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
                    st.dataframe(df)
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
    st.header("✋ Aprobación de Postulaciones Voluntarias")
    cursor = conn.cursor()

    # Validar sesión y rol
    if "usuario" not in st.session_state or st.session_state["usuario"]["rol"] != "PROFESOR":
        st.warning("Este módulo solo está disponible para profesores.")
        return

    profesor_id = st.session_state["usuario"].get("vinculoId")
    if not profesor_id:
        st.error("Tu cuenta no está vinculada a un profesor.")
        return

    # Obtener asignaturas del profesor
    cursor.execute("SELECT id, nombre FROM asignaturas WHERE profesorId = ?", (profesor_id,))
    asignaturas = cursor.fetchall()
    if not asignaturas:
        st.info("No tienes asignaturas asignadas.")
        return

    asignatura_dict = {f"{nombre} (ID: {id})": id for id, nombre in asignaturas}
    asignatura_sel = st.selectbox("Selecciona una asignatura", list(asignatura_dict.keys()))
    asignatura_id = asignatura_dict[asignatura_sel]

    # Obtener postulaciones pendientes
    cursor.execute('''
        SELECT po.id, al.id, al.nombre, al.codigoAlumno
        FROM postulaciones po
        JOIN alumnos al ON po.alumnoId = al.id
        WHERE po.asignaturaId = ? AND po.estado = 'PENDIENTE'
    ''', (asignatura_id,))
    postulaciones = cursor.fetchall()

    if postulaciones:
        st.subheader("Postulaciones pendientes:")
        for post_id, alumno_id, nombre, codigo in postulaciones:
            col1, col2, col3 = st.columns([4, 2, 2])
            col1.markdown(f"**{nombre}** (Código: `{codigo}`)")
            with col2:
                if st.button("✅ Aprobar", key=f"aprobar_{post_id}"):
                    # Verificar si ya existe elección para esta asignatura
                    cursor.execute('''
                        SELECT id FROM elecciones
                        WHERE asignaturaId = ? AND metodo = 'VOLUNTARIO'
                        ORDER BY fechaEleccion DESC LIMIT 1
                    ''', (asignatura_id,))
                    eleccion = cursor.fetchone()

                    if eleccion:
                        eleccion_id = eleccion[0]
                        # Registrar como delegado
                        cursor.execute('''
                            INSERT INTO elecciones_detalle (eleccionId, alumnoId, rol, votosObtenidos)
                            VALUES (?, ?, 'DELEGADO', 1)
                        ''', (eleccion_id, alumno_id))
                        # Marcar postulación como aprobada
                        cursor.execute("UPDATE postulaciones SET estado = 'APROBADO' WHERE id = ?", (post_id,))
                        conn.commit()
                        st.success(f"{nombre} ha sido aprobado como delegado.")
                        st.rerun()
                    else:
                        st.error("No hay una elección VOLUNTARIA activa para esta asignatura.")
            with col3:
                if st.button("❌ Rechazar", key=f"rechazar_{post_id}"):
                    cursor.execute("UPDATE postulaciones SET estado = 'RECHAZADO' WHERE id = ?", (post_id,))
                    conn.commit()
                    st.warning(f"{nombre} ha sido rechazado.")
                    st.rerun()
    else:
        st.info("No hay postulaciones pendientes para esta asignatura.")

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
def login_module(conn):
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
    conn = conectar_db()
    crear_tablas(conn)
    inicializar_admin(conn)  # Inserta el admin si no existe
    
# Esto hace que el reloj se actualice automáticamente cada 5 segundos
    st_autorefresh(interval=9000, key="reloj_actual")
    now = datetime.now()
    st.sidebar.markdown(f"🕒 Hora actual: `{now.strftime('%I:%M:%S %p')}`")


    if 'usuario' not in st.session_state:
        login_module(conn)
        return

    usuario = st.session_state['usuario']
    rol = usuario["rol"]

    st.sidebar.title(f"Navegación - {rol}")
    st.sidebar.write(f"Sesión iniciada como: {usuario['username']}")
    if rol == "ALUMNO" and st.session_state['usuario'].get("vinculoId"):
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, codigoAlumno, programaEstudio FROM alumnos WHERE id = ?", 
                   (st.session_state['usuario']["vinculoId"],))
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
            "Registro de Profesores",  # 👈 Agrega esta línea
            "Registro de Profesor + Usuario"  # ✅ Nueva opción
        ]
    elif rol == "PROFESOR":
        opciones = [
            "Registro de Profesores",
            "Registro Asignatura",
            "Crear Elección",
            "Asociar Alumno a Asignatura",  # ✅ nuevo acceso
            "Administración",
            "Reporte Historial",
            "Vincular con Ficha de Profesor",
            "Aprobación de Postulaciones",
            "Gestionar Elecciones"
            
        ]
    elif rol == "ALUMNO":
        opciones = [
            "Registro Alumno",  # Si quieres permitir que cree su ficha
            "Votación/Selección",
            "Reporte Historial",
            "Vincular con Ficha de Alumno"  # ✅ nueva opción

        ]

    if opciones:
        opcion = st.sidebar.radio("Ir a:", opciones)

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
        if opcion == "Aprobación de Postulaciones":
            aprobar_postulaciones_module(conn)
        if opcion == "Gestionar Elecciones":
            gestionar_elecciones_profesor(conn)

        


    else:
        st.warning("No tienes opciones disponibles para este rol.")


    if st.sidebar.button("Cerrar Sesión"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("Sesión cerrada. Recargando...")
        st.rerun()  # Aquí sí está bien usarlo tras limpiar sesión


if __name__ == "__main__":
    main()
