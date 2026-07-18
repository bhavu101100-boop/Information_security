# 04 — Network Configuration and Diagnostics

## Objective
Learn to inspect and troubleshoot network configuration using core Linux
networking commands.

## Concepts
- **IP addressing / subnetting:** how hosts are identified and grouped on a
  network (e.g., `192.168.56.0/24`).
- **Routing:** how a packet decides which interface/gateway to leave through.
- **DNS resolution:** translating hostnames to IP addresses.
- **TCP three-way handshake (SYN, SYN-ACK, ACK):** how a TCP connection is
  established — important background for later packet-capture and scanning
  labs.

## Tools Used
`ip`, `ifconfig`, `ping`, `traceroute`, `dig`/`nslookup`, `netstat`/`ss`, `arp`

## Steps Performed
```bash
# Interface & IP info
ip addr show
ip route show

# Reachability
ping -c 4 192.168.56.20

# Path to a host (hop by hop)
traceroute 192.168.56.20

# DNS lookups
dig google.com
nslookup google.com

# Active connections / listening ports
ss -tulnp
netstat -antp

# ARP table (MAC <-> IP mapping on local segment)
arp -a
```

## Sample Output / Observations
```
$ ss -tulnp
Netid  State   Local Address:Port   Peer Address:Port  Process
tcp    LISTEN  0.0.0.0:22           0.0.0.0:*           sshd
tcp    LISTEN  0.0.0.0:80           0.0.0.0:*           apache2
```
This shows which services are listening on which ports — the very first
thing an administrator (or attacker) checks to understand a machine's attack
surface.

```
$ traceroute 192.168.56.20
1  192.168.56.20  0.412 ms
```
Single hop confirms the target is on the same local segment (internal lab
network), consistent with the Topic 3 setup.

## Conclusion
These diagnostic commands are the baseline for every later network-security
lab: you can't secure or attack what you can't first see and understand.
