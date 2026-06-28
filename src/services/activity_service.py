from database.database import get_connection
from services.validation_utils import (
    parse_time,
    validate_date,
    validate_time
)

def create_activity(
        fecha,
        hora_inicio,
        hora_fin,
        interrupciones,
        descripcion,
        job_id):
    (
        fecha,
        hora_inicio,
        hora_fin,
        interrupciones,
        job_id
    ) = validate_activity_data(
        fecha,
        hora_inicio,
        hora_fin,
        interrupciones,
        job_id
    )

    if activity_overlaps(fecha, hora_inicio, hora_fin):
        raise ValueError("Ya existe una actividad registrada en ese rango horario.")

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO actividades (
            fecha,
            hora_inicio,
            hora_fin,
            interrupciones,
            descripcion,
            job_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            fecha,
            hora_inicio,
            hora_fin,
            interrupciones,
            descripcion,
            job_id
        )
    )

    conn.commit()

    activity_id = cursor.lastrowid

    conn.close()

    return activity_id

def get_all_activities():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            a.id,
            a.fecha,
            a.hora_inicio,
            a.hora_fin,
            a.interrupciones,
            a.descripcion,
            j.id,
            j.nombre
        FROM actividades a
        JOIN jobs j
            ON a.job_id = j.id
        WHERE a.activo = 1
        ORDER BY a.fecha DESC
        """
    )

    activities = cursor.fetchall()

    conn.close()

    return activities

def get_activity_by_id(activity_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            fecha,
            hora_inicio,
            hora_fin,
            interrupciones,
            descripcion,
            job_id
        FROM actividades
        WHERE id = ?
        AND activo = 1
        """,
        (activity_id,)
    )

    activity = cursor.fetchone()

    conn.close()

    return activity

def update_activity(
        activity_id,
        fecha,
        hora_inicio,
        hora_fin,
        interrupciones,
        descripcion,
        job_id):
    (
        fecha,
        hora_inicio,
        hora_fin,
        interrupciones,
        job_id
    ) = validate_activity_data(
        fecha,
        hora_inicio,
        hora_fin,
        interrupciones,
        job_id
    )
    if activity_overlaps(fecha, hora_inicio, hora_fin, activity_id):
        raise ValueError("Ya existe una actividad registrada en ese rango horario.")

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE actividades
        SET
            fecha = ?,
            hora_inicio = ?,
            hora_fin = ?,
            interrupciones = ?,
            descripcion = ?,
            job_id = ?
        WHERE id = ?
        AND activo = 1
        """,
        (
            fecha,
            hora_inicio,
            hora_fin,
            interrupciones,
            descripcion,
            job_id,
            activity_id
        )
    )

    conn.commit()

    filas_afectadas = cursor.rowcount

    conn.close()

    return filas_afectadas > 0

def delete_activity(activity_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE actividades
        SET activo = 0
        WHERE id = ?
        """,
        (activity_id,)
    )

    conn.commit()

    filas_afectadas = cursor.rowcount

    conn.close()

    return filas_afectadas > 0

def restore_activity(activity_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE actividades
        SET activo = 1
        WHERE id = ?
        """,
        (activity_id,)
    )

    conn.commit()

    filas_afectadas = cursor.rowcount

    conn.close()

    return filas_afectadas > 0

def get_all_activities_admin():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            a.id,
            a.fecha,
            a.hora_inicio,
            a.hora_fin,
            a.interrupciones,
            a.descripcion,
            a.activo,
            j.nombre
        FROM actividades a
        JOIN jobs j
            ON a.job_id = j.id
        ORDER BY a.fecha DESC
        """
    )

    activities = cursor.fetchall()

    conn.close()

    return activities

#####################
###### Helpers ######
#####################

def validate_time_range(hora_inicio, hora_fin):

    inicio = parse_time(hora_inicio)
    fin = parse_time(hora_fin)

    return fin > inicio

def calculate_duration(
        hora_inicio,
        hora_fin,
        interrupciones):

    inicio = parse_time(hora_inicio)
    fin = parse_time(hora_fin)

    minutos = (
        fin - inicio
    ).total_seconds() / 60

    return int(
        minutos - interrupciones
    )

def validate_activity_data(
        fecha,
        hora_inicio,
        hora_fin,
        interrupciones,
        job_id):

    fecha = validate_date(fecha, "La fecha debe tener formato AAAA-MM-DD.")

    hora_inicio = validate_time(hora_inicio, "La hora de inicio no es valida.")
    hora_fin = validate_time(hora_fin, "La hora de fin no es valida.")

    if not isinstance(interrupciones, int) or isinstance(interrupciones, bool):
        raise ValueError("Las interrupciones deben ser un numero entero.")

    if interrupciones < 0:
        raise ValueError("Las interrupciones no pueden ser negativas.")

    if not validate_time_range(hora_inicio, hora_fin):
        raise ValueError("La hora de fin debe ser posterior a la hora de inicio.")

    duracion = calculate_duration(hora_inicio, hora_fin, interrupciones)

    if duracion <= 0:
        raise ValueError("La duracion resultante debe ser mayor a cero.")

    if not job_exists(job_id):
        raise ValueError("El trabajo seleccionado no existe o esta inactivo.")

    return (
        fecha,
        hora_inicio,
        hora_fin,
        interrupciones,
        job_id
    )

def job_exists(job_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM jobs
        WHERE id = ?
        AND activo = 1
        """,
        (job_id,)
    )

    job = cursor.fetchone()

    conn.close()

    return job is not None

def activity_overlaps(
        fecha,
        hora_inicio,
        hora_fin,
        activity_id=None):

    conn = get_connection()

    cursor = conn.cursor()

    query = """
        SELECT id
        FROM actividades
        WHERE fecha = ?
        AND activo = 1
        AND hora_inicio < ?
        AND hora_fin > ?
    """

    params = [
        fecha,
        hora_fin,
        hora_inicio
    ]

    if activity_id is not None:
        query += " AND id <> ?"
        params.append(activity_id)

    cursor.execute(
        query,
        tuple(params)
    )

    activity = cursor.fetchone()

    conn.close()

    return activity is not None
