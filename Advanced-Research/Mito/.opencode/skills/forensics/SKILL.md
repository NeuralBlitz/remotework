---
name: forensics
description: Digital forensics, incident response, evidence collection, and forensic analysis
license: MIT
compatibility: opencode
metadata:
  audience: security
  category: cybersecurity
---

## What I do
- Collect digital evidence properly
- Analyze forensic artifacts
- Preserve chain of custody
- Document findings for legal proceedings
- Investigate security incidents
- Recover deleted data

## When to use me
When investigating security incidents, responding to breaches, or conducting digital forensics investigations.

## Evidence Collection

### Order of Volatility
1. CPU registers, cache
2. Network connections
3. Running processes
4. Memory (RAM)
5. Network traffic
6. Disk
7. Remote logs
8. Physical config
9. Media (archival)

### Collection Methods
- Write blockers
- Forensic images (DD, E01)
- Hash verification
- Live vs dead collection
- Remote collection

### Chain of Custody
- Document every access
- Secure storage
- Timestamps
- Who/what/when/why

## Forensic Analysis

### Memory Forensics
- RAM dump analysis
- Volatile data extraction
- Malware detection
- Rootkit identification

### Disk Forensics
- File recovery
- Deleted file analysis
- Metadata examination
- Timeline analysis
- Slack space

### Network Forensics
- Packet capture analysis
- Flow analysis
- Malware communication
- Intrusion detection

### Browser Forensics
- History extraction
- Cookies analysis
- Cache examination
- Bookmarks

### Email Forensics
- Header analysis
- Attachment extraction
- Phishing analysis

## Common Artifacts

### Windows
- Event logs (Security, System, Application)
- Registry (NTUSER.DAT, SAM, SECURITY)
- Prefetch
- Jumplists
- Recent files
- Recycle Bin

### Linux
- Bash history
- System logs (/var/log)
- Audit logs
- Cron jobs
- SSH keys

### macOS
- Unified logs
- Spotlight
- HFS+/APFS metadata
- Keychain
- Safari artifacts

## Tools
- **EnCase**: Commercial forensics
- **FTK**: Full toolkit
- **Autopsy**: Open source
- **Volatility**: Memory forensics
- **Wireshark**: Network analysis
- **The Sleuth Kit**: File system analysis

## Reporting
- Executive summary
- Technical findings
- Evidence catalog
- Recommendations
- Expert testimony preparation
