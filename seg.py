import psycopg2
from cryptography.fernet import Fernet

# Leer la clave de encriptación desde un archivo seguro
with open("secret.key", "rb") as key_file:
    key = key_file.read()

# Inicializar Fernet con la clave leída
fernet = Fernet(key)

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

# Desencriptar el número de teléfono usando la clave Fernet
decMessage = fernet.decrypt(encrypted_telefono).decode()

print("decrypted string: ", decMessage)

# Cerrar el cursor y la conexión a la base de datos
cursor.close()
conn.close()
