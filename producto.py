import random
from faker import Faker
import pymssql

# Conexión a la base de datos
# BD Producto

##################
#  DEFINICIONES  #
##################

# Función para generar datos falsos de productos
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


# Función para generar datos falsos de stock_sucursal
def generar_stock_sucursal(productos_ids, sucursales_ids):
    stock_sucursal_data = []
    id_stock_sucursal = 1
    for producto_id in productos_ids:
        for sucursal_id in range(random.randint(1, len(sucursales_ids))): #no estoy seguro
            stock = random.randint(1, 100)
            stock_sucursal_data.append((id_stock_sucursal, stock, producto_id, sucursal_id))
            id_stock_sucursal += 1
    return stock_sucursal_data

############
#  INICIO  #
############

#Se intenta la conexion y los insert, en caso de error, lo muestra en consola.
try:
    
    #Se realiza la conexion usando pymssql
    conn_producto = pymssql.connect(
        server='techgear.database.windows.net',
        user='arquitecturadb',
        password='Arqui2024#',
        database='TechGearDB',
        port=1433,
        encryption='require',
        login_timeout=30
    )
    
    cursor_producto = conn_producto.cursor()
    fake = Faker()

    # Lista de sucursales
    sucursales = [
        {'id': 1, 'nombre': 'Sucursal 1', 'direccion': fake.address()},
        {'id': 2, 'nombre': 'Sucursal 2', 'direccion': fake.address()},
        {'id': 3, 'nombre': 'Sucursal 3', 'direccion': fake.address()}
    ]

    # Lista de proveedores
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

    # Lista de productos específicos
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

    

    productos = generar_productos(productos_especificos)
    
    # Se limpian las tablas desactivando y activando las restricciones de llave foranea
    cursor_producto.execute("ALTER TABLE Stock_Sucursal NOCHECK CONSTRAINT ALL")
    cursor_producto.execute("ALTER TABLE Producto NOCHECK CONSTRAINT ALL")
    cursor_producto.execute("ALTER TABLE Sucursal NOCHECK CONSTRAINT ALL")
    cursor_producto.execute("ALTER TABLE Proveedor NOCHECK CONSTRAINT ALL")

    cursor_producto.execute("DELETE FROM Stock_Sucursal")
    cursor_producto.execute("DELETE FROM Producto")
    cursor_producto.execute("DELETE FROM Sucursal")
    cursor_producto.execute("DELETE FROM Proveedor")

    cursor_producto.execute("ALTER TABLE Stock_Sucursal WITH CHECK CHECK CONSTRAINT ALL")
    cursor_producto.execute("ALTER TABLE Producto WITH CHECK CHECK CONSTRAINT ALL")
    cursor_producto.execute("ALTER TABLE Sucursal WITH CHECK CHECK CONSTRAINT ALL")
    cursor_producto.execute("ALTER TABLE Proveedor WITH CHECK CHECK CONSTRAINT ALL")
    
    # Insertar datos en la tabla Producto 
    for categoria, productos_categoria in productos.items():
        for producto, detalles_producto in productos_categoria.items():
            # BD Inventario
            cursor_producto.execute("""
                INSERT INTO Producto (id_producto, nombre, precio_venta, precio_compra, categoria)
                VALUES (%s, %s, %s, %s, %s)
            """, (detalles_producto['id_producto'], producto, detalles_producto['precio_venta'], detalles_producto['precio_compra'], categoria))

    # Insertar proveedores
    for proveedor in proveedores:
        cursor_producto.execute(
            """
            INSERT INTO Proveedor (rut_proveedor, nombre, direccion) 
            VALUES (%s, %s, %s)
            """,
            (proveedor['rut'], proveedor['nombre'], proveedor['direccion'])
        )

    # Insertar sucursales
    for sucursal in sucursales:
        cursor_producto.execute(
            """
            INSERT INTO Sucursal (id_sucursal, direccion, nombre) 
            VALUES (%s, %s, %s)
            """,
            (sucursal['id'], sucursal['direccion'], sucursal['nombre'])
        )

    # creo que no se debiese generar ids de nada porque ya se creó stock_sucursal en la linea 110

    # Confirmar cambios y cerrar conexión
    conn_producto.commit()
    cursor_producto.close()
    conn_producto.close()
    
    print("Codigo ejecutado Exitosamente")
 
except pymssql.OperationalError as e:
    print(f"Error de conexión: {e}")
except Exception as e:
    print(f"Otro error: {e}")




