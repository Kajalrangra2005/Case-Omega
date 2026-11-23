# Chain of Custody - Case OMEGA-2026-001

All persons, serials and seal numbers are **fictional (simulation)**.

## Item
| Field | Value |
|-------|-------|
| Item ID | E1-IMG |
| Description | Forensic image of SRV-EHR-01 system disk (raw/dd), 4,194,304 bytes (simulation size) |
| Source | SRV-EHR-01, Server Room B |
| Acquired by | Analyst R. Menon, 2026-11-10 05:10 IST |
| Method | `dd` via software write-protect (simulation); FTK Imager equivalent steps in `docs/tool_summary.md` |
| SHA-256 (source) | `582b3d79b1b5c88b2477365c03984dcb368b1de96237cef2062c6239220702a9` |
| SHA-256 (image) | `582b3d79b1b5c88b2477365c03984dcb368b1de96237cef2062c6239220702a9` |
| Verification | MATCH (see `acquisition_log.txt`, `hashes.sha256`) |
| Storage media | Evidence HDD HDD-EV-009 (sealed, SEAL-000418) |

## Custody log
| # | Date/Time (IST) | Released by (name, sign) | Received by (name, sign) | Purpose | Location | Hash re-verified |
|---|-----------------|--------------------------|--------------------------|---------|----------|------------------|
| 1 | 2026-11-10 04:25 | Insp. A. Verma (First Responder) | R. Menon (Forensic Analyst) | Seizure at scene, imaging | Server Room B | n/a |
| 2 | 2026-11-10 05:40 | R. Menon | S. Iyer (Evidence Custodian) | Secure storage | Evidence room, locker 4 | Yes - match |
| 3 | 2026-11-11 10:00 | S. Iyer | P. Nair (Malware Analyst) | Working copy for analysis (original stays sealed) | Forensic lab | Yes - match |
| 4 | 2026-11-12 17:30 | P. Nair | S. Iyer | Return after analysis | Evidence room, locker 4 | Yes - match |
| 5 | 2026-11-14 11:00 | S. Iyer | Insp. D. Rao (Cyber Cell, Law Enforcement) | Hand-over for investigation | Police Cyber Cell | Yes - match |

## Other items (same form, one per item)
| Item | Description | Seal | Custodian |
|------|-------------|------|-----------|
| E4 | SanDisk Ultra USB 3.0, serial 4C530001230815112394 | SEAL-000419 | S. Iyer |
| E3 | Firewall/DC/mail/VPN log exports (+ SHA-256 list) | SEAL-000420 | S. Iyer |
| E6 | WS-BILL-07 disk image (pending) | SEAL-000421 | S. Iyer |

## Declaration
I certify that the above entries are accurate and the evidence has not been altered since collection.

Signature: ______________  Name/Designation: ______________  Date: ______________
