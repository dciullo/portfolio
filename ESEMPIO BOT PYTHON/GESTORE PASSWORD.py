from cryptography.fernet import Fernet
import json
import os
from getpass import getpass

# --- SETUP: CREA CHIAVE SE NON ESISTE ---
def load_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("secret.key", "rb") as key_file:
            key = key_file.read()
    return key

# --- ENCRYPT / DECRYPT ---
def encrypt_password(password, fernet):
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password, fernet):
    return fernet.decrypt(encrypted_password.encode()).decode()

# --- SALVA / LEGGI PASSWORDS ---
def save_passwords(data):
    with open("passwords.json", "w") as file:
        json.dump(data, file)

def load_passwords():
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            return json.load(file)
    return {}

# --- MAIN ---
def main():
    key = load_key()
    fernet = Fernet(key)
    passwords = load_passwords()

    print("🔐 Gestore Password")
    while True:
        print("\n1. Aggiungi password")
        print("2. Visualizza password")
        print("3. Esci")
        scelta = input("Scegli: ")

        if scelta == "1":
            sito = input("Nome sito: ")
            user = input("Nome utente: ")
            pwd = getpass("Password: ")
            pwd_criptata = encrypt_password(pwd, fernet)
            passwords[sito] = {"user": user, "password": pwd_criptata}
            save_passwords(passwords)
            print("✅ Password salvata!")
        elif scelta == "2":
            sito = input("Nome sito da visualizzare: ")
            if sito in passwords:
                user = passwords[sito]["user"]
                pwd_decriptata = decrypt_password(passwords[sito]["password"], fernet)
                print(f"👤 Utente: {user}")
                print(f"🔑 Password: {pwd_decriptata}")
            else:
                print("❌ Sito non trovato.")
        elif scelta == "3":
            print("👋 Uscita.")
            break
        else:
            print("❗ Scelta non valida.")

if __name__ == "__main__":
    main()
