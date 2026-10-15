import duckdb

try:
    con = duckdb.connect('./data/db/e-commerce.duckdb')
    print("Conexión exitosa a la base de datos.")  
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

try:
    con.sql("""
        SELECT
            ROUND(AVG(pct_mes_1), 1) AS retencion_promedio_mes_1
        FROM (
            SELECT am.cohorte, 
                ROUND(100.0 * COUNT(DISTINCT am.cliente_id) / MAX(tc.n), 1) AS pct_mes_1
            FROM actividad_mensual am
            JOIN (SELECT cohorte, COUNT(DISTINCT cliente_id) AS n FROM cohortes_base GROUP BY cohorte) tc
                ON tc.cohorte = am.cohorte
            WHERE am.meses_desde_inicio = 1
            GROUP BY am.cohorte
        );        
    """).show()
except Exception as e:
    print(f"Error al ejecutar la consulta: {e}")

try:
    con.sql("""
        -- Metrica 2: Mejor y peor cohorte
        WITH retention_m1 AS (
            SELECT
                am.cohorte,
                ROUND(100.0 * COUNT(DISTINCT am.cliente_id) / MAX(tc.n), 1) AS pct
            FROM actividad_mensual am
            JOIN (SELECT cohorte, COUNT(DISTINCT cliente_id) AS n FROM cohortes_base GROUP BY cohorte) tc
                ON tc.cohorte = am.cohorte
            WHERE am.meses_desde_inicio = 1
            GROUP BY am.cohorte
        )
        SELECT
            cohorte, pct,
            RANK() OVER (ORDER BY pct DESC) AS rank_mejor,
            RANK() OVER (ORDER BY pct ASC) AS rank_peor
        FROM retention_m1
        ORDER BY pct DESC
    """).show()
except Exception as e:
    print(f"Error al ejecutar la consulta: {e}")