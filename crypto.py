from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64
import hashlib

def derive_key(password):
    salt = b"this_is_a_salt"
    return PBKDF2(password, salt, dkLen=32)

def encrypt_message(message, password):
    key = derive_key(password)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

def decrypt_message(enc_message, password):
    enc = base64.b64decode(enc_message.encode())
    key = derive_key(password)
    nonce, tag, ciphertext = enc[:16], enc[16:32], enc[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()
