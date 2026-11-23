# Tool Summary & Workflow

| Tool | Purpose in this case | Used here? |
|------|----------------------|-----------|
| `dd` | Bit-for-bit disk imaging | Yes (real command on simulated source) |
| `sha256sum` | Integrity hashing / validation | Yes |
| FTK Imager | GUI imaging, verify, directory listing | Steps documented (`02_evidence_collection/hash_validation.md`); not run (Windows GUI) |
| `strings` | Artifact search in image | Yes |
| Python 3 + matplotlib | Log parsing, correlation, timeline chart, visuals | Yes |
| log2timeline / Plaso | Super-timeline from real images | Documented as the production alternative: `log2timeline.py plaso.dump SRV-EHR-01.dd` then `psort.py -o l2tcsv` |
| Volatility 3 | RAM analysis | Documented only (no RAM image in simulation) |
| YARA | Detection rule | Rule written (`03_malware_analysis/omega_detection.yar`) |
| GitHub Actions | Repo structure + Markdown lint | Yes (`.github/workflows/ci.yml`) |

## Workflow
```
First response (SOP, photos, sketch, tags)
        -> Acquisition (dd + SHA-256, chain of custody)
        -> Analysis (artifact search, malware behaviour, IOCs, ATT&CK)
        -> Timeline (parse + correlate logs, visualise)
        -> Report (legal-technical, DOCX)
```

## Reproduce
```bash
pip install matplotlib python-docx
python3 tools/generate_logs.py        # simulated logs
python3 04_timeline/build_timeline.py # timeline.csv, correlation_findings.txt, timeline.png
python3 tools/make_visuals.py         # screenshots + scene sketch
python3 tools/make_report.py          # 05_report/Case_Omega_Forensic_Report.docx
python3 tools/check_structure.py      # same check CI runs
```

## Simulation limitations
All data (hospital, people, hosts, IPs, hashes of the malware) are fictional. The disk image is a 4 MiB synthetic image with planted text artifacts. No real malware was created or executed. Screenshots are rendered from real command output files, not OS screen captures.
