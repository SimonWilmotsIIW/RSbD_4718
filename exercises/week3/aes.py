from Crypto.Cipher import AES
import sys

data = b"abcdefg"*4
key = b"icandoencryption"

cipher = AES.new(key, AES.MODE_ECB)
ciphertext = cipher.encrypt(data)
print("ECB", ciphertext.hex())              