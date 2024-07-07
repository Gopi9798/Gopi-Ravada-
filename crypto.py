from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

# Generate a key and IV
key = os.urandom(32)  # AES-256
iv = os.urandom(16)

def encrypt(plain_text):
    # Pad the plain text
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plain_text.encode()) + padder.finalize()

    # Encrypt the padded text
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()

    return iv + cipher_text

def decrypt(cipher_text):
    iv = cipher_text[:16]
    actual_cipher_text = cipher_text[16:]

    # Decrypt the cipher text
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plain_text = decryptor.update(actual_cipher_text) + decryptor.finalize()

    # Unpad the plain text
    unpadder = padding.PKCS7(128).unpadder()
    plain_text = unpadder.update(padded_plain_text) + unpadder.finalize()

    return plain_text.decode()

# Example usage
plain_text = "Secret Message"
cipher_text = encrypt(plain_text)
print("Cipher Text:", cipher_text)

decoded_text = decrypt(cipher_text)
print("Decoded Text:", decoded_text)


def main():
    print("Secret Messaging Application")
    while True:
        choice = input("Choose an option:\n1. Encode a message\n2. Decode a message\n3. Exit\n")
        if choice == '1':
            plain_text = input("Enter the plain text message: ")
            cipher_text = encrypt(plain_text)
            print("Encoded Cipher Text:", cipher_text)
        elif choice == '2':
            cipher_text = input("Enter the cipher text to decode (in bytes): ")
            try:
                cipher_text_bytes = eval(cipher_text)  # Convert string to bytes
                decoded_text = decrypt(cipher_text_bytes)
                print("Decoded Plain Text:", decoded_text)
            except Exception as e:
                print("Invalid cipher text or decryption error:", e)
        elif choice == '3':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
