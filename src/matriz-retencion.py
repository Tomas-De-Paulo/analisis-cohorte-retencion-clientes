import duckdb

try:
    con = duckdb.connect('./data/db/e-commerce.duckdb')
    print("Conexión exitosa a la base de datos.")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

try:
    con.sql("""
        WITH tamano_cohorte AS (
            SELECT cohorte, COUNT(DISTINCT cliente_id) AS clientes_iniciales
            FROM cohortes_base
            GROUP BY cohorte
        ),
        retencion AS (
            SELECT
                am.cohorte,
                am.meses_desde_inicio,
                COUNT(DISTINCT am.cliente_id) AS clientes_activos
            FROM actividad_mensual am
        GROUP BY am.cohorte, am.meses_desde_inicio
        )
        SELECT
            r.cohorte,
            tc.clientes_iniciales,
            r.meses_desde_inicio,
            r.clientes_activos,
            ROUND(100.0 * r.clientes_activos / tc.clientes_iniciales, 1) AS pct_retencion
        FROM retencion r
        JOIN tamano_cohorte tc ON tc.cohorte = r.cohorte
        WHERE r.meses_desde_inicio <= 6  -- Primeros 6 meses
        ORDER BY r.cohorte, r.meses_desde_inicio;
    """).show()

    con.sql("""
        WITH tamano_cohorte AS (
                    SELECT cohorte, COUNT(DISTINCT cliente_id) AS n
                    FROM cohortes_base GROUP BY cohorte
                ),
                retencion AS (
                    SELECT
                        am.cohorte, am.meses_desde_inicio,
                        COUNT(DISTINCT am.cliente_id) AS activos,
                        ROUND(100.0 * COUNT(DISTINCT am.cliente_id) / MAX(tc.n), 1) AS pct
                    FROM actividad_mensual am
                    JOIN tamano_cohorte tc ON tc.cohorte = am.cohorte
                    GROUP BY am.cohorte, am.meses_desde_inicio
                )
                SELECT
                    cohorte,
                    meses_desde_inicio,
                    pct AS retencion_pct,
                    LAG(pct) OVER (PARTITION BY cohorte ORDER BY meses_desde_inicio) AS pct_mes_anterior,
                    pct - LAG(pct) OVER (PARTITION BY cohorte ORDER BY meses_desde_inicio) AS caida_vs_anterior,
                    -- Media de retencion de TODAS las cohortes en este mismo mes de vida
                    ROUND(AVG(pct) OVER (PARTITION BY meses_desde_inicio), 1) AS media_todas_cohortes
                FROM retencion
                WHERE meses_desde_inicio <= 6
                ORDER BY cohorte, meses_desde_inicio;
    """).show()
except Exception as e:
    print(f"Error al mostrar la matriz de retencion: {e}")