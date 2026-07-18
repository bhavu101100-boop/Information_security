# 05 — Packet Capture and Traffic Analysis

## Objective
Capture live network traffic in the lab and analyze it to understand
protocols and spot unencrypted/sensitive data.

## Concepts
- **Packet sniffing:** capturing raw frames off a network interface.
- **Promiscuous mode:** NIC mode that captures all traffic on the segment,
  not just traffic addressed to this host.
- **Why cleartext protocols are risky:** HTTP, Telnet, and FTP send
  credentials in plain text — anyone capturing the traffic can read them.
  This is the practical reason HTTPS/SSH exist.

## Tools Used
Wireshark (GUI), `tcpdump` (CLI)

## Steps Performed
```bash
# CLI capture, 100 packets, saved to file
sudo tcpdump -i eth0 -c 100 -w capture.pcap

# Filter only HTTP traffic on port 80
sudo tcpdump -i eth0 port 80 -A
```
In Wireshark:
1. Selected the lab interface (`eth0`) and started a capture.
2. On the target VM, logged into a deliberately insecure FTP service running
   on Metasploitable2 (`ftp 192.168.56.20`).
3. Stopped the capture and applied the display filter:
   ```
   ftp
   ```
4. Used **Follow → TCP Stream** on the FTP session to reconstruct the full
   conversation.

## Sample Output / Observations
Following the TCP stream showed the FTP login sequence in plain text:
```
USER msfadmin
PASS ********
230 Login successful.
```
This demonstrates exactly why FTP/Telnet/HTTP are considered insecure for
anything sensitive — the username and password were visible without any
decryption, just by capturing traffic on the same segment.

Repeating the same capture against an SSH session showed only encrypted,
unreadable bytes — confirming SSH protects credentials in transit.

## Conclusion
Packet capture is a foundational skill for both attackers (credential
harvesting on insecure networks) and defenders (spotting exactly this kind
of traffic to flag insecure protocols in an audit — see Topic 15).
