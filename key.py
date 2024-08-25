from cryptography.fernet import Fernet

# Generar una clave segura
key = Fernet.generate_key()

# Mostrar la clave generada
print(key.decode())

# Almacenar la clave en un archivo seguro para referencia futura (opcional)
with open("secret.key", "wb") as key_file:
    key_file.write(key)

# Se debe ejecutar este script para almacenar la clave en Azure Key Vault
# az keyvault secret set --vault-name keyvault-techgear --name encryption-key --value dFNt8L4EHClBbQoEUlPsG2wxpCi-NOQyHgnghYY4-jE= 
