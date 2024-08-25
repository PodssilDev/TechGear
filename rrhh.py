# BLOQUE DE DEFINICIONES
# ----------------------------------------------------------------------------
# IMPORTACION DE FUNCIONES
# ----------------------------------------------------------------------------
import random
from faker import Faker
import mysql.connector
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# DEFINICIONES DE FUNCIONES
#----------------------------------------------------------------------------
'''
Entradas:
        - sucursales_ids (list) - Lista de IDs de sucursales
        - departamentos_ids (list) - Lista de IDs de departamentos
Salida: sucursal_departamento_data (list) - Lista de tuplas con los datos de relación entre sucursales y departamentos
Descripción: Genera datos de relación entre sucursales y departamentos de forma aleatoria
'''
def generar_sucursal_departamento(sucursales_ids, departamentos_ids):
    sucursal_departamento_data = []
    id_sucursal_departamento = 1  # ID incremental
    for sucursal_id in sucursales_ids:
        for _ in range(random.randint(1, len(departamentos_ids))):  # Número aleatorio de departamentos por sucursal
            departamento_id = random.choice(departamentos_ids)
            sucursal_departamento_data.append((id_sucursal_departamento, sucursal_id, departamento_id))
            id_sucursal_departamento += 1
    return sucursal_departamento_data


'''
Entradas:
        - num_trabajadores (int) - Cantidad de trabajadores a generar
        - departamentos_ids (list) - Lista de IDs de departamentos
        - cargos (list) - Lista de cargos de trabajadores
Salida: trabajadores_data (list) - Lista de tuplas con los datos de los trabajadores generados
Descripción: Genera datos sintéticos de trabajadores con RUT único y sueldo aleatorio por departamento
'''
# Función para generar datos falsos de trabajadores
def generar_trabajadores(num_trabajadores, departamentos_ids, cargos):
    trabajadores_data = []
    for _ in range(num_trabajadores):
        run_trabajador = fake.unique.ssn() # RUT aleatorio
        nombre = fake.name() # Nombre aleatorio
        correo = fake.email() # Correo aleatorio
        cargo = random.choice(cargos) # Cargo aleatorio
        sueldo = random.randint(300000, 1000000)  # Sueldo aleatorio
        fecha_ingreso = fake.date_between(start_date='-10y', end_date='today')
        id_departamento = random.choice(departamentos_ids)
        trabajadores_data.append((run_trabajador, nombre, correo, cargo, sueldo, fecha_ingreso, id_departamento))
    return trabajadores_data


# BLOQUE PRINCIPAL
#----------------------------------------------------------------------------
# Credenciales para la conexión a Azure Key Vault
KVurl = "https://keyvault-techgear.vault.azure.net"
credencial = DefaultAzureCredential()
secretClient = SecretClient(vault_url=KVurl, credential=credencial)

# Obtiene la clave de encriptación del Key Vault
retrieved_secret = secretClient.get_secret("encryption-key")
clave_secreta = retrieved_secret.value
print(clave_secreta)

# Configuración para la conexión a la base de datos de RRHH
config_rrhh = {
    'user': 'rrhh',
    'password': 'Arqui1234!',
    'host': 'db-rrhh.mysql.database.azure.com',
    'database': 'rrhh',
}

# Conexión a la base de datos
conn_rrhh = mysql.connector.connect(**config_rrhh)
# Crear un cursor para realizar operaciones en la base de datos
cursor_rrhh = conn_rrhh.cursor()

# Inicializar Faker para generar datos sintéticos
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

# Lista de cargos de trabajadores
cargos = cargos = [
    'Director de Recursos Humanos',
    'Gerente de Recursos Humanos',
    'Especialista en Desarrollo de Talento',
    'Coordinador de Cultura Corporativa',
    'Director Financiero',
    'Gerente Financiero',
    'Analista Financiero',
    'Especialista en Planificación Financiera',
    'Director de Operaciones',
    'Gerente de Operaciones',
    'Coordinador de Logística',
    'Analista de Cadena de Suministro',
    'Director de Ventas y Marketing',
    'Gerente de Marketing',
    'Analista de Marketing Digital',
    'Especialista en Publicidad y Promociones',
    'Director de Tecnología de la Información',
    'Gerente de TI',
    'Desarrollador Web',
    'Especialista en Ciberseguridad',
    'Administrador de Sistemas',
    'Director Legal',
    'Abogado Corporativo',
    'Especialista en Cumplimiento Legal',
    'Director de Compras',
    'Gerente de Compras',
    'Analista de Compras',
    'Coordinador de Proveedores'
]

# Lista de sucursales con datos generados por Faker
sucursales = [
    {'id': 1, 'nombre': 'Sucursal 1', 'direccion': fake.address()},
    {'id': 2, 'nombre': 'Sucursal 2', 'direccion': fake.address()},
    {'id': 3, 'nombre': 'Sucursal 3', 'direccion': fake.address()}
]

# Insertar departamentos en la tabla Departamento
for idx, nombre in enumerate(departamentos, start=1):
    cursor_rrhh.execute(
        """
        INSERT INTO Departamento (id_departamento, nombre) 
        VALUES (%s, %s)
        """,
        (idx, nombre)
    )

# Insertar sucursales en la tabla Sucursal
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

# Generar datos de relación sucursal-departamento
sucursal_departamento_data = generar_sucursal_departamento(sucursales_ids, departamentos_ids)

# Insertar datos en la tabla Sucursal_Departamento
for id_sucursal_departamento, id_sucursal, id_departamento in sucursal_departamento_data:
    cursor_rrhh.execute(
        "INSERT INTO Sucursal_Departamento (id_sucursal_departamento, id_sucursal, id_departamento) VALUES (%s, %s, %s)",
        (id_sucursal_departamento, id_sucursal, id_departamento)
    )

# Generar e insertar datos falsos en la tabla Trabajador
trabajadores_data = generar_trabajadores(300, departamentos_ids, cargos)
for trabajador in trabajadores_data:
    cursor_rrhh.execute(
        """
        INSERT INTO Trabajador (run_trabajador, nombre, correo, cargo, sueldo, fecha_ingreso, id_departamento) 
        VALUES (AES_ENCRYPT(%s, %s), %s, %s, %s, AES_ENCRYPT(%s, %s), %s, %s)
        """,
        (trabajador[0], clave_secreta, trabajador[1], trabajador[2], trabajador[3], trabajador[4], clave_secreta, trabajador[5], trabajador[6])
    )

# Confirmar las transacciones en la base de datos
conn_rrhh.commit()

# Cerrar el cursor y la conexión a la base de datos
cursor_rrhh.close()
conn_rrhh.close()