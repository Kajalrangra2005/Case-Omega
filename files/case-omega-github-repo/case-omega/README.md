# Case Omega - Investigating a Ransomware Attack on a Healthcare Network

![CI](../../actions/workflows/ci.yml/badge.svg)

Simulated end-to-end digital forensic investigation (Assignment 3, Unit 3: Investigation of Cyber Crimes). **All data is fictional.**

## Repository map
| Folder | Contents | Marks area |
|--------|----------|-----------|
| `01_first_responder/` | SOP, scene sketch, evidence tag template | SOP & scene documentation (1.0) |
| `02_evidence_collection/` | dd image, SHA-256, acquisition log, chain of custody, hash validation | Evidence & CoC (2.0) |
| `03_malware_analysis/` | Behaviour analysis, IOCs, YARA, ATT&CK mapping | Malware analysis (2.0) |
| `04_timeline/` | Simulated logs, correlation script, timeline CSV/PNG | Timeline (2.0) |
| `05_report/` | Final legal-technical report (DOCX) | Report (2.0) |
| `screenshots/` | Command-output and timeline screenshots | Supporting |
| `docs/` | Tool summary, workflow, authorship declaration | Documentation (1.0) |
| `.github/workflows/` | CI: structure + Markdown checks | CI (1.0) |

## Key findings
- Phish -> macro -> PowerShell -> `upd_svc.exe` (10 Nov 2026, 02:14 IST)
- LSASS dump, RDP lateral movement with `svc_backup`, USB staging, ~1.8 GB exfiltrated
- Shadow copies deleted, persistence set, **48,213 files encrypted** (`.omega`) 03:35-03:47
- Contained 04:03 IST; image SHA-256 `582b3d79...0702a9` verified against source

Start with [`05_report/Case_Omega_Forensic_Report.docx`](05_report/Case_Omega_Forensic_Report.docx). Reproduction steps: [`docs/tool_summary.md`](docs/tool_summary.md).
