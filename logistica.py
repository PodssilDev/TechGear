import random
import psycopg2
from faker import Faker

# Credenciales 
host = 'bd-logistica.postgres.database.azure.com'
dbname = 'postgres'
user = 'logistica'
password = 'Arqui1234!'

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host
)

cursor = conn.cursor()

# Datos sintéticos
fake = Faker()

categorias = [
    'computadores',
    'telefonos celulares',
    'smartwatches',
    'tablets',
    'audifonos',
    'monitores'
]

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

# Lista de sucursales 
sucursales = [
    {'id': 1, 'nombre': 'Sucursal 1', 'direccion': fake.address()},
    {'id': 2, 'nombre': 'Sucursal 2', 'direccion': fake.address()},
    {'id': 3, 'nombre': 'Sucursal 3', 'direccion': fake.address()}
]


def generar_productos(productos_especificos):
    productos_detalles = {}
    id_producto = 1
    for categoria, productos in productos_especificos.items():
        detalles_categoria = {}
        for producto in productos:
            precio_venta = random.randint(10000, 2000000)  
            precio_compra = random.randint(5000, precio_venta)  
            rut_proveedor = fake.unique.ssn()  
            detalles_producto = {
                'id_producto': id_producto,
                'producto': producto,
                'precio_venta': precio_venta,
                'precio_compra': precio_compra,
                'rut_proveedor': rut_proveedor
            }
            detalles_categoria[producto] = detalles_producto
            id_producto += 1  
        productos_detalles[categoria] = detalles_categoria
    return productos_detalles

# Función para generar datos falsos de sucursal-departamento
def generar_sucursal_departamento(sucursales_ids, departamentos_ids):
    sucursal_departamento_data = []
    id_sucursal_departamento = 1
    for sucursal_id in sucursales_ids:
        for _ in range(random.randint(1, len(departamentos_ids))):
            departamento_id = random.choice(departamentos_ids)
            sucursal_departamento_data.append((id_sucursal_departamento, sucursal_id, departamento_id))
            id_sucursal_departamento += 1
    return sucursal_departamento_data

def generar_stock_sucursal(sucursales_ids, productos_detalles):
    stock_sucursal = []
    id_stock_sucursal = 1
    for sucursal_id in sucursales_ids:
        for categoria, productos in productos_detalles.items():
            for producto in productos:
                stock = random.randint(0, 100)
                stock_sucursal.append((id_stock_sucursal, stock, productos[producto]['id_producto'], sucursal_id))
                id_stock_sucursal += 1
    return stock_sucursal


def generar_proveedores(n):
    proveedores = []
    for _ in range(n):
        rut_proveedor = fake.unique.ssn()
        nombre = fake.company()
        direccion = fake.address()
        contacto  = fake.random_number(digits=9)
        proveedores.append((rut_proveedor, nombre, direccion, contacto))
    return proveedores

def generar_producto_proveedor(productos_detalles, proveedores):
    producto_proveedor = []
    for categoria, productos in productos_detalles.items():
        for producto in productos:
            rut_proveedor = productos[producto]['rut_proveedor']
            id_producto = productos[producto]['id_producto']
            producto_proveedor.append((rut_proveedor, id_producto))
    return producto_proveedor

productos = generar_productos(productos_especificos)

# Insertar departamentos
for idx, nombre in enumerate(departamentos, start=1):
    cursor.execute(
        """
        INSERT INTO Departamento (id_departamento, nombre) 
        VALUES (%s, %s)
        """,
        (idx, nombre)
    )
    
# Insertar sucursales
for sucursal in sucursales:
    cursor.execute(
        """
        INSERT INTO Sucursal (id_sucursal, direccion, nombre) 
        VALUES (%s, %s, %s)
        """,
        (sucursal['id'], sucursal['direccion'], sucursal['nombre'])
    )
    
# Obtener IDs de sucursales
cursor.execute("SELECT id_sucursal FROM Sucursal")
sucursales_ids = [row[0] for row in cursor.fetchall()]

# Obtener IDs de departamentos
cursor.execute("SELECT id_departamento FROM Departamento")
departamentos_ids = [row[0] for row in cursor.fetchall()]

sucursal_departamento_data = generar_sucursal_departamento(sucursales_ids, departamentos_ids)

# Insertar datos en Sucursal_Departamento
for id_sucursal_departamento, id_sucursal, id_departamento in sucursal_departamento_data:
    cursor.execute(
        "INSERT INTO Sucursal_Departamento (id_sucursal_departamento, id_sucursal, id_departamento) VALUES (%s, %s, %s)",
        (id_sucursal_departamento, id_sucursal, id_departamento)
    )
    

stock_sucursal = generar_stock_sucursal(sucursales_ids, productos)

# Insertar datos en Stock_Sucursal
for id_stock_sucursal, stock, id_producto, id_sucursal in stock_sucursal:
    cursor.execute(
        "INSERT INTO Stock_Sucursal(stock_id, stock, producto_id, sucursal_id) VALUES (%s, %s, %s, %s)",
        (id_stock_sucursal, stock, id_producto, id_sucursal)
    )

proveedores = generar_proveedores(10)

# Insertar datos en Proveedor
for proveedor in proveedores:
    cursor.execute(
        "INSERT INTO Proveedor (rut_proveedor, nombre, direccion, contacto) VALUES (%s, %s, %s, %s)",
        proveedor
    )

# Confirmar las transacciones
conn.commit()

# Cerrar la conexión
cursor.close()
conn.close()