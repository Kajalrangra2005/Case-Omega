#!/usr/bin/env python3
"""Build the final legal-technical report (DOCX)."""
import pathlib
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
R = pathlib.Path(__file__).resolve().parent.parent
d = Document()
st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(11)
for s in d.sections: s.left_margin = s.right_margin = Inches(1)

def H(t, l=1): d.add_heading(t, l)
def P(t, b=False, i=False):
    p = d.add_paragraph(); r = p.add_run(t); r.bold = b; r.italic = i; return p
def B(t): d.add_paragraph(t, style="List Bullet")
def N(t): d.add_paragraph(t, style="List Number")
def T(rows, widths=None, header=True):
    t = d.add_table(rows=len(rows), cols=len(rows[0])); t.style = "Light Grid Accent 1"
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = t.cell(i, j); c.text = str(v)
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(9); r.bold = (i == 0 and header)
    if widths:
        for row in t.rows:
            for j, w in enumerate(widths): row.cells[j].width = Inches(w)
    d.add_paragraph()
def IMG(path, w=6.3, cap=""):
    d.add_picture(str(R/path), width=Inches(w)); d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    if cap:
        c = d.add_paragraph(cap); c.alignment = WD_ALIGN_PARAGRAPH.CENTER; c.runs[0].italic = True; c.runs[0].font.size = Pt(9)

t = d.add_heading("Digital Forensic Investigation Report", 0)
P("Case OMEGA-2026-001: Ransomware Attack on City Hospital Network (Fictional Simulation)", b=True)
T([["Prepared for", "Cyber Crime Cell / Law Enforcement"], ["Prepared by", "Forensic team (student name: ________)"],
   ["Incident date", "10 November 2026 (IST)"], ["Report date", "18 November 2026"],
   ["Classification", "Confidential - Simulated case; all names, IPs and hashes are fictional"]], [1.6, 4.9], header=False)

H("1. Executive Summary")
P("On 10 November 2026 a human-operated ransomware attack (\"Omega\") compromised City Hospital's electronic health record (EHR) server SRV-EHR-01. "
  "An employee in Billing opened a phishing attachment at 02:14 IST. The attacker dumped credentials, moved laterally by RDP using a service account, "
  "staged tools from a USB drive, exfiltrated approximately 1.8 GB to an external server, deleted backups/shadow copies, installed persistence and "
  "encrypted 48,213 files (extension .omega) between 03:35 and 03:47. The incident was contained at 04:03 IST, 1 h 49 min after first execution.")
P("Impact: clinical systems unavailable; patient health records presumed stolen (sensitive personal data); backups on the NAS destroyed. "
  "Evidence was preserved by imaging SRV-EHR-01 with SHA-256 verification and a documented chain of custody. "
  "Offences disclosed include unauthorised access, data theft, extortion and damage to a computer system (Section 7).")

H("2. First Responder Steps")
P("Full SOP: 01_first_responder/SOP_first_responder.md (based on ACPO principles, ISO/IEC 27037 and NIST SP 800-61/86).")
for s in ["Secured Server Room B and started an access log; informed CISO, legal and management.",
          "Did NOT power off the server (RAM volatility); isolated it by unplugging the network cable and blocking 198.51.100.77 at the firewall (04:03).",
          "Disabled compromised accounts (svc_backup, rsharma).",
          "Photographed scene wide/mid/close (P1-P14), drew the scene sketch (Figure 1) and tagged items E1-E9.",
          "Captured volatile data in order of volatility, then seized/imaged media; opened Chain-of-Custody forms.",
          "Reported to CERT-In within the mandated 6-hour window."]: N(s)
IMG("01_first_responder/scene_sketch.png", 6.2, "Figure 1: Scene sketch of Server Room B (not to scale)")
P("Digital evidence identified", b=True)
T([["ID", "Evidence", "Notes"], ["E1", "SRV-EHR-01 server (disk + RAM)", "Primary target; imaged"],
   ["E2", "SRV-DB-02", "Unaffected; baseline"], ["E3", "Firewall/switch/DNS logs", "Exported + hashed"],
   ["E4", "USB SanDisk S/N 4C530001230815112394", "Tool staging"], ["E5", "Backup NAS", "Shadow copies deleted"],
   ["E6", "WS-BILL-07 workstation", "Patient zero"], ["E7", "DC-01, mail gateway, VPN/cloud logs", "Auth + phishing evidence"],
   ["E8", "Ransom note + encrypted samples", "In image"], ["E9", "User mobile devices", "Faraday bag"]], [0.5, 3.2, 2.8])

H("3. Evidence Collection and Acquisition")
P("The system disk of SRV-EHR-01 was acquired through a write-protected path using dd (FTK Imager steps documented as equivalent):")
P("dd if=SRV-EHR-01_source.raw of=SRV-EHR-01.dd bs=4096 conv=noerror,sync", i=True)
T([["Item", "SHA-256"], ["Source (before)", "582b3d79b1b5c88b2477365c03984dcb368b1de96237cef2062c6239220702a9"],
   ["Image (after)", "582b3d79b1b5c88b2477365c03984dcb368b1de96237cef2062c6239220702a9"], ["Result", "MATCH - image is a verified exact copy"]], [1.4, 5.1])
IMG("screenshots/01_dd_acquisition_and_sha256.png", 6.4, "Figure 2: Imaging and hash verification output")
P("Chain of custody: five transfers (scene -> analyst -> evidence custodian -> malware analyst -> custodian -> Cyber Cell) each with hash re-verification. "
  "Analysis used a working copy; the original remains sealed (SEAL-000418). See 02_evidence_collection/chain_of_custody.md.")

H("4. Analysis of Malicious Application Behaviour")
P("Scope note: no live sample was handled; behaviour is derived from telemetry and artifacts recovered from the image. Full detail: 03_malware_analysis/malware_analysis.md.", i=True)
T([["Behaviour", "Finding", "Evidence"],
   ["Encryption", "48,213 files renamed to .omega in 12m10s (~66 files/s); D:\\EHR\\ targeted", "file_audit.log"],
   ["Ransom note", "README_OMEGA.txt in every directory; contact portal omega-recover[.]example", "Image offset 0x30000"],
   ["Persistence", "Scheduled task + Run key 'WinUpdateSvc' -> upd_svc.exe", "process_events.log; offset 0x40000"],
   ["Anti-recovery", "vssadmin delete shadows; wbadmin delete catalog", "process_events.log; offset 0x50000"],
   ["Credential theft", "LSASS dump via comsvcs.dll; password spray; svc_backup abused", "process/auth logs"],
   ["Exfiltration", "rclone (renamed rc.exe) from USB; ~1.8 GB to 198.51.100.77:443", "usb_events, firewall.log"]], [1.2, 3.3, 2.0])
P("Classification: Windows crypto-ransomware with data exfiltration (double extortion), human-operated, medium sophistication. Threat level: CRITICAL (patient-safety impact, sensitive health data, destroyed backups).", b=True)
P("Indicators of Compromise (full list in iocs.csv)", b=True)
T([["Type", "Value"], ["IPv4", "203.0.113.45 (payload), 198.51.100.77 (C2/exfil)"], ["Domains", "mediclaims-portal.example, omega-recover.example"],
   ["Files", "upd_svc.exe, rc.exe, README_OMEGA.txt, *.omega, claim_88213.docm"], ["Persistence", "Task/Run value WinUpdateSvc"],
   ["USB serial", "4C530001230815112394"], ["Account", "svc_backup"]], [1.2, 5.3])
IMG("screenshots/03_strings_artifacts_in_image.png", 6.4, "Figure 3: Attack artifacts recovered from the disk image")

H("5. Attack Timeline and Correlation")
IMG("04_timeline/timeline.png", 6.5, "Figure 4: Attack timeline by kill-chain phase (IST)")
T([["Time (IST)", "Event", "Source"],
   ["02:14", "Macro document opens; PowerShell downloads upd_svc.exe from 203.0.113.45", "process, browser, firewall"],
   ["02:41", "LSASS credential dump on WS-BILL-07", "process"],
   ["02:44-02:58", "svc_backup first used from workstation; password spray; RDP to SRV-EHR-01", "auth, firewall"],
   ["03:10-03:19", "USB inserted; rclone copied; USB removed", "usb_events"],
   ["03:22-03:30", "~1.8 GB uploaded to 198.51.100.77:443", "firewall"],
   ["03:31-03:33", "Shadow copies/backup catalog deleted; persistence created", "process, EDR"],
   ["03:35-03:47", "Encryption of 48,213 files; ransom notes dropped", "file_audit, process"],
   ["03:47-04:03", "EDR critical alert; SOC paged; firewall block + server isolated", "EDR"]], [1.0, 4.0, 1.5])
P("Correlation highlights: USB insertion preceded the bulk upload by ~12 minutes; the upload ended exactly 1 minute before shadow-copy deletion, then encryption began within about 4 minutes; EDR alerted 12.5 minutes after encryption began and containment took a further 15.5 minutes, so detection-to-containment is a key improvement area.")

H("6. Findings and Conclusions")
for s in ["Initial access was via phishing (SPF fail) targeting the Billing department.",
          "A privileged service account (svc_backup) with weak controls enabled lateral movement; no MFA on RDP.",
          "Backups were reachable from the production network and were deleted.",
          "Data exfiltration occurred before encryption; this must be treated as a personal-data breach.",
          "Attribution is not established; infrastructure indicators have been provided to law enforcement."]: B(s)

H("7. Applicable Legal Provisions (India)")
P("Note: this section is for academic purposes; sections should be verified against current official texts and counsel. The Bharatiya Nyaya Sanhita, 2023 (BNS) replaced the IPC for offences on/after 1 July 2024; the IPC equivalents requested by the assignment are shown for reference.", i=True)
T([["Law / Section", "Offence / provision", "Application in Case Omega"],
   ["IT Act 2000, s.43 r/w s.66", "Unauthorised access, introducing malware, damage, denial of access - dishonest/fraudulent: up to 3 years and/or fine up to Rs 5 lakh", "Access to SRV-EHR-01, ransomware deployment, deletion of backups"],
   ["IT Act s.66C / s.66D", "Identity theft (use of another's password); cheating by personation using computer resource", "Use of rsharma and svc_backup credentials; phishing as insurance portal"],
   ["IT Act s.66F / s.70", "Cyber terrorism / protected system (if hospital system notified as critical information infrastructure)", "Applicable only if notified; assess with authorities"],
   ["IT Act s.72, s.43A", "Breach of confidentiality; failure to protect sensitive personal data (compensation)", "Exfiltrated patient records; hospital's reasonable-security-practices duty"],
   ["IT Act s.65 / s.84B / s.84C", "Tampering with computer source documents; abetment; attempt", "Encryption/alteration of records; supporting offence"],
   ["IPC 384/386 [BNS 308]", "Extortion", "Ransom demand under threat of leaking data"],
   ["IPC 420 [BNS 318]", "Cheating / dishonestly inducing delivery", "Phishing email deceived employee"],
   ["IPC 379 [BNS 303]; IPC 425-426 [BNS 324]", "Theft (data/media); mischief", "Data theft; destruction of backups"],
   ["IPC 463/465/468 [BNS 336-338]", "Forgery / forgery for cheating", "Spoofed sender and fake claim document"],
   ["IPC 120B [BNS 61]", "Criminal conspiracy", "If multiple actors are identified"],
   ["DPDP Act 2023", "Security safeguards, breach notification to Board and data principals; penalties up to Rs 250 crore", "Health-data breach; hospital as data fiduciary (check commencement status of rules)"],
   ["CERT-In Directions, 28 Apr 2022 (s.70B(6))", "Report cyber incidents within 6 hours; retain logs 180 days", "Reported; logs preserved"]], [1.6, 2.5, 2.4])
P("Admissibility of electronic evidence", b=True)
for s in ["Bharatiya Sakshya Adhiniyam 2023, s.63 (formerly Indian Evidence Act s.65B): electronic records are admissible with a certificate identifying the device/process and signed by the person in charge and an expert, including hash values.",
          "BNSS 2023 (formerly CrPC): seizure/search powers (ss.94, 105-106, 185) and procedure for police investigation; IT Act s.80 allows search by a Deputy Superintendent of Police.",
          "IT Act s.79A: Examiner of Electronic Evidence; s.69B: monitoring and collection of traffic data by authorised agencies.",
          "Integrity is shown by the SHA-256 match, write-blocked acquisition, sealed original and unbroken chain of custody."]: B(s)

H("8. Recommendations for Cybersecurity Hardening")
T([["Priority", "Recommendation"],
   ["Immediate", "Rotate all credentials (domain-wide); disable svc_backup; block IOCs; rebuild SRV-EHR-01; restore from offline backups; notify affected patients/regulators as required"],
   ["Identity", "MFA on VPN/RDP/admin; remove RDP exposure; tiered admin model; LAPS; service accounts with least privilege and deny-interactive-logon"],
   ["Email", "Enforce SPF/DKIM/DMARC reject; block Office macros from the internet; attachment sandboxing; phishing training"],
   ["Endpoint", "EDR on all servers; Credential Guard / LSASS PPL; application allow-listing; block unmanaged USB (device control)"],
   ["Network", "Segment clinical, admin and backup networks; egress filtering and DLP/anomaly alerts on large uploads; DNS filtering"],
   ["Backup", "3-2-1-1-0 rule with immutable/offline copy; test restores; separate backup credentials"],
   ["Detection & response", "24x7 SOC alerting on vssadmin/wbadmin/comsvcs; automated host isolation; tested IR plan and tabletop exercises"],
   ["Governance", "Log retention >= 180 days centralised; ISO 27001 / NABH-aligned controls; DPDP compliance programme; cyber insurance review"]], [1.4, 5.1])

H("9. Appendices")
B("A: Chain of custody - 02_evidence_collection/chain_of_custody.md")
B("B: Hash validation - 02_evidence_collection/hash_validation.md")
B("C: IOCs and YARA rule - 03_malware_analysis/")
B("D: Raw logs and timeline CSV - 04_timeline/")
B("E: Tool summary and authorship declaration - docs/")
IMG("screenshots/02_timeline_correlation.png", 6.4, "Figure 5: Timeline script output with correlation deltas")
d.save(R/"05_report/Case_Omega_Forensic_Report.docx")
print("report saved")
