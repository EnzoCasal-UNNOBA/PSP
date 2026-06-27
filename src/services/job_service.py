from src.database.database import get_connection
from src.services.validation_utils import (
    validate_optional_integer,
    validate_optional_number,
    validate_required_text
)

def create_job(
        nombre,
        tipo_tarea_id,
        estimado_tiempo=None,
        estimado_unidades=None):

    nombre = validate_job_data(
        nombre,
        tipo_tarea_id,
        estimado_tiempo,
        estimado_unidades
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO jobs (
            nombre,
            tipo_tarea_id,
            fecha_creacion,
            estimado_tiempo,
            estimado_unidades
        )
        VALUES (
            ?,
            ?,
            DATE('now'),
            ?,
            ?
        )
        """,
        (
            nombre,
            tipo_tarea_id,
            estimado_tiempo,
            estimado_unidades
        )
    )

    conn.commit()

    job_id = cursor.lastrowid

    conn.close()

    return job_id

def get_all_active_jobs():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            j.id,
            j.nombre,
            t.nombre,
            j.estimado_tiempo,
            j.estimado_unidades
        FROM jobs j
        JOIN tipos_tarea t
            ON j.tipo_tarea_id = t.id
        WHERE j.activo = 1
        ORDER BY j.id
        """
    )

    jobs = cursor.fetchall()

    conn.close()

    return jobs

def get_job_by_id(job_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            j.id,
            j.nombre,
            j.tipo_tarea_id,
            t.nombre,
            j.estimado_tiempo,
            j.estimado_unidades,
            j.activo
        FROM jobs j
        JOIN tipos_tarea t
            ON j.tipo_tarea_id = t.id
        WHERE j.id = ?
        """,
        (job_id,)
    )

    job = cursor.fetchone()

    conn.close()

    return job

def update_job(
        job_id,
        nombre,
        tipo_tarea_id,
        estimado_tiempo,
        estimado_unidades):

    nombre = validate_job_data(
        nombre,
        tipo_tarea_id,
        estimado_tiempo,
        estimado_unidades
    )

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE jobs
        SET
            nombre = ?,
            tipo_tarea_id = ?,
            estimado_tiempo = ?,
            estimado_unidades = ?
        WHERE id = ?
        AND activo = 1
        """,
        (
            nombre,
            tipo_tarea_id,
            estimado_tiempo,
            estimado_unidades,
            job_id
        )
    )

    conn.commit()

    filas_afectadas = cursor.rowcount

    conn.close()

    return filas_afectadas > 0

def delete_job(job_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE jobs
        SET activo = 0
        WHERE id = ?
        """,
        (job_id,)
    )

    conn.commit()

    filas_afectadas = cursor.rowcount

    conn.close()

    return filas_afectadas > 0

def restore_job(job_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE jobs
        SET activo = 1
        WHERE id = ?
        """,
        (job_id,)
    )

    conn.commit()

    filas_afectadas = cursor.rowcount

    conn.close()

    return filas_afectadas > 0

#####################
###### Helpers ######
#####################

def validate_job_data(
        nombre,
        tipo_tarea_id,
        estimado_tiempo,
        estimado_unidades):

    nombre = validate_required_text(nombre, "El nombre del trabajo no puede estar vacio.")

    if not active_task_type_exists(tipo_tarea_id):
        raise ValueError("El tipo de tarea seleccionado no existe o esta inactivo.")

    validate_optional_integer(estimado_tiempo, "El tiempo estimado debe ser un numero entero mayor o igual a cero.")

    validate_optional_number(estimado_unidades, "Las unidades estimadas deben ser un numero mayor o igual a cero.")

    return nombre

def active_task_type_exists(tipo_tarea_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM tipos_tarea
        WHERE id = ?
        AND activo = 1
        """,
        (tipo_tarea_id,)
    )

    task_type = cursor.fetchone()

    conn.close()

    return task_type is not None
