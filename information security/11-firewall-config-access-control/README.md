# 11 — Firewall Configuration and Access Control

## Objective
Configure Linux host firewall rules to allow only necessary traffic, and
verify the rules actually block what they should.

## Concepts
- **Default-deny principle:** block everything by default, then explicitly
  allow only what's needed — safer than trying to list every bad thing to
  block.
- **Stateful firewall:** tracks connection state (NEW/ESTABLISHED/RELATED)
  so return traffic for an allowed outbound connection is automatically
  permitted without a separate rule.
- **iptables chains:** `INPUT` (traffic to this host), `OUTPUT` (traffic
  from this host), `FORWARD` (traffic passing through, if acting as a
  router).
- **UFW** is a simpler front-end over iptables for common cases.

## Tools Used
`iptables`, `ufw`, `nmap` (to verify from the attacker VM)

## Steps Performed
```bash
# View current rules
sudo iptables -L -n -v

# Default-deny policy on INPUT
sudo iptables -P INPUT DROP

# Allow loopback
sudo iptables -A INPUT -i lo -j ACCEPT

# Allow established/related connections back in
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH (22) and HTTP (80) only
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Save rules
sudo netfilter-persistent save

# Equivalent with UFW
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw enable
```
Verified from the Kali attacker VM:
```bash
nmap -p 21,22,23,80,3306 192.168.56.20
```

## Sample Output / Observations
Before the firewall rules, Nmap showed ports 21 (FTP), 23 (Telnet), and 3306
(MySQL) all open in addition to 22/80. After applying the default-deny +
allow-list rules above and re-scanning:
```
PORT   STATE    SERVICE
22/tcp open     ssh
80/tcp open     http
21/tcp filtered ftp
23/tcp filtered telnet
3306/tcp filtered mysql
```
"Filtered" (rather than "closed") confirms packets are being silently
dropped by the firewall rather than actively refused — consistent with the
`DROP` policy used above. This shows the firewall successfully reduced the
attack surface identified back in Topic 6's scan.

## Conclusion
A default-deny firewall with an explicit allow-list measurably shrinks the
attack surface — directly verified by re-running the same scan from Topic 6
and seeing fewer open ports.
