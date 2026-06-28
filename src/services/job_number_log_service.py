from database.database import get_connection


def get_job_number_log():

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            j.id,
            j.nombre,
            a.fecha,
            tt.nombre,
            j.estimado_tiempo,
            j.estimado_unidades,

            (
                (
                    strftime('%s','1970-01-01 ' || a.hora_fin)
                    -
                    strftime('%s','1970-01-01 ' || a.hora_inicio)
                ) / 60
                - a.interrupciones
            ) AS tiempo_real,

            j.tipo_tarea_id

        FROM actividades a

        JOIN jobs j
            ON a.job_id = j.id

        JOIN tipos_tarea tt
            ON j.tipo_tarea_id = tt.id

        WHERE a.activo = 1

        ORDER BY
            a.fecha,
            j.id
        """
    ).fetchall()

    conn.close()

    historial = {}

    resultado = []

    for row in rows:

        (
            job_id,
            job_nombre,
            fecha,
            categoria,
            estimado_tiempo,
            estimado_unidades,
            tiempo_real,
            tipo_id
        ) = row

        if tipo_id not in historial:

            historial[tipo_id] = {
                "tiempo_acumulado": 0,
                "cantidad": 0,
                "maximo": tiempo_real,
                "minimo": tiempo_real
            }

        h = historial[tipo_id]

        h["tiempo_acumulado"] += tiempo_real
        h["cantidad"] += 1

        promedio = round(
            h["tiempo_acumulado"] / h["cantidad"],
            2
        )

        h["maximo"] = max(
            h["maximo"],
            tiempo_real
        )

        h["minimo"] = min(
            h["minimo"],
            tiempo_real
        )

        resultado.append({

            "job_id": job_id,

            "job_nombre": job_nombre,

            "fecha": fecha,

            "categoria": categoria,

            "estimado_tiempo": estimado_tiempo,

            "estimado_unidades": estimado_unidades,

            "tiempo_real": tiempo_real,

            "velocidad": promedio,

            "acumulado": h["tiempo_acumulado"],

            "maximo": h["maximo"],

            "minimo": h["minimo"]
        })
    
    return resultado