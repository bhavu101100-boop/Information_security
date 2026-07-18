# 01 — Introduction to Security Tools and Environment Setup

## Objective
Set up a personal security lab and get familiar with the standard toolkit
used throughout the course.

## Concepts
- **Why a lab, not the real internet:** Security tools (scanners, sniffers,
  crackers) can be misused or accidentally cause damage. A closed lab lets
  you learn safely and legally.
- **CIA Triad:** Confidentiality, Integrity, Availability — the three goals
  every security control tries to protect.
- **Offensive vs Defensive tools:** Offensive (Nmap, Metasploit, Burp Suite)
  simulate an attacker to find weaknesses. Defensive (Wireshark, firewalls,
  log analyzers, IDS) detect/block attacks.

## Tools Used
| Tool | Purpose |
|---|---|
| Kali Linux | Pre-built distro with 600+ security tools installed |
| VirtualBox | Hypervisor to run isolated lab VMs |
| Nmap | Network scanner |
| Wireshark | Packet analyzer |
| Metasploit Framework | Exploitation framework |
| John the Ripper | Password cracker |
| OpenSSL | Cryptography toolkit |

## Steps Performed
1. Downloaded Kali Linux ISO from the official site (`kali.org`) and verified
   the SHA256 checksum against the published hash before use.
   ```bash
   sha256sum kali-linux-2024.x-installer-amd64.iso
   ```
2. Installed VirtualBox and created a new VM (2 vCPU, 4 GB RAM, 40 GB disk).
3. Booted Kali and updated the tool repository:
   ```bash
   sudo apt update && sudo apt full-upgrade -y
   ```
4. Verified key tools were installed:
   ```bash
   nmap --version
   wireshark --version
   msfconsole -v
   john --version
   openssl version
   ```
5. Took a VM snapshot (clean state) before doing any further labs, so I could
   always roll back.

## Sample Output / Observations
```
$ nmap --version
Nmap version 7.94 ( https://nmap.org )
```
Confirms the tool is installed and ready. Checksum verification confirmed the
ISO wasn't tampered with/corrupted before install.

## Conclusion
A working, isolated lab environment is the foundation for every later lab —
without it, none of the scanning/exploitation exercises could be done safely
or legally.
