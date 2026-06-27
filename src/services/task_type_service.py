from src.database.database import get_connection
from src.services.validation_utils import (
    normalize_text,
    validate_required_text
)

def create_task_type(nombre):

    nombre = validate_task_type_name(nombre)

    existente = get_task_type_by_name(nombre)

    if existente:
        if existente[2] == 1:
            return existente[0]
        raise ValueError("Ya existe un tipo de tarea inactivo con ese nombre. Debe restaurarlo antes de usarlo.")

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

def get_active_task_types():

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

# Cambiado para validar tipos de tarea inactivas tambien.
def get_task_type_by_name(nombre):

    nombre = normalize_text(nombre)

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            nombre,
            activo
        FROM tipos_tarea
        WHERE nombre = ?
        """,
        (nombre,)
    )

    tipo = cursor.fetchone()

    conn.close()

    return tipo

def update_task_type(task_type_id, nuevo_nombre):

    nuevo_nombre = validate_task_type_name(nuevo_nombre)

    existente = get_task_type_by_name(nuevo_nombre)

    if existente and existente[0] != task_type_id:
        raise ValueError("Ya existe un tipo de tarea con ese nombre.")

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tipos_tarea
        SET nombre = ?
        WHERE id = ?
        AND activo = 1
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

#####################
###### Helpers ######
#####################

def validate_task_type_name(nombre):

    return validate_required_text(
        nombre,
        "El nombre del tipo de tarea no puede estar vacio."
    )