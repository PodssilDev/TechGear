import random
import datetime
import psycopg2
from faker import Faker

# Credenciales 
host = 'bd-cliente.postgres.database.azure.com'
dbname = 'postgres'
user = 'cliente'
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

def generar_clientes(n):
    clientes = []
    for _ in range(n):
        run_cliente = fake.unique.ssn()
        nombre = fake.name()
        correo = fake.email()
        direccion = fake.address()
        telefono = fake.random_number(digits=9)
        clientes.append((run_cliente, nombre, correo, direccion, telefono))
    return clientes

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

def generar_detalles_boleta(n, run_clientes, productos_detalles):
    detalles_boleta = []
    envios = []
    boleta = []
    for _ in range(n):
        run_cliente = random.choice(run_clientes)
        productos = random.choice(list(productos_detalles.keys()))
        id_envio = fake.random_number(digits=6)
        id_boleta = fake.random_number(digits=6)
        
        fecha = fake.date_this_year()
        total = 0
        for producto in productos_detalles[productos]:
            id_detalle_boleta = fake.random_number(digits=6)
            id_producto = productos_detalles[productos][producto]['id_producto']
            cantidad = random.randint(1, 10)
            valor = productos_detalles[productos][producto]['precio_venta'] * cantidad
            total += valor
            detalles_boleta.append((id_detalle_boleta, id_producto, id_envio, id_boleta, cantidad, valor))
            
        # Envios
        envios = generar_envios(envios, fecha, id_envio)  
        
        # Boletas
        boleta.append((id_boleta, run_cliente, fecha, total))     
             
    return detalles_boleta, envios, boleta    
 
def generar_envios(envios, fecha, id_envio):
        metodo_envio = random.choice(["Empresa 1", "Empresa 2", "Empresa 3"])
        precio = random.randint(500, 5000)
        fecha_envio = fecha + datetime.timedelta(days=random.randint(1, 5))  
        fecha_entrega = fecha_envio + datetime.timedelta(days=random.randint(1, 10))
        envios.append((id_envio, metodo_envio, precio, fecha_envio, fecha_entrega))  
        return envios 
        
# Crear datos sintéticos
clientes = generar_clientes(10)
productos = generar_productos(productos_especificos)
run_clientes = [cliente[0] for cliente in clientes]

detalles_boleta, envios, boletas = generar_detalles_boleta(10, run_clientes, productos)

# Insertar datos en la tabla Cliente
for cliente in clientes:
    cursor.execute("""
        INSERT INTO public."Cliente" (run_cliente, nombre, correo, direccion, telefono)
        VALUES (%s, %s, %s, %s, %s)
    """, cliente)

# Insertar datos en la tabla Producto
for categoria, productos_categoria in productos.items():
    for producto, detalles_producto in productos_categoria.items():
        cursor.execute("""
            INSERT INTO public."Producto" (id_producto, nombre, precio_venta, precio_compra, categoria, rut_proveedor)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (detalles_producto['id_producto'], producto, detalles_producto['precio_venta'], detalles_producto['precio_compra'], categoria, detalles_producto['rut_proveedor']))

# Insertar datos en la tabla Envio
for envio in envios:
    cursor.execute("""
        INSERT INTO public."Envio" (id_envio, metodo_envio, precio, fecha_envio, fecha_entrega)
        VALUES (%s, %s, %s, %s, %s)
    """, envio)

# Insertar datos en la tabla Boleta 
for boleta in boletas:
    cursor.execute("""
        INSERT INTO public."Boleta" (id_boleta, run_cliente, fecha, total)
        VALUES (%s, %s, %s, %s)
    """, boleta)

# Insertar datos en la tabla Detalle_boleta
for detalle_boleta in detalles_boleta:
    cursor.execute("""
        INSERT INTO public."Detalle_boleta" (id_detalle_boleta, id_producto, id_envio, id_boleta, cantidad, valor)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, detalle_boleta)

# Confirmar las transacciones
conn.commit()

# Cerrar la conexión
cursor.close()
conn.close()