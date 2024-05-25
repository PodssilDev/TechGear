import random
from faker import Faker
import mysql.connector

# BD Inventario
config_inventario = {
  'user': 'inventario',
  'password': 'Arqui1234!',
  'host': 'bd-inventario.mysql.database.azure.com',
  'database': 'inventario_data',  
}

conn_inventario = mysql.connector.connect(**config_inventario)
cursor_inventario = conn_inventario.cursor()

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
    # ID incremental
    id_producto = 1
    for categoria, productos in productos_especificos.items():
        detalles_categoria = {}
        # Para cada producto genera una tupla 
        for producto in productos:
            precio_venta = random.randint(10000, 2000000)  
            precio_compra = random.randint(5000, precio_venta)  
            detalles_producto = {
                'id_producto': id_producto,
                'producto': producto,
                'precio_venta': precio_venta,
                'precio_compra': precio_compra,
            }
            detalles_categoria[producto] = detalles_producto
            id_producto += 1  
        productos_detalles[categoria] = detalles_categoria
    return productos_detalles

def generar_sucursal_departamento(sucursales_ids, departamentos_ids):
    sucursal_departamento_data = []
    id_sucursal_departamento = 1
    for sucursal_id in sucursales_ids:
        for _ in range(random.randint(1, len(departamentos_ids))):  
            departamento_id = random.choice(departamentos_ids)
            sucursal_departamento_data.append((id_sucursal_departamento, sucursal_id, departamento_id))
            id_sucursal_departamento += 1
    return sucursal_departamento_data  # Añade esta línea para devolver los datos generados

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


productos = generar_productos(productos_especificos)

# Insertar datos en la tabla Producto 
for categoria, productos_categoria in productos.items():
    for producto, detalles_producto in productos_categoria.items():
        # BD Inventario
        cursor_inventario.execute("""
            INSERT INTO Producto (id_producto, nombre, precio_venta, precio_compra, categoria)
            VALUES (%s, %s, %s, %s, %s)
        """, (detalles_producto['id_producto'], producto, detalles_producto['precio_venta'], detalles_producto['precio_compra'], categoria))

# Insertar departamentos
for idx, nombre in enumerate(departamentos, start=1):
    cursor_inventario.execute(
        """
        INSERT INTO Departamento (id_departamento, nombre) 
        VALUES (%s, %s)
        """,
        (idx, nombre)
    )
    
# Insertar sucursales
for sucursal in sucursales:
    cursor_inventario.execute(
        """
        INSERT INTO Sucursal (id_sucursal, direccion, nombre) 
        VALUES (%s, %s, %s)
        """,
        (sucursal['id'], sucursal['direccion'], sucursal['nombre'])
    )
    
# Obtener IDs de sucursales
cursor_inventario.execute("SELECT id_sucursal FROM Sucursal")
sucursales_ids = [row[0] for row in cursor_inventario.fetchall()]

# Obtener IDs de departamentos
cursor_inventario.execute("SELECT id_departamento FROM Departamento")
departamentos_ids = [row[0] for row in cursor_inventario.fetchall()]

sucursal_departamento_data = generar_sucursal_departamento(sucursales_ids, departamentos_ids)

# Insertar datos en Sucursal_Departamento
for id_sucursal_departamento, id_sucursal, id_departamento in sucursal_departamento_data:
    cursor_inventario.execute(
        "INSERT INTO Sucursal_Departamento (id_sucursal_departamento, id_sucursal, id_departamento) VALUES (%s, %s, %s)",
        (id_sucursal_departamento, id_sucursal, id_departamento)
    )
    
stock_sucursal = generar_stock_sucursal(sucursales_ids, productos)

# Insertar datos en Stock_Sucursal
for id_stock_sucursal, stock, id_producto, id_sucursal in stock_sucursal:
    cursor_inventario.execute(
        "INSERT INTO Stock_Sucursal(stock_id, stock, producto_id, sucursal_id) VALUES (%s, %s, %s, %s)",
        (id_stock_sucursal, stock, id_producto, id_sucursal)
    )

# Confirmar las transacciones
conn_inventario.commit()

# Cerrar la conexión
cursor_inventario.close()
conn_inventario.close()