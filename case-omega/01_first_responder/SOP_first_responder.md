# First Responder SOP - Ransomware / Suspected Digital Evidence Scene

**Case:** Omega | **Applies to:** IR team, hospital IT, security officers | **Standards followed:** ACPO Good Practice Guide for Digital Evidence (principles 1-4), ISO/IEC 27037:2012, NIST SP 800-86 / 800-61r2, CERT-In directions (28 Apr 2022)

## Four guiding principles
1. Do not change data that may later be relied on in court.
2. If original data must be accessed, the person must be competent and able to explain their actions.
3. Keep an audit trail of every action; a third party must be able to repeat the process and reach the same result.
4. The incident lead is responsible for ensuring the law and these principles are followed.

## Procedure

| # | Phase | Action | Record |
|---|-------|--------|--------|
| 1 | Prepare | Put on gloves; take the IR kit (write-blockers, evidence bags, tags, labels, camera, notebook, anti-static bags, Faraday bag, USB-C/SATA adapters, trusted USB with tools). | Kit checklist |
| 2 | Secure | Restrict access to Server Room B; log everyone entering/leaving; stop all non-IR staff touching systems. | Access log |
| 3 | Notify | Inform the incident commander, CISO, legal counsel and hospital management. Prepare CERT-In report (within 6 hours of noticing) and, where required, police complaint. | Notification log |
| 4 | Assess volatility | Identify what is **powered on** and what holds volatile data (RAM, network connections, running processes, logged-in sessions). | Volatility sheet |
| 5 | **Do NOT** | Do **not** power off, reboot, log in, run AV clean-up, delete the ransom note, or pay/contact the attacker. Powering off destroys RAM (encryption keys may be in memory). | - |
| 6 | Contain | Isolate by **unplugging network cable / disabling switch port** (not powering off). Block attacker IP/domain at firewall. Disable compromised accounts (`svc_backup`, `rsharma`). | Containment log |
| 7 | Photograph | Photograph the scene wide -> mid -> close-up: room, screens (with time), cabling, rear panels, USB ports, serial labels. Use a scale/ruler and a clock in frame. | Photo log (P1..Pn) |
| 8 | Sketch | Draw/annotate a scene sketch with every device assigned an ID (E1, E2...). See `scene_sketch.png`. | Sketch |
| 9 | Live data capture (if authorised) | In this order of volatility: RAM image -> network connections -> process list -> logged-in users -> scheduled tasks -> clipboard. Use trusted tools from external media; write output to evidence media; hash it. | Live-response log |
| 10 | Collect | Tag each item (see `evidence_tag_template.md`), place in anti-static/Faraday bag, seal and sign over the seal. Disks: forensic image via write-blocker. | Evidence tags |
| 11 | Chain of custody | Open a Chain-of-Custody form for each item at the moment of seizure. | `02_evidence_collection/chain_of_custody.md` |
| 12 | Transport & store | Transport in a sealed container; store in locked evidence room with access log; no unsupervised access. | Transfer entries |
| 13 | Hand-over | Provide a first-responder statement and all logs to the forensic lab. | Statement |

## Digital evidence types to identify at this scene

| ID | Evidence | Location | Volatility | Handling |
|----|----------|----------|-----------|----------|
| E1 | Compromised server SRV-EHR-01 (disk, RAM) | Server Room B | RAM = high; disk = low | Live RAM capture then dd/FTK image |
| E2 | SRV-DB-02 (unaffected DB server) | Server Room B | Low | Image for comparison/baseline |
| E3 | Network logs (firewall, switch, DNS) | FW-EDGE, SW-CORE-1 | Medium (rolling) | Export immediately; hash |
| E4 | USB drive (SanDisk, serial 4C530001230815112394) | On E1 | Low | Bag + tag; write-blocked imaging |
| E5 | Backup NAS | Server Room B | Low | Image; check shadow copies/snapshots |
| E6 | Patient workstation WS-BILL-07 (phish victim) | Billing, 2nd floor | RAM high | Same as E1 |
| E7 | Cloud / mail gateway / identity (DC-01) logs, VPN logs | Cloud + DC | Medium | Export with admin; hash; document who exported |
| E8 | Ransom note `README_OMEGA.txt` and encrypted samples | D:\EHR\ | Low | Copy via image only |
| E9 | Mobile devices of affected users | Users | Medium | Faraday bag, airplane mode |
