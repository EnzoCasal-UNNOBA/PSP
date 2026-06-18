from src.database.database import get_connection


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
        WHERE activo = 1
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
        AND activo = 1
        """,
        (nombre,)
    )

    tipo = cursor.fetchone()

    conn.close()

    return tipo

def update_task_type(task_type_id, nuevo_nombre):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tipos_tarea
        SET nombre = ?
        WHERE id = ?
        """,
        (
            nuevo_nombre,
            task_type_id
        )
    )

    conn.commit()

    filas_afectadas = cursor.rowcount

    conn.close()

    return filas_afectadas > 0

def delete_task_type(task_type_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tipos_tarea
        SET activo = 0
        WHERE id = ?
        """,
        (task_type_id,)
    )

    conn.commit()

    filas_afectadas = cursor.rowcount

    conn.close()

    return filas_afectadas > 0

def get_all_task_types_admin():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            nombre,
            activo
        FROM tipos_tarea
        ORDER BY nombre
        """
    )

    tipos = cursor.fetchall()

    conn.close()

    return tipos

def restore_task_type(task_type_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tipos_tarea
        SET activo = 1
        WHERE id = ?
        """,
        (task_type_id,)
    )

    conn.commit()

    filas_afectadas = cursor.rowcount

    conn.close()

    return filas_afectadas > 0