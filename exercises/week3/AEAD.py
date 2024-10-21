from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
from base64 import b64encode, b64decode

plaintext = b'abcdefghabcdefghabcdefghabcdefgh'
key = b'icandoencryption'
nonce = get_random_bytes(12)  # GCM nonce size
cipher_gcm = AES.new(key, AES.MODE_GCM, nonce=nonce)
ciphertext, tag = cipher_gcm.encrypt_and_digest(plaintext)

cipher_gcm_dec = AES.new(key, AES.MODE_GCM, nonce=nonce)
try:
    decrypted_plaintext = cipher_gcm_dec.decrypt_and_verify(ciphertext, tag)
    integrity_check_gcm = True
except ValueError:
    integrity_check_gcm = False

modified_ciphertext = bytearray(ciphertext)
modified_ciphertext[0] ^= 1  # Flip a bit in the ciphertext to simulate tampering
cipher_gcm_dec_mod = AES.new(key, AES.MODE_GCM, nonce=nonce)
try:
    decrypted_modified_plaintext = cipher_gcm_dec_mod.decrypt_and_verify(modified_ciphertext, tag)
    integrity_check_gcm_mod = True
except ValueError:
    integrity_check_gcm_mod = False

cipher_ctr = AES.new(key, AES.MODE_CTR, nonce=nonce)
ciphertext_ctr = cipher_ctr.encrypt(plaintext)

cipher_ctr_dec = AES.new(key, AES.MODE_CTR, nonce=nonce)
decrypted_plaintext_ctr = cipher_ctr_dec.decrypt(ciphertext_ctr)

{
    "gcm_encryption": (b64encode(ciphertext).decode(), b64encode(tag).decode()),
    "gcm_decryption_successful": decrypted_plaintext.decode(),
    "gcm_modified_decryption_successful": integrity_check_gcm_mod,
    "ctr_decryption_successful": decrypted_plaintext_ctr.decode()
}

