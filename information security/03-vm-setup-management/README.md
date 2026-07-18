# 03 — Virtual Machine Setup and Management

## Objective
Build a multi-VM lab network: an attacker machine (Kali) and an
intentionally vulnerable target (Metasploitable2), isolated from the real
network.

## Concepts
- **Hypervisor (Type 2):** software like VirtualBox/VMware that runs on top
  of a host OS and virtualizes hardware for guest VMs.
- **Networking modes:**
  - *NAT* — VM can reach the internet, outside can't reach VM
  - *Bridged* — VM appears as its own device on the physical LAN
  - *Host-only / Internal Network* — VMs can talk to each other (and
    optionally the host) but **not** the internet or physical LAN — this is
    what's used for attack/target labs
- **Snapshots:** a saved VM state you can roll back to, useful after an
  exploit intentionally breaks the target.

## Tools Used
VirtualBox (Oracle), Kali Linux VM, Metasploitable2 VM

## Steps Performed
1. Created an **Internal Network** named `seclab` in VirtualBox.
2. Attached both the Kali VM and Metasploitable2 VM's network adapter to
   `seclab` (Settings → Network → Attached to: Internal Network).
3. Set static IPs so the machines could reliably find each other:
   - Kali: `192.168.56.10`
   - Metasploitable2: `192.168.56.20`
4. Verified connectivity:
   ```bash
   ping -c 4 192.168.56.20
   ```
5. Took a snapshot of Metasploitable2 immediately after setup:
   ```
   VirtualBox → Machine → Take Snapshot → "clean-install"
   ```
   so it could be reset to a known-vulnerable state after each exploit lab.

## Sample Output / Observations
```
$ ping -c 4 192.168.56.20
4 packets transmitted, 4 received, 0% packet loss
```
Confirms both VMs are on the same isolated segment and can reach each other,
while neither can reach the real internet (verified by `ping 8.8.8.8` timing
out on the Internal Network adapter).

## Conclusion
Isolating the lab network is what makes every later "attack" lab (scanning,
exploitation) safe and legal — nothing here can ever touch a real,
unauthorized system. Snapshots let labs be repeated cleanly.
