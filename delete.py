import mysql.connector

# Configuración para la conexión a la base de datos de RRHH
config_rrhh = {
    'user': 'rrhh',
    'password': 'Arqui1234!',
    'host': 'db-rrhh.mysql.database.azure.com',
    'database': 'rrhh',
}

# Conectar a la base de datos
conn_rrhh = mysql.connector.connect(**config_rrhh)
cursor_rrhh = conn_rrhh.cursor()

try:
    # Deshabilitar las restricciones de claves foráneas temporalmente
    cursor_rrhh.execute("SET FOREIGN_KEY_CHECKS = 0;")

    # Obtener los nombres de todas las tablas en la base de datos
    cursor_rrhh.execute("SHOW TABLES;")
    tablas = cursor_rrhh.fetchall()

    # Iterar sobre cada tabla y eliminar todos los registros
    for tabla in tablas:
        cursor_rrhh.execute(f"DELETE FROM {tabla[0]};")
        print(f"Datos eliminados de la tabla {tabla[0]}")

    # Volver a habilitar las restricciones de claves foráneas
    cursor_rrhh.execute("SET FOREIGN_KEY_CHECKS = 1;")

    # Confirmar los cambios
    conn_rrhh.commit()
    print("Todos los datos de la base de datos han sido eliminados.")

except mysql.connector.Error as err:
    # Si ocurre un error, hacer rollback para deshacer los cambios
    print(f"Error: {err}")
    conn_rrhh.rollback()

finally:
    # Cerrar el cursor y la conexión
    cursor_rrhh.close()
    conn_rrhh.close()
