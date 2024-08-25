# BLOQUE DE DEFINICIONES
# ----------------------------------------------------------------------------
# IMPORTACION DE FUNCIONES
# ----------------------------------------------------------------------------
import random
import datetime
import psycopg2
from faker import Faker
from cryptography.fernet import Fernet


# DEFINICIONES DE FUNCIONES
#----------------------------------------------------------------------------
'''
Entradas: 
        - n (int) - Cantidad de clientes a generar
        - comunas (list) - Lista de comunas de la Región Metropolitana de Santiago
Salida: clientes (list) - Lista de tuplas con los datos de los clientes generados
Descripción: Genera datos sintéticos de clientes con RUT único
'''
def generar_clientes(n, comunas):
    clientes = []
    for _ in range(n):
        run_cliente = fake.unique.ssn()  # Generar un RUT de cliente único
        nombre = fake.name()  # Generar un nombre
        correo = fake.email()  # Generar un correo electrónico
        direccion = random.choice(comunas)  # Generar una dirección
        telefono = fake.random_number(digits=9)  # Generar un número de teléfono
         # Encriptar el número de teléfono antes de almacenarlo
        telefono_encriptado = cipher_suite.encrypt(str(telefono).encode()).decode('utf-8')
        clientes.append((run_cliente, nombre, correo, direccion, telefono_encriptado))
    return clientes


'''
Entrada: productos_especificos (dict) - Diccionario con los productos específicos por categoría
Salida: productos_detalles (dict) - Diccionario con los detalles de los productos generados
Descripción: Genera datos sintéticos de productos con precios aleatorios y RUT de proveedor único
'''
def generar_productos(productos_especificos):
    productos_detalles = {}
    id_producto = 1
    for categoria, productos in productos_especificos.items():
        detalles_categoria = {}
        for producto in productos:
            precio_venta = random.randint(10000, 2000000)  # Generar un precio de venta aleatorio
            precio_compra = random.randint(5000, precio_venta)  # Generar un precio de compra aleatorio
            rut_proveedor = fake.unique.ssn()  # Generar un RUT de proveedor único
            detalles_producto = {
                'id_producto': id_producto,
                'producto': producto,
                'precio_venta': precio_venta,
                'precio_compra': precio_compra,
                'rut_proveedor': rut_proveedor
            }
            detalles_categoria[producto] = detalles_producto
            id_producto += 1  # Incrementar el ID del producto
        productos_detalles[categoria] = detalles_categoria
    return productos_detalles


'''
Entradas: 
        - n (int) - Cantidad de boletas a generar
        - run_clientes (list) - Lista de RUT de clientes 
        - productos_detalles (dict) - Diccionario con los detalles de los productos
Salidas: 
        - detalles_boleta (list) - Lista de tuplas con los detalles de las boletas generadas
        - envios (list) - Lista de tuplas con los datos de los envíos generados
        - boleta (list) - Lista de tuplas con los datos de las boletas generadas
Descripción: Genera datos sintéticos de boletas y envíos asociados a los clientes y productos
'''
def generar_detalles_boleta(n, run_clientes, productos_detalles):
    detalles_boleta = []
    envios = []
    boleta = []
    for _ in range(n):
        run_cliente = random.choice(run_clientes)  # Seleccionar un cliente aleatorio
        productos = random.choice(list(productos_detalles.keys()))  # Seleccionar una categoría de productos aleatoria
        id_envio = fake.random_number(digits=9)  # Generar un ID de envío aleatorio
        id_boleta = fake.random_number(digits=9)  # Generar un ID de boleta aleatorio       
        fecha = fake.date_this_year()  # Generar una fecha dentro del año actual
        total = 0
        for producto in productos_detalles[productos]:
            id_detalle_boleta = fake.random_number(digits=9)  # Generar un ID de detalle de boleta aleatorio
            id_producto = productos_detalles[productos][producto]['id_producto']
            cantidad = random.randint(1, 10)  # Generar una cantidad aleatoria
            valor = productos_detalles[productos][producto]['precio_venta'] * cantidad  # Calcular el valor total
            total += valor  # Sumar al total de la boleta
            detalles_boleta.append((id_detalle_boleta, id_producto, id_envio, id_boleta, cantidad, valor))      
        # Generar datos de envío
        envios = generar_envios(envios, fecha, id_envio)          
        # Agregar datos de boleta
        boleta.append((id_boleta, run_cliente, fecha, total))            
    return detalles_boleta, envios, boleta    


'''
Entradas: 
        - envios (list) - Lista de tuplas con los datos de los envíos
        - fecha (datetime) - Fecha de referencia para el envío
        - id_envio (int) - ID del envío a generar
Salida: envios (list) - Lista de tuplas con los datos de los envíos generados
Descripción: Genera datos sintéticos de envíos con método de envío, precio, fecha de envío y fecha de entrega
'''
def generar_envios(envios, fecha, id_envio):
    metodo_envio = random.choice(["Empresa 1", "Empresa 2", "Empresa 3"])  # Seleccionar un método de envío aleatorio
    precio = random.randint(500, 5000)  # Generar un precio de envío aleatorio
    fecha_envio = fecha + datetime.timedelta(days=random.randint(1, 5))  # Generar una fecha de envío aleatoria
    fecha_entrega = fecha_envio + datetime.timedelta(days=random.randint(1, 10))  # Generar una fecha de entrega aleatoria
    envios.append((id_envio, metodo_envio, precio, fecha_envio, fecha_entrega))  
    return envios 



# Generar o cargar la clave de encriptación (haz esto una vez y almacénala de forma segura)
key = Fernet.generate_key()
cipher_suite = Fernet(key)


# BLOQUE PRINCIPAL
#----------------------------------------------------------------------------
# Credenciales para la conexión a la base de datos
host = 'cliente-db.postgres.database.azure.com'
dbname = 'postgres'
user = 'cliente'
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

# Lista de comunas de la Región Metropolitana de Santiago
comunas = [
    'Cerrillos',
    'Cerro Navia',
    'Conchalí',
    'El Bosque',
    'Estación Central',
    'Huechuraba',
    'Independencia',
    'La Cisterna',
    'La Florida',
    'La Granja',
    'La Pintana',
    'La Reina',
    'Las Condes',
    'Lo Barnechea',
    'Lo Espejo',
    'Lo Prado',
    'Macul',
    'Maipú',
    'Ñuñoa',
    'Pedro Aguirre Cerda',
    'Peñalolén',
    'Providencia',
    'Pudahuel',
    'Puente Alto',
    'Quilicura',
    'Quinta Normal',
    'Recoleta',
    'Renca',
    'San Joaquín',
    'San Miguel',
    'San Ramón',
    'Santiago',
    'Vitacura'
]

# Crear datos sintéticos
clientes = generar_clientes(200, comunas)
productos = generar_productos(productos_especificos)
run_clientes = [cliente[0] for cliente in clientes]

detalles_boleta, envios, boletas = generar_detalles_boleta(1000, run_clientes, productos)

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

# Confirmar las transacciones en la base de datos
conn.commit()

# Cerrar el cursor y la conexión a la base de datos
cursor.close()
conn.close()