# 02 — Linux System Administration Basics

## Objective
Build the Linux command-line skills every later lab depends on: file
permissions, users/groups, processes, and services.

## Concepts
- **Everything is a file** — devices, sockets, processes all appear in the
  filesystem tree.
- **Permission model:** `rwx` for **owner / group / others**, represented as
  a 3-digit octal number (e.g., `chmod 750`).
- **Root vs normal user:** root can bypass all permission checks — daily work
  should be done as a normal user, elevated with `sudo` only when needed.
- **Process vs service:** a process is a running program instance; a service
  (managed by `systemd`) is a background process configured to start
  automatically.

## Tools Used
`bash`, `chmod`, `chown`, `useradd`, `passwd`, `ps`, `top`, `systemctl`, `grep`, `find`

## Steps Performed
```bash
# User & group management
sudo useradd -m -s /bin/bash student
sudo passwd student
sudo usermod -aG sudo student

# File permissions
ls -l /var/log/auth.log
chmod 640 secret_notes.txt
chown student:student secret_notes.txt

# Process management
ps aux | grep ssh
top
kill -15 <PID>          # graceful terminate
kill -9 <PID>           # force kill

# Service management
sudo systemctl status ssh
sudo systemctl enable ssh
sudo systemctl restart ssh

# Searching
grep -i "failed password" /var/log/auth.log
find / -perm -4000 -type f 2>/dev/null   # find SUID binaries (security check)
```

## Sample Output / Observations
```
$ ls -l secret_notes.txt
-rw-r-----  1 student student  128 Jul 12 10:02 secret_notes.txt
```
`640` means owner can read/write, group can read, others have no access —
appropriate for a file that shouldn't be world-readable.

The `find / -perm -4000` command lists SUID binaries — files that run with
owner (often root) privileges regardless of who executes them. This is a
real audit technique: unexpected SUID binaries are a common privilege-
escalation vector.

## Conclusion
Comfort with permissions, users, and services is what lets you safely
configure and inspect every tool used in later labs (firewalls, logs,
services under attack, etc.).
