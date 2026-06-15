from src.database.database import get_connection
from datetime import datetime

def create_activity(
        fecha,
        hora_inicio,
        hora_fin,
        interrupciones,
        descripcion,
        job_id):
    
    if not validate_time_range(
        hora_inicio,
        hora_fin):

        raise ValueError(
            "La hora de fin debe ser posterior a la hora de inicio."
        )

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

def validate_time_range(hora_inicio, hora_fin):

    inicio = datetime.strptime(
        hora_inicio,
        "%H:%M"
    )

    fin = datetime.strptime(
        hora_fin,
        "%H:%M"
    )

    return fin > inicio

def calculate_duration(
        hora_inicio,
        hora_fin,
        interrupciones):

    inicio = datetime.strptime(
        hora_inicio,
        "%H:%M"
    )

    fin = datetime.strptime(
        hora_fin,
        "%H:%M"
    )

    minutos = (
        fin - inicio
    ).total_seconds() / 60

    return int(
        minutos - interrupciones
    )