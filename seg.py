import psycopg2
from cryptography.fernet import Fernet
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

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

# Obtener un run_cliente real de la tabla Cliente
cursor.execute("SELECT run_cliente FROM public.\"Cliente\" LIMIT 1;")
run_cliente = cursor.fetchone()[0]  # Recupera el primer run_cliente de la consulta

print(f"run_cliente obtenido de la base de datos: {run_cliente}")

# Recuperar el número de teléfono encriptado de la base de datos usando el run_cliente obtenido
cursor.execute("SELECT telefono FROM public.\"Cliente\" WHERE run_cliente = %s", (run_cliente,))
encrypted_telefono = cursor.fetchone()[0]

# Convertir a bytes si es necesario
if isinstance(encrypted_telefono, memoryview):
    encrypted_telefono = encrypted_telefono.tobytes()


# Configurar la conexión a Azure Key Vault
KVUri = "https://keyvault-techgear.vault.azure.net"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

# Recuperar la clave de encriptación desde el Key Vault
retrieved_secret = client.get_secret("encryption-key")
key = retrieved_secret.value  # La clave se recupera como cadena base64

# Convertir la clave recuperada a bytes para usar con Fernet
key_bytes = key.encode()

# Inicializar Fernet con la clave correcta
try:
    fernet = Fernet(key_bytes)
except ValueError as e:
    print(f"Error: {e}")
    exit()

# Desencriptar el número de teléfono usando la clave Fernet
try:
    decMessage = fernet.decrypt(encrypted_telefono).decode()
    print("Número de teléfono desencriptado:", decMessage)
except Exception as e:
    print(f"Error al desencriptar el número de teléfono: {e}")

# Cerrar el cursor y la conexión a la base de datos
cursor.close()
conn.close()