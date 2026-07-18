# 08 — Password Security and Authentication

## Objective
Understand how passwords are stored and cracked, and why hashing/salting
and multi-factor authentication matter.

## Concepts
- **Hashing vs encryption:** hashing is one-way (can't be reversed);
  passwords should be *hashed*, never encrypted, so even the server operator
  can't recover the plaintext.
- **Salting:** adding a random value per password before hashing, so two
  identical passwords don't produce identical hashes — defeats precomputed
  "rainbow table" attacks.
- **Attack types:**
  - *Dictionary attack* — try words from a wordlist
  - *Brute-force attack* — try all possible combinations
  - *Rainbow table* — precomputed hash lookup table
- **MFA (Multi-Factor Authentication):** combining "something you know"
  (password) with "something you have" (OTP/device) so a stolen password
  alone isn't enough.

## Tools Used
John the Ripper, `hashcat`, `/etc/shadow` (Linux hash storage)

## Steps Performed
```bash
# Inspect how Linux stores password hashes (salted SHA-512 by default)
sudo cat /etc/shadow | grep student

# Crack a sample password hash file with a wordlist (John the Ripper)
john --wordlist=/usr/share/wordlists/rockyou.txt sample_hashes.txt
john --show sample_hashes.txt

# Same attack with hashcat, specifying hash type (0 = MD5)
hashcat -m 0 -a 0 sample_hashes.txt /usr/share/wordlists/rockyou.txt
```
> All hashes cracked in this lab were generated locally from test accounts
> created solely for this exercise — not taken from any real system.

## Sample Output / Observations
```
$ sudo cat /etc/shadow | grep student
student:$6$Ab3dEfGh$xyz.../hash.../:19900:0:99999:7:::
```
The `$6$` prefix identifies the SHA-512 algorithm; the string right after it
is the random salt — confirming Linux salts passwords before hashing.

```
$ john --show sample_hashes.txt
testuser:password123
1 password hash cracked
```
A weak, dictionary-word password was cracked in seconds, while a longer
random password in the same file was not cracked within the lab time limit
— demonstrating why password length/randomness matters more than
complexity substitutions like `P@ssw0rd`.

## Conclusion
Weak passwords are crackable in practical time even with modest hardware.
Salting slows down attackers (no precomputed tables), but doesn't help
against a weak password directly targeted with a wordlist — length and
randomness, plus MFA, are the real defenses.
