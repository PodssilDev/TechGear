# BLOQUE DE DEFINICIONES
# ----------------------------------------------------------------------------
# IMPORTACION DE FUNCIONES
# ----------------------------------------------------------------------------
import random
import psycopg2
from faker import Faker

# DEFINICIONES DE FUNCIONES
#----------------------------------------------------------------------------
'''
Entrada: productos_especificos (dict) - Diccionario con los productos específicos por categoría
Salida: productos_detalles (dict) - Diccionario con los detalles de los productos generados
Descripción: Genera datos sintéticos de productos con precios aleatorios y RUT de proveedor único
'''
def generar_productos(productos_especificos):
    productos_detalles = {}
    id_producto = 1  # ID incremental
    for categoria, productos in productos_especificos.items():
        detalles_categoria = {}
        for producto in productos:
            precio_venta = random.randint(10000, 2000000)  # Precio de venta aleatorio
            precio_compra = random.randint(5000, precio_venta)  # Precio de compra aleatorio
            rut_proveedor = fake.unique.ssn()  # RUT de proveedor generado
            detalles_producto = {
                'id_producto': id_producto,
                'producto': producto,
                'precio_venta': precio_venta,
                'precio_compra': precio_compra,
                'rut_proveedor': rut_proveedor
            }
            detalles_categoria[producto] = detalles_producto
            id_producto += 1  # Incrementa el ID del producto
        productos_detalles[categoria] = detalles_categoria
    return productos_detalles


'''
Entradas:
        - sucursales_ids (list) - Lista de IDs de sucursales
        - departamentos_ids (list) - Lista de IDs de departamentos
Salida: sucursal_departamento_data (list) - Lista de tuplas con los datos de relación entre sucursales y departamentos
Descripción: Genera datos de relación entre sucursales y departamentos de forma aleatoria
'''
def generar_sucursal_departamento(sucursales_ids, departamentos_ids):
    sucursal_departamento_data = []
    id_sucursal_departamento = 1
    for sucursal_id in sucursales_ids:
        for _ in range(random.randint(1, len(departamentos_ids))):  # Número aleatorio de departamentos por sucursal
            departamento_id = random.choice(departamentos_ids)
            sucursal_departamento_data.append((id_sucursal_departamento, sucursal_id, departamento_id))
            id_sucursal_departamento += 1
    return sucursal_departamento_data


'''
Entradas:
        - sucursales_ids (list) - Lista de IDs de sucursales
        - productos_detalles (dict) - Diccionario con los detalles de los productos
Salida: stock_productos (list) - Lista de tuplas con los datos de stock de productos por sucursal generados
Descripción: Genera datos de stock de productos por sucursal de forma aleatoria
'''
def generar_stock_productos(sucursales_ids, productos_detalles):
    stock_productos = []
    id_stock_producto = 1
    for sucursal_id in sucursales_ids:
        for categoria, productos in productos_detalles.items():
            for producto in productos:
                stock = random.randint(0, 100)  # Cantidad aleatoria de stock
                stock_productos.append((id_stock_producto, sucursal_id, productos[producto]['id_producto'], stock))
                id_stock_producto += 1
    return stock_productos


'''
Entrada: n (int) - Cantidad de proveedores a generar
Salida: proveedores (list) - Lista de tuplas con los datos de los proveedores generados
Descripción: Genera datos sintéticos de proveedores con RUT único
'''
def generar_proveedores(n):
    proveedores = []
    for _ in range(n):
        rut_proveedor = fake.unique.ssn()
        nombre = fake.company()
        direccion = fake.address()
        contacto  = fake.random_number(digits=9)
        proveedores.append((rut_proveedor, nombre, direccion, contacto))
    return proveedores

'''
Entrada:
        - productos_detalles (dict) - Diccionario con los detalles de los productos
        - proveedores (list) - Lista de tuplas con los datos de los proveedores
Salida: producto_proveedor (list) - Lista de tuplas con los datos de relación entre productos y proveedores
Descripción: Genera datos de relación entre productos y proveedores de forma aleatoria
'''
def generar_producto_proveedor(productos_detalles, proveedores):
    producto_proveedor = []
    for categoria, productos in productos_detalles.items():
        for producto in productos:
            rut_proveedor = productos[producto]['rut_proveedor']
            id_producto = productos[producto]['id_producto']
            producto_proveedor.append((rut_proveedor, id_producto))
    return producto_proveedor


# BLOQUE PRINCIPAL
#----------------------------------------------------------------------------
# Credenciales para la conexión a la base de datos
host = 'bd-logistica.postgres.database.azure.com'
dbname = 'postgres'
user = 'logistica'
password = 'Arqui1234!'

# Establecer la conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host
)

# Crear un cursor para realizar operaciones en la base de datos
cursor = conn.cursor()

# Inicializar Faker para generar datos sintéticos
fake = Faker()

# Lista de categorías de productos
categorias = [
    'computadores',
    'telefonos celulares',
    'smartwatches',
    'tablets',
    'audifonos',
    'monitores'
]

# Diccionario de productos específicos por categoría
productos_especificos = {
    'computadores': [
        'Laptop HP', 'MacBook Pro', 'Dell Inspiron', 'Lenovo ThinkPad', 'Acer Aspire',
        'Asus ZenBook', 'Microsoft Surface', 'Razer Blade', 'MSI Prestige', 'Samsung Notebook'
    ],
    'telefonos celulares': [
        'iPhone 13', 'Samsung Galaxy S21', 'Google Pixel 6', 'OnePlus 9', 'Xiaomi Mi 11',
        'Huawei P40', 'Sony Xperia 5', 'Nokia 8.3', 'Oppo Find X3', 'Motorola Edge'
    ],
    'smartwatches': [
        'Apple Watch Series 7', 'Samsung Galaxy Watch 4', 'Fitbit Versa 3', 'Garmin Forerunner 945',
        'Fossil Gen 6', 'TicWatch Pro 3', 'Huawei Watch GT 2', 'Amazfit GTR 3', 'Suunto 7', 'Withings Steel HR'
    ],
    'tablets': [
        'iPad Pro', 'Samsung Galaxy Tab S7', 'Amazon Fire HD 10', 'Microsoft Surface Go', 'Lenovo Tab P11',
        'Huawei MatePad Pro', 'Asus ZenPad 3S', 'Xiaomi Mi Pad 5', 'Sony Xperia Z4 Tablet', 'Google Pixel Slate'
    ],
    'audifonos': [
        'Sony WH-1000XM4', 'Bose QuietComfort 35 II', 'Apple AirPods Pro', 'Sennheiser Momentum 3',
        'Jabra Elite 85h', 'Beats Solo Pro', 'Bang & Olufsen Beoplay H9', 'Microsoft Surface Headphones 2',
        'Anker Soundcore Life Q30', 'Shure AONIC 50'
    ],
    'monitores': [
        'Dell UltraSharp', 'LG UltraFine', 'Samsung Odyssey G7', 'Asus ROG Swift', 'Acer Predator',
        'BenQ PD3220U', 'HP Z27', 'Philips Brilliance', 'Lenovo ThinkVision', 'ViewSonic Elite'
    ]
}

# Lista de departamentos
departamentos = [
    'Recursos Humanos',
    'Finanzas',
    'Operaciones',
    'Ventas y Marketing',
    'Tecnología de la Información',
    'Legal',
    'Compras'
]

# Lista de sucursales con datos generados por Faker
sucursales = [
    {'id': 1, 'nombre': 'Sucursal 1', 'direccion': fake.address()},
    {'id': 2, 'nombre': 'Sucursal 2', 'direccion': fake.address()},
    {'id': 3, 'nombre': 'Sucursal 3', 'direccion': fake.address()}
]

# Generar productos
productos = generar_productos(productos_especificos)

# Insertar productos en la tabla Producto
for categoria, productos_categoria in productos.items():
    for producto, detalles_producto in productos_categoria.items():
        cursor.execute(
            """INSERT INTO public."Producto" (id_producto, nombre, precio_venta, precio_compra, categoria) VALUES (%s, %s, %s, %s, %s)""",
            (detalles_producto['id_producto'], producto, detalles_producto['precio_venta'], detalles_producto['precio_compra'], categoria)
        )

# Insertar departamentos en la tabla Departamento
for idx, nombre in enumerate(departamentos, start=1):
    cursor.execute(
        """
        INSERT INTO public."Departamento" (id_departamento, nombre) 
        VALUES (%s, %s)
        """,
        (idx, nombre)
    )

# Insertar sucursales en la tabla Sucursal
for sucursal in sucursales:
    cursor.execute(
        """
        INSERT INTO public."Sucursal" (id_sucursal, direccion, nombre) 
        VALUES (%s, %s, %s)
        """,
        (sucursal['id'], sucursal['direccion'], sucursal['nombre'])
    )

# Obtener IDs de sucursales
cursor.execute("""SELECT id_sucursal FROM public."Sucursal" """)
sucursales_ids = [row[0] for row in cursor.fetchall()]

# Obtener IDs de departamentos
cursor.execute("""SELECT id_departamento FROM public."Departamento" """)
departamentos_ids = [row[0] for row in cursor.fetchall()]

# Generar datos de relación entre sucursales y departamentos
sucursal_departamento_data = generar_sucursal_departamento(sucursales_ids, departamentos_ids)

# Insertar datos en Sucursal_Departamento
for id_sucursal_departamento, id_sucursal, id_departamento in sucursal_departamento_data:
    cursor.execute(
        """INSERT INTO public."Sucursal_Departamento" (id_sucursal_departamento, id_sucursal, id_departamento) VALUES (%s, %s, %s)""",
        (id_sucursal_departamento, id_sucursal, id_departamento)
    )

# Generar stock de productos por sucursal
stock_productos = generar_stock_productos(sucursales_ids, productos)

# Insertar datos en Stock_Producto
for id_stock_producto, id_sucursal, id_producto, stock in stock_productos:
    cursor.execute(
        """INSERT INTO public."Stock_Sucursal" (stock_id, id_sucursal, id_producto, stock) VALUES (%s, %s, %s, %s)""",
        (id_stock_producto, id_sucursal, id_producto, stock)
    )

# Generar datos de proveedores
proveedores = generar_proveedores(10)

# Insertar datos en Proveedor
for proveedor in proveedores:
    cursor.execute(
        """INSERT INTO public."Proveedor" (rut_proveedor, nombre, direccion, contacto) VALUES (%s, %s, %s, %s)""",
        proveedor
    )

# Confirmar las transacciones en la base de datos
conn.commit()

# Cerrar el cursor y la conexión a la base de datos
cursor.close()
conn.close()