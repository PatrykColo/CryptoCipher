from Crypto.Cipher import AES, DES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Util import Counter
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import io

def image_to_bytes(path):
    with Image.open(path) as img:
        img = img.convert("RGB")  #
        byte_io = io.BytesIO()
        img.save(byte_io, format="BMP")
        return byte_io.getvalue()


def bytes_to_image(data, path):
    img = Image.open(io.BytesIO(data))
    img.save(path)


def encrypt_AES(data, mode, key):
    encrypted = None
    iv = None
    nonce = None
    if mode == "ECB":
        cipher = AES.new(key, AES.MODE_ECB)
        encrypted = cipher.encrypt(pad(data, AES.block_size))
    elif mode == "CBC":
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        encrypted = cipher.encrypt(pad(data, AES.block_size))
    elif mode == "CTR":
        nonce = get_random_bytes(8)
        ctr = Counter.new(64, prefix=nonce, initial_value=0)
        cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
        encrypted = cipher.encrypt(data)

    offset = b""
    if iv is not None:
        offset += iv
    if nonce is not None:
        offset += nonce
    return encrypted, offset

def encrypt_DES(data, mode, key):
    encrypted = None
    iv = None
    nonce = None

    if mode == "ECB":
        cipher = DES.new(key, DES.MODE_ECB)
        encrypted = cipher.encrypt(pad(data, DES.block_size))

    elif mode == "CBC":
        iv = get_random_bytes(8)
        cipher = DES.new(key, DES.MODE_CBC, iv=iv)
        encrypted = cipher.encrypt(pad(data, DES.block_size))

    elif mode == "CTR":
        nonce = get_random_bytes(4)
        ctr = Counter.new(32, prefix=nonce, initial_value=0)
        cipher = DES.new(key, DES.MODE_CTR, counter=ctr)
        encrypted = cipher.encrypt(data)

    offset = b""
    if iv is not None:
        offset += iv
    if nonce is not None:
        offset += nonce

    return encrypted, offset

def encrypt(path, algType, mode, password):
    print(path, algType, mode, password)
    salt = b'cyberbezpieczenstwo'
    img_bytes = image_to_bytes(path)
    if algType == "AES":
        key = PBKDF2(password, salt, dkLen=16, count=100_000, hmac_hash_module=SHA256)
        encrypted_bytes, offset = encrypt_AES(img_bytes, mode, key)
    else:
        key = PBKDF2(password, salt, dkLen=8, count=100_000, hmac_hash_module=SHA256)
        encrypted_bytes, offset = encrypt_DES(img_bytes, mode, key)

    with open("zaszyfrowany.bin", "wb") as f:
        f.write(offset + encrypted_bytes)

def decrypt_AES(data, mode, key):
    decrypted = None
    if mode == "ECB":
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted = unpad(cipher.decrypt(data), AES.block_size)
    elif mode == "CBC":
        iv = data[:16]
        ciphertext = data[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    elif mode == "CTR":
        nonce = data[:8]
        ciphertext = data[8:]
        ctr = Counter.new(64, prefix=nonce, initial_value=0)
        cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
        decrypted = cipher.decrypt(ciphertext)
    return decrypted

def decrypt_DES(data, mode, key):
    decrypted = None
    if mode == "ECB":
        cipher = DES.new(key, DES.MODE_ECB)
        decrypted = unpad(cipher.decrypt(data), DES.block_size)
    elif mode == "CBC":
        iv = data[:8]
        ciphertext = data[8:]
        cipher = DES.new(key, DES.MODE_CBC, iv=iv)
        decrypted = unpad(cipher.decrypt(ciphertext), DES.block_size)
    elif mode == "CTR":
        nonce = data[:4]
        ciphertext = data[4:]
        ctr = Counter.new(32, prefix=nonce, initial_value=0)
        cipher = DES.new(key, DES.MODE_CTR, counter=ctr)
        decrypted = cipher.decrypt(ciphertext)

    return decrypted

def decrypt(path, algType, mode, password):
    print(path, algType, mode, password)
    with open(path, "rb") as f:
        data = f.read()
    salt = b'cyberbezpieczenstwo'
    decrypted_bytes = None
    if algType == "AES":
        key = PBKDF2(password, salt, dkLen=16, count=100_000, hmac_hash_module=SHA256)
        decrypted_bytes = decrypt_AES(data, mode, key)
    elif algType == "DES":
        key = PBKDF2(password, salt, dkLen=8, count=100_000, hmac_hash_module=SHA256)
        decrypted_bytes = decrypt_DES(data, mode, key)

    bytes_to_image(decrypted_bytes, "odszyfrowany_obrazek.bmp")
