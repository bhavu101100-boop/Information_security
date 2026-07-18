# 12 — System Log Monitoring and Analysis

## Objective
Learn where Linux stores security-relevant logs and practice spotting signs
of an attack (e.g., brute-force login attempts) inside them.

## Concepts
- **Centralized logging (`/var/log/`):** most system/security events land
  here — `auth.log` (authentication), `syslog` (general), `apache2/access.log`
  (web requests).
- **`journalctl`:** queries the systemd journal, a structured/binary log
  store used on modern distros alongside or instead of flat files.
- **Log correlation:** a single log line rarely tells the whole story;
  patterns across many lines (e.g., 50 failed logins in 1 minute from one
  IP) are what reveal an attack.
- **Fail2ban:** a tool that watches logs in real time and automatically
  firewalls off IPs showing attack patterns — an automated response to what
  we do manually in this lab.

## Tools Used
`journalctl`, `grep`/`awk`, `tail`, `fail2ban`

## Steps Performed
```bash
# Live-tail auth log while generating some failed SSH logins from Kali
sudo tail -f /var/log/auth.log

# From the attacker VM, simulate failed login attempts (for the lab only)
for i in {1..10}; do ssh baduser@192.168.56.20; done

# Search for failed password attempts
sudo grep "Failed password" /var/log/auth.log

# Count failed attempts per source IP
sudo grep "Failed password" /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -nr

# journalctl equivalent, filtered to SSH service, last hour
journalctl -u ssh --since "1 hour ago"

# Install & check fail2ban status
sudo apt install fail2ban -y
sudo fail2ban-client status sshd
```

## Sample Output / Observations
```
$ sudo grep "Failed password" /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -nr
     10 192.168.56.10
```
10 failed attempts from a single IP in a short window is a textbook
brute-force signature — this is exactly the pattern a SOC analyst or an
automated tool like fail2ban looks for.
```
$ sudo fail2ban-client status sshd
Status for the jail: sshd
|- Currently banned: 1
`- Banned IP list: 192.168.56.10
```
Confirms fail2ban detected the same pattern and automatically firewalled the
offending IP after the configured threshold.

## Conclusion
Logs are the raw evidence trail for almost every security investigation;
knowing where to look and how to spot attack patterns (repeated failures
from one source) is a core blue-team skill, and directly feeds the Incident
Response lab.
