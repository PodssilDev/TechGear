# BLOQUE DE DEFINICIONES
# ----------------------------------------------------------------------------
# IMPORTACION DE FUNCIONES
# ----------------------------------------------------------------------------
import random
from faker import Faker
import pymssql

# DEFINICIONES DE FUNCIONES
#----------------------------------------------------------------------------
'''
Entradas:
        - productos_especificos (dict) - Diccionario con los productos específicos por categoría
        - proveedores (list) - Lista de proveedores
Salida: productos_detalles (dict) - Diccionario con los detalles de los productos generados
Descripción: Genera datos sintéticos de productos con precios aleatorios y RUT de proveedor único
'''
def generar_productos(productos_especificos, proveedores):
    productos_detalles = {}
    id_producto = 1  # ID incremental para productos
    for categoria, productos in productos_especificos.items():
        detalles_categoria = {}
        for producto in productos:
            precio_venta = random.randint(10000, 2000000)  # Precio de venta aleatorio
            precio_compra = random.randint(5000, precio_venta)  # Precio de compra aleatorio
            rut = random.choice(proveedores)['rut']  # Seleccionar un proveedor aleatorio
            detalles_producto = {
                'id_producto': id_producto,
                'producto': producto,
                'precio_venta': precio_venta,
                'precio_compra': precio_compra,
                'rut_proveedor': rut,
            }
            detalles_categoria[producto] = detalles_producto
            id_producto += 1  # Incrementar ID del producto
        productos_detalles[categoria] = detalles_categoria
    return productos_detalles


'''
Entradas:
        - productos_ids (list) - Lista de IDs de productos
        - sucursales_ids (list) - Lista de IDs de sucursales
Salida: stock_sucursal_data (list) - Lista de tuplas con los datos de stock de productos por sucursal generados
Descripción: Genera datos de stock de productos por sucursal de forma aleatoria con cantidades aleatorias
'''
def generar_stock_sucursal(productos_ids, sucursales_ids):
    stock_sucursal_data = []
    id_stock_sucursal = 1  # ID incremental para stock
    for sucursal_id in sucursales_ids:
        numero_aleatorio = random.randint((len(productos_ids)*2)//3, len(productos_ids))  # Número aleatorio de productos por sucursal
        productos_reducidos = random.sample(productos_ids, numero_aleatorio)  # Seleccionar productos aleatorios
        for producto_id in productos_reducidos:
            stock = random.randint(5, 100)  # Cantidad aleatoria de stock
            stock_sucursal_data.append((id_stock_sucursal, stock, producto_id, sucursal_id))
            id_stock_sucursal += 1
    return stock_sucursal_data


# BLOQUE PRINCIPAL
#----------------------------------------------------------------------------
try:
    # Conexión a la base de datos usando pymssql
    conn_producto = pymssql.connect(
        server='techgear.database.windows.net',
        user='arquitecturadb',
        password='Arqui2024#',
        database='TechGearDB',
        port=1433,
        encryption='require',
        login_timeout=30
    )
    # Crear un cursor para realizar operaciones en la base de datos
    cursor_producto = conn_producto.cursor()
    # Inicializar Faker para generar datos sintéticos
    fake = Faker()

    # Lista de sucursales con datos falsos generados por Faker
    sucursales = [
        {'id': 1, 'nombre': 'Sucursal 1', 'direccion': fake.address()},
        {'id': 2, 'nombre': 'Sucursal 2', 'direccion': fake.address()},
        {'id': 3, 'nombre': 'Sucursal 3', 'direccion': fake.address()}
    ]

    # Lista de proveedores con datos falsos
    proveedores = [
        {'rut': '11.111.111-1', 'nombre': 'Proveedor 1', 'direccion': fake.address()},
        {'rut': '22.222.222-2', 'nombre': 'Proveedor 2', 'direccion': fake.address()},
        {'rut': '33.333.333-3', 'nombre': 'Proveedor 3', 'direccion': fake.address()},
        {'rut': '44.444.444-4', 'nombre': 'Proveedor 4', 'direccion': fake.address()},
        {'rut': '55.555.555-5', 'nombre': 'Proveedor 5', 'direccion': fake.address()}
    ]

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

    # Generar datos de productos
    productos = generar_productos(productos_especificos, proveedores)
    
    # Desactivar restricciones de llave foránea antes de limpiar las tablas
    cursor_producto.execute("ALTER TABLE Stock_Sucursal NOCHECK CONSTRAINT ALL")
    cursor_producto.execute("ALTER TABLE Producto NOCHECK CONSTRAINT ALL")
    cursor_producto.execute("ALTER TABLE Sucursal NOCHECK CONSTRAINT ALL")
    cursor_producto.execute("ALTER TABLE Proveedor NOCHECK CONSTRAINT ALL")

    # Limpiar las tablas
    cursor_producto.execute("DELETE FROM Stock_Sucursal")
    cursor_producto.execute("DELETE FROM Producto")
    cursor_producto.execute("DELETE FROM Sucursal")
    cursor_producto.execute("DELETE FROM Proveedor")

    # Activar restricciones de llave foránea después de limpiar las tablas
    cursor_producto.execute("ALTER TABLE Stock_Sucursal WITH CHECK CHECK CONSTRAINT ALL")
    cursor_producto.execute("ALTER TABLE Producto WITH CHECK CHECK CONSTRAINT ALL")
    cursor_producto.execute("ALTER TABLE Sucursal WITH CHECK CHECK CONSTRAINT ALL")
    cursor_producto.execute("ALTER TABLE Proveedor WITH CHECK CHECK CONSTRAINT ALL")
    
    # Insertar proveedores en la tabla Proveedor
    for proveedor in proveedores:
        cursor_producto.execute(
            """
            INSERT INTO Proveedor (rut_proveedor, nombre, direccion) 
            VALUES (%s, %s, %s)
            """,
            (proveedor['rut'], proveedor['nombre'], proveedor['direccion'])
        )
        
    # Insertar datos en la tabla Producto 
    for categoria, productos_categoria in productos.items():
        for producto, detalles_producto in productos_categoria.items():
            cursor_producto.execute("""
                INSERT INTO Producto (id_producto, nombre, precio_venta, precio_compra, categoria, rut_proveedor)
                VALUES (%s, %s, %s, %s, %s, %s)
                """, (detalles_producto['id_producto'], producto, detalles_producto['precio_venta'], detalles_producto['precio_compra'], categoria, detalles_producto['rut_proveedor'])
            )

    # Insertar sucursales en la tabla Sucursal
    for sucursal in sucursales:
        cursor_producto.execute(
            """
            INSERT INTO Sucursal (id_sucursal, direccion, nombre) 
            VALUES (%s, %s, %s)
            """,
            (sucursal['id'], sucursal['direccion'], sucursal['nombre'])
        )
    
    # Generar IDs de productos y sucursales para generar stock
    productos_ids = [detalles['id_producto'] for productos_cat in productos.values() for detalles in productos_cat.values()]
    sucursales_ids = [sucursal['id'] for sucursal in sucursales]

    # Generar datos de stock en sucursales
    stock_sucursal_data = generar_stock_sucursal(productos_ids, sucursales_ids)

    # Insertar datos en la tabla Stock_Sucursal
    for stock_sucursal in stock_sucursal_data:
        cursor_producto.execute("""
            INSERT INTO Stock_Sucursal (stock_id, stock, producto_id, sucursal_id)
            VALUES (%s, %s, %s, %s)
            """, stock_sucursal
        )

    # Confirmar las transacciones en la base de datos
    conn_producto.commit()
    
    # Cerrar el cursor y la conexión a la base de datos
    cursor_producto.close()
    conn_producto.close()
    
    print("Codigo ejecutado Exitosamente")

# Manejo de errores
except pymssql.OperationalError as e:
    print(f"Error de conexión: {e}")
except Exception as e:
    print(f"Otro error: {e}")