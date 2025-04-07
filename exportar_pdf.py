from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import os
from datetime import datetime

def exportar_rerpe_pdf(conn, eleccion_id, logo_path="logo_ucss.png"):
    cursor = conn.cursor()

    # Datos de la elección y profesor
    cursor.execute("""
        SELECT e.fechaEleccion, a.nombre, a.codigoAsignatura, a.profesorId, p.nombre, p.correo
        FROM elecciones e
        JOIN asignaturas a ON e.asignaturaId = a.id
        JOIN profesores p ON a.profesorId = p.id
        WHERE e.id = ?
    """, (eleccion_id,))
    eleccion = cursor.fetchone()
    if not eleccion:
        return None

    fecha, asignatura, codigo_asig, profesor_id, profesor_nombre, correo = eleccion

    # Totales de votos
    cursor.execute("""
        SELECT totalVotantes, votosDelegado, votosSubdelegado, abstenciones
        FROM elecciones
        WHERE id = ?
    """, (eleccion_id,))
    total_votantes, votos_delegado, votos_subdelegado, abstenciones = cursor.fetchone()

    # Delegado
    cursor.execute("""
        SELECT al.codigoAlumno, al.nombre, al.programaEstudio, ed.votosObtenidos
        FROM elecciones_detalle ed
        JOIN alumnos al ON ed.alumnoId = al.id
        WHERE ed.eleccionId = ? AND ed.rol = 'DELEGADO'
        LIMIT 1
    """, (eleccion_id,))
    delegado = cursor.fetchone()

    # Subdelegado
    cursor.execute("""
        SELECT al.codigoAlumno, al.nombre, al.programaEstudio, ed.votosObtenidos
        FROM elecciones_detalle ed
        JOIN alumnos al ON ed.alumnoId = al.id
        WHERE ed.eleccionId = ? AND ed.rol = 'SUBDELEGADO'
        LIMIT 1
    """, (eleccion_id,))
    subdelegado = cursor.fetchone()

    # Nombre dinámico del archivo
    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
    fecha_str = fecha_dt.strftime("%Y-%m-%d")
    nombre_pdf = f"RERPE_{asignatura.replace(' ', '_')}_{fecha_str}.pdf"
    ruta_pdf = os.path.join(os.getcwd(), nombre_pdf)

    # Crear PDF
    c = canvas.Canvas(ruta_pdf, pagesize=A4)
    width, height = A4

    if os.path.exists(logo_path):
        c.drawImage(logo_path, 2 * cm, height - 4 * cm, width=4 * cm, preserveAspectRatio=True)

    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, height - 2.5 * cm, "UNIVERSIDAD CATÓLICA SEDES SAPIENTIAE")
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, height - 3.1 * cm, "FACULTAD DE INGENIERÍA")
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width / 2, height - 3.7 * cm, "ACTA DE ELECCIÓN DE DELEGADOS DE ASIGNATURAS")

    y = height - 5 * cm

    # Tabla de resumen ajustada
    table_data = [
        ["PROGRAMA DE ESTUDIOS", "CÓDIGO DE ASIGNATURA", "SECCIÓN", "ASIGNATURA", "PROFESOR"],
        [delegado[2] if delegado else "-----", codigo_asig, "------", asignatura, profesor_nombre]
    ]
    col_widths = [4*cm, 4*cm, 2.5*cm, 4.5*cm, 4.5*cm]
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")
    ]))
    table.wrapOn(c, width, height)
    table.drawOn(c, 2 * cm, y - 2 * cm)
    y -= 6 * cm

    # Texto con fecha y hora actual
    now = datetime.now()
    texto = f"""En Lima, el día {now.strftime('%d')} de {now.strftime('%B')} del año {now.year}, 
siendo las {now.strftime('%I:%M %p')} horas y terminado el acto de elección de delegado, se dio el siguiente resultado:"""
    c.setFont("Helvetica", 9)
    for line in texto.split("\n"):
        c.drawString(2 * cm, y, line.strip())
        y -= 0.5 * cm

    # Resultados
    c.drawString(2 * cm, y, f"Número de votos para elegir al delegado (a): {votos_delegado}")
    y -= 0.4 * cm
    c.drawString(2 * cm, y, f"Número de votos para elegir al subdelegado (a): {votos_subdelegado}")
    y -= 0.4 * cm
    c.drawString(2 * cm, y, f"Número de abstenciones: {abstenciones}")
    y -= 0.4 * cm
    c.drawString(2 * cm, y, f"Número total de estudiantes que participaron en la elección: {total_votantes}")
    y -= 0.8 * cm

    # Delegado
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2 * cm, y, "DELEGADO (A)")
    y -= 0.4 * cm
    c.setFont("Helvetica", 9)
    if delegado:
        c.drawString(2 * cm, y, f"Código: {delegado[0]}        Votos: {delegado[3]}")
        y -= 0.4 * cm
        c.drawString(2 * cm, y, f"Apellidos y Nombres: {delegado[1]}")
        y -= 0.4 * cm
        c.drawString(2 * cm, y, f"Teléfono: __________________________    Celular: _________________________")
        y -= 0.4 * cm
        c.drawString(2 * cm, y, f"Email: ______________________________    Firma: _________________________")
        y -= 1 * cm
    else:
        c.drawString(2 * cm, y, "No se registró delegado.")
        y -= 1 * cm

    # Subdelegado
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2 * cm, y, "SUBDELEGADO (A)")
    y -= 0.4 * cm
    c.setFont("Helvetica", 9)
    if subdelegado:
        c.drawString(2 * cm, y, f"Código: {subdelegado[0]}        Votos: {subdelegado[3]}")
        y -= 0.4 * cm
        c.drawString(2 * cm, y, f"Apellidos y Nombres: {subdelegado[1]}")
        y -= 0.4 * cm
        c.drawString(2 * cm, y, f"Teléfono: __________________________    Celular: _________________________")
        y -= 0.4 * cm
        c.drawString(2 * cm, y, f"Email: ______________________________    Firma: _________________________")
        y -= 1 * cm
    else:
        c.drawString(2 * cm, y, "No se registró subdelegado.")
        y -= 1 * cm

    c.save()
    return ruta_pdf
