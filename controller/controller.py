from Crypto.Cipher import AES, DES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Util import Counter
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import io

def file_to_bytes(path):
    with open(path, "rb") as f:
        return f.read()

def image_to_bytes(path):
    with Image.open(path) as img:
        img = img.convert("RGB")
        byte_io = io.BytesIO()
        img.save(byte_io, format="BMP")
        return byte_io.getvalue()

def bmp_file_size(bmp_raw: bytes):
    # in the bmp header size is located on the second byte and has a size of 4 bytes
    # bmp is always litte endian, always signed
    return int.from_bytes(bmp_raw[2:6], byteorder="little", signed=False)

def bmp_pixel_data_offset(bmp_raw: bytes):
    # at the 10th byte of the header info about where the pixel data starts is stored
    # its called pixel offset, it is 4 byte, little-endian integer
    return int.from_bytes(bmp_raw[10:14], byteorder="little", signed=False)

def bytes_to_image(data, path):
    img = Image.open(io.BytesIO(data))
    img.save(path)

def bytes_to_file(data, path):
    with open(path, "wb") as f:
        f.write(data)

def encrypt_any_file(input_path, output_path, algType, mode, password):
    file_bytes = file_to_bytes(input_path)
    encrypted_bytes, offset = encrypt(file_bytes, algType, mode, password)
    with open(output_path, "wb") as f:
        f.write(offset + encrypted_bytes)

def decrypt_any_file(input_path, output_path, algType, mode, password):
    file_bytes = file_to_bytes(input_path)
    decrypted_bytes = decrypt(file_bytes, algType, mode, password)
    bytes_to_file(decrypted_bytes, output_path)

def encrypt_bmp_file(input_path, output_path, algType, mode, password):
    img_raw = file_to_bytes(input_path)
    pixel_offset = bmp_pixel_data_offset(img_raw)
    encrypted_bytes, encryption_offset \
        = encrypt(img_raw[pixel_offset:], algType, mode, password)
    # don't forget to include the offset!
    encrypted_image = img_raw[:pixel_offset] + encryption_offset + encrypted_bytes
    bytes_to_file(encrypted_image, output_path)

def decrypt_bmp_file(input_path, output_path, algType, mode, password):
    img_raw_encr = file_to_bytes(input_path)
    pixel_offset = bmp_pixel_data_offset(img_raw_encr)
    decrypted_bytes = decrypt(img_raw_encr[pixel_offset:], algType, mode, password)
    decrypted_image = img_raw_encr[:pixel_offset] + decrypted_bytes
    bytes_to_file(decrypted_image, output_path)

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

def encrypt(data, algType, mode, password):
    print(algType, mode, password)
    salt = b'cyberbezpieczenstwo'
    if algType == "AES":
        key = PBKDF2(password, salt, dkLen=16, count=100_000, hmac_hash_module=SHA256)
        encrypted_bytes, offset = encrypt_AES(data, mode, key)
    else:
        key = PBKDF2(password, salt, dkLen=8, count=100_000, hmac_hash_module=SHA256)
        encrypted_bytes, offset = encrypt_DES(data, mode, key)

    return encrypted_bytes, offset

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

def decrypt(data, algType, mode, password):
    print(algType, mode, password)
    salt = b'cyberbezpieczenstwo'
    decrypted_bytes = None
    if algType == "AES":
        key = PBKDF2(password, salt, dkLen=16, count=100_000, hmac_hash_module=SHA256)
        decrypted_bytes = decrypt_AES(data, mode, key)
    elif algType == "DES":
        key = PBKDF2(password, salt, dkLen=8, count=100_000, hmac_hash_module=SHA256)
        decrypted_bytes = decrypt_DES(data, mode, key)

    return decrypted_bytes
