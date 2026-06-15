from src.database.database import get_connection

def create_job(
        nombre,
        tipo_tarea_id,
        estimado_tiempo=None,
        estimado_unidades=None):

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

def get_all_jobs():

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

def create_task_type(nombre):

    existente = get_task_type_by_name(nombre)

    if existente:
        return existente[0]

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tipos_tarea(nombre)
        VALUES(?)
        """,
        (nombre,)
    )

    conn.commit()

    task_type_id = cursor.lastrowid

    conn.close()

    return task_type_id

def get_all_task_types():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            nombre
        FROM tipos_tarea
        ORDER BY nombre
        """
    )

    tipos = cursor.fetchall()

    conn.close()

    return tipos

def get_task_type_by_name(nombre):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            nombre
        FROM tipos_tarea
        WHERE nombre = ?
        """,
        (nombre,)
    )

    tipo = cursor.fetchone()

    conn.close()

    return tipo