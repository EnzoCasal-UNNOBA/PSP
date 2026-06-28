from database.database import get_connection
from datetime import datetime, timedelta


# ==========================================================
# Datos principales de una semana
# ==========================================================

def get_week_entries(conn, fecha_inicio: str):

    fecha_fin = (
        datetime.strptime(fecha_inicio, "%Y-%m-%d")
        + timedelta(days=6)
    ).strftime("%Y-%m-%d")

    return conn.execute(
        """
        SELECT
            a.fecha,
            tt.nombre,
            SUM(
                (
                    strftime('%s','1970-01-01 ' || a.hora_fin)
                    -
                    strftime('%s','1970-01-01 ' || a.hora_inicio)
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
        """,
        (
            fecha_inicio,
            fecha_fin
        )
    ).fetchall()


# ==========================================================
# Categorías utilizadas en la semana
# ==========================================================

def get_week_categories(fecha_inicio):

    conn = get_connection()

    rows = get_week_entries(conn, fecha_inicio)

    conn.close()

    categorias = []

    for _, categoria, _ in rows:

        if categoria not in categorias:
            categorias.append(categoria)

    return categorias


# ==========================================================
# Resumen día / categoría
# ==========================================================

def get_per_day_summary(fecha_inicio):

    conn = get_connection()

    rows = get_week_entries(conn, fecha_inicio)

    inicio = datetime.strptime(
        fecha_inicio,
        "%Y-%m-%d"
    )

    resultado = {}

    for i in range(7):

        fecha = (
            inicio +
            timedelta(days=i)
        ).strftime("%Y-%m-%d")

        resultado[fecha] = {}

    for fecha, categoria, minutos in rows:

        resultado[fecha][categoria] = minutos

    conn.close()

    return resultado


# ==========================================================
# Totales por categoría
# ==========================================================

def get_weekly_totals(fecha_inicio):

    resumen = get_per_day_summary(fecha_inicio)

    totales = {}

    for categorias in resumen.values():

        for categoria, minutos in categorias.items():

            totales[categoria] = (
                totales.get(categoria, 0)
                + minutos
            )

    return totales


# ==========================================================
# Totales por día
# ==========================================================

def get_daily_totals(fecha_inicio):

    resumen = get_per_day_summary(fecha_inicio)

    return {

        fecha: sum(categorias.values())

        for fecha, categorias
        in resumen.items()

    }


# ==========================================================
# Total de la semana
# ==========================================================

def get_week_total(fecha_inicio):

    return sum(
        get_weekly_totals(fecha_inicio).values()
    )


# ==========================================================
# Estadísticas PSP
# ==========================================================

def get_weekly_statistics(fecha_inicio):

    semanas = get_available_weeks()

    actual = get_weekly_totals(fecha_inicio)

    historico = {}

    for _, semana in semanas:

        if semana > fecha_inicio:
            break

        totales = get_weekly_totals(semana)

        for categoria, minutos in totales.items():

            historico.setdefault(
                categoria,
                []
            )

            historico[categoria].append(
                minutos
            )

    resultado = {}

    for categoria, valores in historico.items():

        resultado[categoria] = {

            "total":
                actual.get(categoria, 0),

            "promedio":
                round(
                    sum(valores) / len(valores),
                    2
                ),

            "maximo":
                max(valores),

            "minimo":
                min(valores)

        }

    return resultado


# ==========================================================
# Semanas disponibles
# ==========================================================

def get_available_weeks():

    conn = get_connection()

    semana_inicial = get_psp_start_week(conn)

    if not semana_inicial:

        conn.close()

        return []

    row = conn.execute(
        """
        SELECT MAX(fecha)
        FROM actividades
        WHERE activo = 1
        """
    ).fetchone()

    if not row or not row[0]:

        conn.close()

        return []

    ultima_fecha = datetime.strptime(
        row[0],
        "%Y-%m-%d"
    )

    semana_actual = datetime.strptime(
        semana_inicial,
        "%Y-%m-%d"
    )

    semanas = []

    numero = 1

    while semana_actual <= ultima_fecha:

        semanas.append(
            (
                numero,
                semana_actual.strftime("%Y-%m-%d")
            )
        )

        numero += 1

        semana_actual += timedelta(days=7)

    conn.close()

    return semanas


# ==========================================================
# Helpers
# ==========================================================

def get_first_activity_date(conn):

    row = conn.execute(
        """
        SELECT MIN(fecha)
        FROM actividades
        WHERE activo = 1
        """
    ).fetchone()

    if row and row[0]:
        return row[0]

    return None


def get_psp_start_week(conn):

    fecha = get_first_activity_date(conn)

    if not fecha:
        return None

    fecha = datetime.strptime(
        fecha,
        "%Y-%m-%d"
    )

    lunes = fecha - timedelta(
        days=fecha.weekday()
    )

    return lunes.strftime("%Y-%m-%d")