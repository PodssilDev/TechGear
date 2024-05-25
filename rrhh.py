import random
from faker import Faker
import mysql.connector

# Configuración de la conexión a la base de datos RRHH
config_rrhh = {
    'user': 'rrhh',
    'password': 'Arqui1234!',
    'host': 'bd-rrhh.mysql.database.azure.com',
    'database': 'rrhh',
}

conn_rrhh = mysql.connector.connect(**config_rrhh)
cursor_rrhh = conn_rrhh.cursor()

fake = Faker()

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

# Función para generar datos falsos de trabajadores
def generar_trabajadores(num_trabajadores, departamentos_ids):
    trabajadores_data = []
    for _ in range(num_trabajadores):
        run_trabajador = fake.unique.ssn()
        nombre = fake.name()
        correo = fake.email()
        cargo = fake.job()
        sueldo = random.randint(300000, 1000000)
        fecha_ingreso = fake.date_between(start_date='-10y', end_date='today')
        id_departamento = random.choice(departamentos_ids)
        trabajadores_data.append((run_trabajador, nombre, correo, cargo, sueldo, fecha_ingreso, id_departamento))
    return trabajadores_data

# Insertar departamentos
for idx, nombre in enumerate(departamentos, start=1):
    cursor_rrhh.execute(
        """
        INSERT INTO Departamento (id_departamento, nombre) 
        VALUES (%s, %s)
        """,
        (idx, nombre)
    )

# Insertar sucursales
for sucursal in sucursales:
    cursor_rrhh.execute(
        """
        INSERT INTO Sucursal (id_sucursal, direccion, nombre) 
        VALUES (%s, %s, %s)
        """,
        (sucursal['id'], sucursal['direccion'], sucursal['nombre'])
    )

# Obtener IDs de sucursales
cursor_rrhh.execute("SELECT id_sucursal FROM Sucursal")
sucursales_ids = [row[0] for row in cursor_rrhh.fetchall()]

# Obtener IDs de departamentos
cursor_rrhh.execute("SELECT id_departamento FROM Departamento")
departamentos_ids = [row[0] for row in cursor_rrhh.fetchall()]

sucursal_departamento_data = generar_sucursal_departamento(sucursales_ids, departamentos_ids)

# Insertar datos en Sucursal_Departamento
for id_sucursal_departamento, id_sucursal, id_departamento in sucursal_departamento_data:
    cursor_rrhh.execute(
        "INSERT INTO Sucursal_Departamento (id_sucursal_departamento, id_sucursal, id_departamento) VALUES (%s, %s, %s)",
        (id_sucursal_departamento, id_sucursal, id_departamento)
    )

# Generar e insertar datos falsos en la tabla Trabajador
trabajadores_data = generar_trabajadores(100, departamentos_ids)
for trabajador in trabajadores_data:
    cursor_rrhh.execute(
        """
        INSERT INTO Trabajador (run_trabajador, nombre, correo, cargo, sueldo, fecha_ingreso, id_departamento) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        trabajador
    )

# Confirmar cambios y cerrar la conexión
conn_rrhh.commit()
cursor_rrhh.close()
conn_rrhh.close()