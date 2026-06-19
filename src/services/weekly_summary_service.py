from src.database.database import get_connection
from datetime import datetime, timedelta

def get_weekly_statistics(fecha_inicio: str):
    conn = get_connection()

    current_totals = get_weekly_totals(fecha_inicio)

    historical = {}

    for semana in get_available_weeks(conn):

        if semana > fecha_inicio:
            break

        totals = get_weekly_totals(semana)

        for task, value in totals.items():

            historical.setdefault(task, [])
            historical[task].append(value)

    result = {}

    for task, values in historical.items():

        result[task] = {
            "total": current_totals.get(task, 0),
            "promedio": round(sum(values) / len(values), 2),
            "minimo": min(values),
            "maximo": max(values)
        }

    conn.close()

    return result

def get_per_day_summary(fecha_inicio: str):
    conn = get_connection()

    rows = get_week_entries(conn, fecha_inicio)

    inicio_semana = datetime.strptime(fecha_inicio, "%Y-%m-%d")

    result = {}

    for i in range(7):
        day = (
            inicio_semana
            + timedelta(days=i)
        ).strftime("%Y-%m-%d")

        result[day] = {}

    for fecha, tipo, minutos in rows:
        result[fecha][tipo] = minutos

    conn.close()

    return result

def get_weekly_totals(fecha_inicio: str):
    conn = get_connection()

    rows = get_week_entries(conn, fecha_inicio)

    totals = {}

    for _, tipo, minutos in rows:
        totals[tipo] = totals.get(tipo, 0) + minutos

    conn.close()

    return totals

def get_daily_totals(fecha_inicio: str):
    summary = get_per_day_summary(fecha_inicio)

    return {
        day: sum(tasks.values())
        for day, tasks in summary.items()
    }

def get_week_total(fecha_inicio: str):
    totals = get_weekly_totals(fecha_inicio)
    return sum(totals.values())

#####################
###### Helpers ######
#####################

def get_week_entries(conn, fecha_inicio: str):
    fecha_fin = (
        datetime.strptime(
            fecha_inicio,
            "%Y-%m-%d"
        )
        + timedelta(days=6)
    ).strftime("%Y-%m-%d")

    query = f"""
    SELECT
        a.fecha,
        tt.nombre,
        SUM(
            (
                strftime('%s', '1970-01-01 ' || a.hora_fin)
                -
                strftime('%s', '1970-01-01 ' || a.hora_inicio)
            ) / 60
            - a.interrupciones
        ) AS minutos
    FROM actividades a
    JOIN jobs j
        ON a.job_id = j.id
    JOIN tipos_tarea tt
        ON j.tipo_tarea_id = tt.id
    WHERE
        a.activo = 1
        AND a.fecha BETWEEN ? AND ?
    GROUP BY
        a.fecha,
        tt.nombre
    ORDER BY
        a.fecha,
        tt.nombre
    """

    return conn.execute(
        query,
        (fecha_inicio, fecha_fin)
    ).fetchall()

def get_available_weeks(conn):
    semana_inicial = get_psp_start_week(conn)

    if not semana_inicial:
        return []

    row = conn.execute(
        """
        SELECT MAX(fecha)
        FROM actividades
        WHERE activo = 1
        """
    ).fetchone()

    if not row or not row[0]:
        return []

    ultima_fecha = datetime.strptime(row[0], "%Y-%m-%d")
    semana_actual = datetime.strptime(semana_inicial, "%Y-%m-%d")

    weeks = []

    while semana_actual <= ultima_fecha:
        weeks.append(
            semana_actual.strftime("%Y-%m-%d")
        )

        semana_actual += timedelta(days=7)

    return weeks

def get_first_activity_date(conn):
    row = conn.execute(
        """
        SELECT MIN(fecha)
        FROM actividades
        WHERE activo = 1
        """
    ).fetchone()

    return row[0] if row and row[0] else None

def get_psp_start_week(conn):
    first_date = get_first_activity_date(conn)

    if not first_date:
        return None

    first_date = datetime.strptime(
        first_date,
        "%Y-%m-%d"
    )

    monday = first_date - timedelta(days=first_date.weekday())

    return monday.strftime("%Y-%m-%d")