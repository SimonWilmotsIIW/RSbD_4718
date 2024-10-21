from hashlib import pbkdf2_hmac

password = b"password"
salt = b"salt"

hash = pbkdf2_hmac("sha256", password, salt, iterations=1000)

print(hash.hex());
