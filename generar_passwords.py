import streamlit_authenticator as stauth

# 🔹 Lista de contraseñas sin cifrar
contraseñas = ["prueba1", "prueba2"]

# 🔹 Generar los hashes
contraseñas_hash = []
hasher = stauth.Hasher()
for password in contraseñas:
    contraseñas_hash.append(hasher.hash(password))

# 🔹 Mostrar las contraseñas cifradas
print(contraseñas_hash)
