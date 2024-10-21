openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048

openssl rsa -in private_key.pem -pubout -out public_key.pem

echo "I promise to complete my homework on time." > promise.txt

openssl dgst -sha256 -sign private_key.pem -out signature.bin promise.txt

openssl base64 -in signature.bin -out signature_base64.txt

openssl dgst -sha256 -verify public_key.pem -signature signature.bin promise.txt

echo "I promise to complete my homework late." > promise.txt

openssl dgst -sha256 -verify public_key.pem -signature signature.bin promise.txt
