import duckdb

try:
    con = duckdb.connect('./data/db/e-commerce.duckdb')
    print("Conexión exitosa a la base de datos.")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

try:
    con.sql("""
        CREATE OR REPLACE TABLE actividad_mensual AS
        SELECT
            cb.cliente_id,
            cb.cohorte,
            DATE_TRUNC('month', p.fecha) AS mes_actividad,
            DATEDIFF('month', cb.cohorte, DATE_TRUNC('month', p.fecha)) AS meses_desde_inicio
        FROM cohortes_base cb
        JOIN pedidos p ON cb.cliente_id = p.cliente_id
        WHERE p.estado = 'completado'
            AND p.cliente_id IS NOT NULL
            AND DATEDIFF('month', cb.cohorte, DATE_TRUNC('month', p.fecha)) >= 0;

        -- Verifico la tabla actividad_mensual
        SELECT
            *
        FROM actividad_mensual;
    """).show()
except Exception as e:
    print(f"Error al crear la tabla actividad_mensual: {e}")