# 06 — Network Scanning and Enumeration

## Objective
Use Nmap to discover live hosts, open ports, running services, and versions
on the isolated lab target (Metasploitable2).

## Concepts
- **Host discovery:** finding which IPs on a subnet are alive.
- **Port scanning:** checking which TCP/UDP ports respond, revealing running
  services.
- **Service/version detection & OS fingerprinting:** inferring exact
  software versions from how a service responds — critical for the
  Vulnerability Assessment lab that follows.
- **Enumeration:** going deeper than "port is open" to extract usable
  detail (share names, usernames, banner text).

## Tools Used
Nmap, `enum4linux` (SMB enumeration)

## Steps Performed
```bash
# Host discovery across the lab subnet
nmap -sn 192.168.56.0/24

# Full TCP port scan
nmap -p- 192.168.56.20

# Service/version detection + default scripts on discovered ports
nmap -sV -sC -p 21,22,23,80,139,445,3306 192.168.56.20

# OS fingerprinting
sudo nmap -O 192.168.56.20

# SMB enumeration
enum4linux -a 192.168.56.20
```

## Sample Output / Observations
```
PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 2.3.4
22/tcp  open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1
23/tcp  open  telnet      Linux telnetd
80/tcp  open  http        Apache httpd 2.2.8
3306/tcp open  mysql       MySQL 5.0.51a-3ubuntu5
```
Each line tells us the exact service version — that's exactly what's needed
to look up known vulnerabilities in the next lab (Topic 7). For example,
`vsftpd 2.3.4` is a version with a well-documented backdoor vulnerability,
making it a common teaching example in security courses.

## Conclusion
Scanning/enumeration is the "reconnaissance" phase of a security assessment
— you can't assess or fix what you haven't first mapped out. This directly
feeds the Vulnerability Assessment lab.
