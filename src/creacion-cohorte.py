import duckdb

try:
    con = duckdb.connect('./data/db/e-commerce.duckdb')
    print("Conexión exitosa a la base de datos.")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

# Fecha de la primer compra de cada cliente
con.sql("""
    CREATE OR REPLACE TABLE cohortes_base AS
    SELECT 
        cliente_id,
        DATE_TRUNC('month', MIN(fecha)) AS cohorte,
        MIN(fecha) AS primera_compra
    FROM pedidos
    WHERE estado = 'completado'
        AND cliente_id IS NOT NULL
    GROUP BY cliente_id;

    -- Verifico la tabala cohortes_base
    SELECT
        cohorte,
        COUNT(*) AS clientes
    FROM cohortes_base
    GROUP BY cohorte
    ORDER BY cohorte;
""").show()