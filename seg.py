import mysql.connector
from cryptography.fernet import Fernet
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

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

# Desencriptar datos al consultarlos desde MySQL
cursor_rrhh.execute(
    """
    SELECT 
        AES_DECRYPT(run_trabajador, %s) AS run_trabajador_desencriptado,
        nombre,
        correo,
        cargo,
        CAST(AES_DECRYPT(sueldo, %s) AS CHAR) AS sueldo_desencriptado,
        fecha_ingreso,
        id_departamento
    FROM 
        Trabajador
    """, 
    (clave_secreta, clave_secreta)
)

# Recuperar y procesar los resultados
resultados = cursor_rrhh.fetchall()
for fila in resultados:
    run_trabajador = fila[0].decode() if fila[0] else None
    nombre = fila[1]
    correo = fila[2]
    cargo = fila[3]
    sueldo = fila[4]
    fecha_ingreso = fila[5]
    id_departamento = fila[6]
    print(f"RUT: {run_trabajador}, Nombre: {nombre}, Sueldo: {sueldo}, Cargo: {cargo}")

# Confirmar las transacciones en la base de datos
conn_rrhh.commit()

# Cerrar el cursor y la conexión a la base de datos
cursor_rrhh.close()
conn_rrhh.close()