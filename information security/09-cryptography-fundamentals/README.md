# 09 — Cryptography Fundamentals

## Objective
Practice symmetric encryption, asymmetric encryption, and hashing using
OpenSSL, and understand when each is used.

## Concepts
- **Symmetric encryption (e.g., AES):** same key encrypts and decrypts —
  fast, but the key must be shared secretly beforehand.
- **Asymmetric encryption (e.g., RSA):** a public/private key pair — anyone
  can encrypt with the public key, only the private key holder can decrypt.
  Solves the key-distribution problem, but is slower.
- **Hashing (e.g., SHA-256):** one-way fingerprint of data, used for
  integrity checking, not encryption.
- **Digital signatures:** hash a message, then encrypt the hash with a
  private key — proves both integrity and authenticity of the sender.
- **In practice (TLS/HTTPS):** asymmetric crypto is used briefly to securely
  exchange a symmetric session key, then symmetric encryption handles the
  actual bulk data — combining the security of asymmetric with the speed of
  symmetric.

## Tools Used
OpenSSL

## Steps Performed
```bash
# Symmetric encryption/decryption (AES-256)
openssl enc -aes-256-cbc -salt -in secret.txt -out secret.enc
openssl enc -aes-256-cbc -d -in secret.enc -out secret_decrypted.txt

# Generate an RSA key pair
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem

# Encrypt with public key, decrypt with private key
openssl rsautl -encrypt -pubin -inkey public.pem -in secret.txt -out secret_rsa.enc
openssl rsautl -decrypt -inkey private.pem -in secret_rsa.enc -out secret_rsa_dec.txt

# Hashing for integrity
sha256sum secret.txt

# Self-signed certificate (used to test a local HTTPS server)
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365
```

## Sample Output / Observations
```
$ sha256sum secret.txt
7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730... secret.txt
```
Changing even one character in `secret.txt` and re-hashing produced a
completely different hash — demonstrating the **avalanche effect**, and why
hashes are useful for detecting tampering (e.g., verifying a downloaded
ISO's checksum, as done in Topic 1).

The RSA-encrypted file could only be decrypted with the matching private
key — attempting decryption with a different key pair failed, confirming
the public/private relationship.

## Conclusion
Symmetric, asymmetric, and hashing each solve a different problem
(confidentiality with speed, secure key exchange, and integrity,
respectively) — real systems like HTTPS combine all three.
