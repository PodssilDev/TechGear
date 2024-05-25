import psycopg2
import random
from faker import Faker
import mysql.connector

# Conexión a la base de datos
# BD Cliente
conn_cliente = psycopg2.connect(
    dbname='postgres',
    user='cliente',
    password='Arqui1234!',
    host='bd-cliente.postgres.database.azure.com'
)

cursor_cliente = conn_cliente.cursor()

# BD Logística
conn_logistica = psycopg2.connect(
    dbname='postgres',
    user='logistica',
    password='Arqui1234!',
    host='bd-logistica.postgres.database.azure.com'
)

cursor_logistica = conn_logistica.cursor()

# BD Inventario
config_inventario = {
  'user': 'inventario',
  'password': 'Arqui1234!',
  'host': 'bd-inventario.mysql.database.azure.com',
  'database': 'inventario',  
}

conn_inventario = mysql.connector.connect(**config_inventario)
cursor_inventario = conn_inventario.cursor()

# Datos sintéticos
fake = Faker()

categorias = [
    'Computadores',
    'Telefonos celulares',
    'Smartwatches',
    'Tablets',
    'Audifonos',
    'Monitores'
]

productos_especificos = {
    'Computadores': [
        'Laptop HP', 'MacBook Pro', 'Dell Inspiron', 'Lenovo ThinkPad', 'Acer Aspire',
        'Asus ZenBook', 'Microsoft Surface', 'Razer Blade', 'MSI Prestige', 'Samsung Notebook'
    ],
    'Telefonos celulares': [
        'iPhone 13', 'Samsung Galaxy S21', 'Google Pixel 6', 'OnePlus 9', 'Xiaomi Mi 11',
        'Huawei P40', 'Sony Xperia 5', 'Nokia 8.3', 'Oppo Find X3', 'Motorola Edge'
    ],
    'Smartwatches': [
        'Apple Watch Series 7', 'Samsung Galaxy Watch 4', 'Fitbit Versa 3', 'Garmin Forerunner 945',
        'Fossil Gen 6', 'TicWatch Pro 3', 'Huawei Watch GT 2', 'Amazfit GTR 3', 'Suunto 7', 'Withings Steel HR'
    ],
    'Tablets': [
        'iPad Pro', 'Samsung Galaxy Tab S7', 'Amazon Fire HD 10', 'Microsoft Surface Go', 'Lenovo Tab P11',
        'Huawei MatePad Pro', 'Asus ZenPad 3S', 'Xiaomi Mi Pad 5', 'Sony Xperia Z4 Tablet', 'Google Pixel Slate'
    ],
    'Audifonos': [
        'Sony WH-1000XM4', 'Bose QuietComfort 35 II', 'Apple AirPods Pro', 'Sennheiser Momentum 3',
        'Jabra Elite 85h', 'Beats Solo Pro', 'Bang & Olufsen Beoplay H9', 'Microsoft Surface Headphones 2',
        'Anker Soundcore Life Q30', 'Shure AONIC 50'
    ],
    'Monitores': [
        'Dell UltraSharp', 'LG UltraFine', 'Samsung Odyssey G7', 'Asus ROG Swift', 'Acer Predator',
        'BenQ PD3220U', 'HP Z27', 'Philips Brilliance', 'Lenovo ThinkVision', 'ViewSonic Elite'
    ]
}

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

productos = generar_productos(productos_especificos)

# Insertar datos en la tabla Producto 
for categoria, productos_categoria in productos.items():
    for producto, detalles_producto in productos_categoria.items():
        '''
        # BD Cliente
        cursor_cliente.execute("""
            INSERT INTO public."Producto" (id_producto, nombre, precio_venta, precio_compra, categoria, rut_proveedor)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (detalles_producto['id_producto'], producto, detalles_producto['precio_venta'], detalles_producto['precio_compra'], categoria, detalles_producto['rut_proveedor']))
        
        # BD Logística
        cursor_logistica.execute("""
            INSERT INTO public."Producto" (id_producto, nombre, precio_venta, precio_compra, categoria)
            VALUES (%s, %s, %s, %s, %s)
        """, (detalles_producto['id_producto'], producto, detalles_producto['precio_venta'], detalles_producto['precio_compra'], categoria))
        '''
        # BD Inventario
        cursor_inventario.execute("""
            INSERT INTO Producto (id_producto, nombre, precio_venta, precio_compra, categoria)
            VALUES (%s, %s, %s, %s, %s)
        """, (detalles_producto['id_producto'], producto, detalles_producto['precio_venta'], detalles_producto['precio_compra'], categoria))
        
conn_cliente.commit()
conn_logistica.commit()
conn_inventario.commit()

cursor_cliente.close()
cursor_logistica.close()
conn_inventario.close()
        
