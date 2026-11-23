#!/usr/bin/env python3
"""CI helper: verify required repository structure and that the image hash still matches."""
import hashlib, pathlib, sys
R = pathlib.Path(__file__).resolve().parent.parent
REQUIRED = [
 "README.md", "01_first_responder/SOP_first_responder.md", "01_first_responder/scene_sketch.png",
 "01_first_responder/evidence_tag_template.md", "02_evidence_collection/chain_of_custody.md",
 "02_evidence_collection/hash_validation.md", "02_evidence_collection/hashes.sha256",
 "02_evidence_collection/image/SRV-EHR-01.dd", "03_malware_analysis/malware_analysis.md",
 "03_malware_analysis/iocs.csv", "04_timeline/timeline.csv", "04_timeline/timeline.png",
 "05_report/Case_Omega_Forensic_Report.docx", "docs/tool_summary.md", "docs/authorship_declaration.md",
 "screenshots",
]
missing = [p for p in REQUIRED if not (R / p).exists()]
if missing:
    print("MISSING:", *missing, sep="\n  "); sys.exit(1)
expected = (R/"02_evidence_collection/hashes.sha256").read_text().split()[0]
actual = hashlib.sha256((R/"02_evidence_collection/image/SRV-EHR-01.dd").read_bytes()).hexdigest()
if expected != actual:
    print("HASH MISMATCH - evidence image altered!"); sys.exit(1)
print("Structure OK; image hash verified:", actual)
