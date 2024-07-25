from stegano import lsb
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os

# Generate a secure key for encryption (save this key to a file for later use)
key = os.urandom(32)
with open("key.bin", "wb") as key_file:
    key_file.write(key)


def encode_image(image_path, message, output_path):
    # Encrypt the message
    iv = os.urandom(16)  # Generate a random initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    # Pad the message using PKCS7 padding
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_message = padder.update(message.encode()) + padder.finalize()

    # Encrypt the padded message
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()

    # Combine IV and ciphertext for embedding
    encrypted_message = iv + ciphertext

    # Hide the encrypted message in the image using LSB steganography
    carrier = lsb.hide(image_path, encrypted_message.hex())

    # Save the stego image
    carrier.save(output_path, format="PNG")
    print(f"Message encoded and saved to {output_path}")


# Example usage
if __name__ == "__main__":
    input_image = "./Images/Apple.png"
    output_image = "./output/encrypted.png"
    secret_message = "Ki obostha kemon acho? ami valoi mon\
    ton kharap ki kora jay bujhte parchina. aowigh gio GH"

    try:
        encode_image(input_image, secret_message, output_image)
    except Exception as e:
        print(f"Error: {e}")
