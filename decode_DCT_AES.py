from stegano import lsb
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# Use the same key as in the encoding script (read this key from the file)
with open("key.bin", "rb") as key_file:
    key = key_file.read()


def decode_image(image_path):
    # Extract the hidden message from the image using LSB steganography
    hidden_message = lsb.reveal(image_path)
    if hidden_message is None:
        raise ValueError("No hidden message found in the image")

    # Convert the hex string back to bytes
    iv_ciphertext = bytes.fromhex(hidden_message)

    # Extract the IV and ciphertext
    iv = iv_ciphertext[:16]
    ciphertext = iv_ciphertext[16:]

    # Decrypt the message
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove PKCS7 padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    message = unpadder.update(padded_message) + unpadder.finalize()

    return message.decode()


# Example usage
if __name__ == "__main__":
    stego_image = "./output/encrypted.png"
    try:
        decoded_message = decode_image(stego_image)
        print(f"Decoded message: {decoded_message}")
    except Exception as e:
        print(f"Error: {e}")
