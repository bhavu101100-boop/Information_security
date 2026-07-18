# 15 — Security Audit and Best Practices

## Objective
Perform a final, structured audit of the lab environment used throughout
the course, and summarize best-practice recommendations — tying together
every previous topic.

## Concepts
- **Security audit vs vulnerability scan:** a scan finds technical flaws; an
  audit is broader — checks configuration, policy, and process against a
  standard/checklist (e.g., CIS Benchmarks).
- **Defense in depth:** no single control is trusted alone — firewall +
  patched software + strong auth + monitoring, layered together.
- **Principle of least privilege:** every account/service gets the minimum
  access it needs, nothing more.

## Tools Used
Manual checklist review, `lynis` (Linux security auditing tool), findings
consolidated from Topics 1–14

## Steps Performed
```bash
# Automated Linux security audit
sudo apt install lynis -y
sudo lynis audit system
```
Reviewed the report's hardening index and warnings, then cross-referenced
against findings from earlier labs.

## Audit Checklist & Findings (consolidated from this course)

| Area | Check | Status | Related Topic |
|---|---|---|---|
| Patching | Vulnerable vsftpd 2.3.4 present | ❌ Fail — needs upgrade | 07 |
| Authentication | Weak/dictionary passwords crackable | ❌ Fail — enforce length/MFA | 08 |
| Encryption | Telnet/FTP send credentials in cleartext | ❌ Fail — replace with SSH/SFTP | 05, 09 |
| Network exposure | Unneeded ports (21, 23, 3306) reachable | ✅ Fixed with firewall rules | 06, 11 |
| Web app | SQLi / XSS present in test app | ❌ Fail (expected — DVWA is intentionally vulnerable) | 10 |
| Logging | Auth logs present and reviewed | ✅ Pass | 12 |
| Intrusion response | fail2ban active on SSH | ✅ Pass | 12, 14 |
| Least privilege | SUID binaries reviewed | ✅ Reviewed, none unexpected | 02 |

## Best-Practice Recommendations
1. Patch/replace outdated service versions immediately (Topic 7 findings).
2. Enforce strong password policy + MFA where possible (Topic 8).
3. Disable cleartext protocols (Telnet, FTP) in favor of SSH/SFTP/HTTPS
   (Topics 5, 9).
4. Default-deny firewall with an explicit allow-list (Topic 11).
5. Centralize and actively monitor logs, with automated response like
   fail2ban for known attack patterns (Topic 12).
6. Validate/sanitize all user input in web applications; use parameterized
   queries (Topic 10).
7. Run periodic audits (this lab) rather than a one-time check — security
   posture drifts over time as new software/services are added.

## Conclusion
This final audit shows how every earlier topic contributes to one coherent
security posture: recon and scanning find the exposure, vulnerability
assessment prioritizes it, and the controls in Topics 8–12 are the actual
fixes — audited here as a whole system rather than isolated labs.
