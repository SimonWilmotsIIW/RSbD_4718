import hmac
import hashlib

message = b"hello"
key = b"secret"
hmac_digest = hmac.new(key, message, hashlib.sha256).hexdigest()

is_verified = hmac.compare_digest(hmac_digest, hmac.new(key, message, hashlib.sha256).hexdigest())

modified_message = b"hello!"
is_verified_modified = hmac.compare_digest(hmac_digest, hmac.new(key, modified_message, hashlib.sha256).hexdigest())

print(hmac_digest, is_verified, is_verified_modified)

