# 14 — Incident Response and Security Reporting

## Objective
Practice the standard incident response lifecycle using the earlier labs
(brute-force detection, vulnerable FTP service) as a simulated incident, and
produce a professional incident report.

## Concepts — The IR Lifecycle (NIST SP 800-61)
1. **Preparation** — tools, logging, and playbooks set up *before* an
   incident (this is what Topics 1–12 built).
2. **Identification** — detecting that an incident is happening (Topic 12's
   log analysis: repeated failed logins).
3. **Containment** — stopping it from spreading (e.g., firewall the
   attacking IP — Topic 11/fail2ban).
4. **Eradication** — removing the root cause (e.g., patch/replace the
   vulnerable vsftpd service from Topic 7).
5. **Recovery** — restoring normal, verified-clean operation.
6. **Lessons Learned** — a post-incident report so it doesn't happen again.

## Tools Used
Log files from Topic 12, fail2ban, a written incident report template

## Steps Performed
1. Used the brute-force login attempts captured in Topic 12 as the simulated
   incident trigger.
2. Followed the lifecycle above end-to-end: identified via `auth.log`,
   contained via fail2ban's automatic ban, and documented the vulnerable
   vsftpd service from Topic 7 as a related exposure to eradicate.
3. Wrote up the incident using a standard report template (below).

## Sample Incident Report (template used)

| Field | Detail |
|---|---|
| **Incident ID** | LAB-IR-001 |
| **Date/Time Detected** | 2026-XX-XX, via `auth.log` review |
| **Detected By** | Log monitoring (Topic 12) |
| **Affected System** | Metasploitable2 lab VM (192.168.56.20) |
| **Incident Type** | SSH brute-force login attempt |
| **Indicators (IOCs)** | Source IP 192.168.56.10; 10 failed logins in <1 min |
| **Severity** | Medium (contained automatically, no successful login) |
| **Containment Action** | fail2ban auto-banned source IP after threshold |
| **Root Cause / Related Exposure** | SSH exposed without rate-limiting; vsftpd 2.3.4 backdoor also present on host (Topic 7) |
| **Eradication** | Recommend patching/upgrading vsftpd; keep fail2ban enabled permanently |
| **Recovery** | Verified service availability restored for legitimate users after ban |
| **Lessons Learned** | Rate-limiting/IDS should be part of default server hardening, not added after the fact |

## Conclusion
Incident response isn't just "block the attacker" — it's a repeatable
process (detect → contain → eradicate → recover → document) that ties
together nearly every earlier lab in this course into one workflow.
