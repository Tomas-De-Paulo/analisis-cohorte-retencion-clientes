import duckdb

# Conectar a la base de datos
try:
    con = duckdb.connect('./data/db/e-commerce.duckdb')
    print("Conexión exitosa a la base de datos.")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

# Cargamos los datos de los CSV en la base de datos
# Cargar categorias.csv
try:
    con.sql("""
        CREATE TABLE IF NOT EXISTS categorias AS    
        SELECT * FROM read_csv_auto('./data/raw/categorias.csv')
        """) 

    # Cargar clientes.csv
    con.sql("""
        CREATE TABLE IF NOT EXISTS clientes AS    
        SELECT * FROM read_csv_auto('./data/raw/clientes.csv')
        """)

    # Cargar empleados.csv
    con.sql("""
        CREATE TABLE IF NOT EXISTS empleados AS
        SELECT * FROM read_csv_auto('./data/raw/empleados.csv')
        """)

    # Cargar lineas_pedidos.csv
    con.sql("""
        CREATE TABLE IF NOT EXISTS lineas_pedidos AS
        SELECT * FROM read_csv_auto('./data/raw/lineas_pedido.csv')
        """)

    # Cargar pedidos.csv
    con.sql("""
        CREATE TABLE IF NOT EXISTS pedidos AS
        SELECT * FROM read_csv_auto('./data/raw/pedidos.csv')
        """)

    # Cargar productos.csv
    con.sql("""
        CREATE TABLE IF NOT EXISTS productos AS
        SELECT * FROM read_csv_auto('./data/raw/productos.csv')
        """)

    # Cargar vendedores.csv
    con.sql("""
        CREATE TABLE IF NOT EXISTS vendedores AS
        SELECT * FROM read_csv_auto('./data/raw/vendedores.csv')
        """)

    #  Cargar ventas_diarias.csv
    con.sql("""
        CREATE TABLE IF NOT EXISTS ventas_diarias AS
        SELECT * FROM read_csv_auto('./data/raw/ventas_diarias.csv')
        """)

    # Cargar ventas_mensuales.csv
    con.sql("""
        CREATE TABLE IF NOT EXISTS ventas_mensuales AS
        SELECT * FROM read_csv_auto('./data/raw/ventas_mensuales.csv')
        """)

    print("Datos cargados exitosamente en la base de datos.")
except Exception as e:
    print(f"Error al cargar los datos: {e}")

