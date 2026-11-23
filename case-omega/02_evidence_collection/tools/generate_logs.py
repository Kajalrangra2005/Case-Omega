#!/usr/bin/env python3
"""Generate the SIMULATED (fictional) log set for Case Omega.
All hosts, users, IPs (RFC 5737 documentation ranges) and domains are fictional."""
import csv, pathlib, random
random.seed(7)
OUT = pathlib.Path(__file__).resolve().parent.parent / "04_timeline" / "logs"
OUT.mkdir(parents=True, exist_ok=True)
TZ = "+05:30"
def ts(h, m, s, day=10): return f"2026-11-{day:02d}T{h:02d}:{m:02d}:{s:02d}{TZ}"

# ---- mail gateway ----
(OUT/"mail_gateway.log").write_text("\n".join([
 f"{ts(1,52,10)} DELIVER from=billing-update@mediclaims-portal.example to=rsharma@cityhospital.example subj=\"Pending insurance claim #88213\" attach=claim_88213.docm spf=fail",
 f"{ts(1,52,44)} DELIVER from=billing-update@mediclaims-portal.example to=accounts@cityhospital.example subj=\"Pending insurance claim #88213\" attach=claim_88213.docm spf=fail",
]) + "\n")

# ---- browser history (WS-BILL-07, user rsharma) ----
with open(OUT/"browser_history.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["timestamp","host","user","url","title"])
    w.writerow([ts(2,9,40),"WS-BILL-07","rsharma","https://mail.cityhospital.example/inbox","Inbox"])
    w.writerow([ts(2,14,3),"WS-BILL-07","rsharma","https://mediclaims-portal.example/claims/88213","Claim 88213 viewer"])
    w.writerow([ts(2,14,31),"WS-BILL-07","rsharma","http://203.0.113.45/dl/upd_svc.exe","download"])

# ---- process / EDR (sysmon-style) ----
(OUT/"process_events.log").write_text("\n".join([
 f"{ts(2,14,20)} WS-BILL-07 rsharma PROC_CREATE parent=WINWORD.EXE child=powershell.exe cmd=\"powershell -nop -w hidden -enc <b64>\"",
 f"{ts(2,14,31)} WS-BILL-07 rsharma NET_CONNECT proc=powershell.exe dst=203.0.113.45:80 note=download upd_svc.exe",
 f"{ts(2,14,33)} WS-BILL-07 rsharma FILE_CREATE C:\\Users\\Public\\upd_svc.exe",
 f"{ts(2,41,5)}  WS-BILL-07 rsharma PROC_CREATE parent=upd_svc.exe child=rundll32.exe cmd=\"comsvcs.dll MiniDump lsass\" note=credential dumping",
 f"{ts(3,2,11)}  SRV-EHR-01 svc_backup FILE_CREATE C:\\Users\\Public\\upd_svc.exe note=copied over SMB admin share",
 f"{ts(3,3,20)}  SRV-EHR-01 svc_backup PROC_CREATE parent=cmd.exe child=upd_svc.exe cmd=\"upd_svc.exe --stage\"",
 f"{ts(3,31,45)} SRV-EHR-01 svc_backup PROC_CREATE parent=upd_svc.exe child=vssadmin.exe cmd=\"vssadmin delete shadows /all /quiet\"",
 f"{ts(3,32,10)} SRV-EHR-01 svc_backup PROC_CREATE parent=upd_svc.exe child=wbadmin.exe cmd=\"wbadmin delete catalog -quiet\"",
 f"{ts(3,33,2)}  SRV-EHR-01 svc_backup PROC_CREATE parent=upd_svc.exe child=schtasks.exe cmd=\"schtasks /create /tn WinUpdateSvc /tr C:\\Users\\Public\\upd_svc.exe /sc onlogon\"",
 f"{ts(3,33,9)}  SRV-EHR-01 svc_backup REG_SET HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\WinUpdateSvc=C:\\Users\\Public\\upd_svc.exe",
 f"{ts(3,35,0)}  SRV-EHR-01 svc_backup PROC_CREATE parent=upd_svc.exe child=upd_svc.exe cmd=\"upd_svc.exe --run\" note=encryption phase starts",
]) + "\n")

# ---- authentication (Windows 4624/4625/4648 style) ----
auth = [
 f"{ts(1,10,0)} DC-01 4625 FAILED logon user=rsharma src=WS-BILL-07 note=typo",
 f"{ts(2,9,12)} DC-01 4624 SUCCESS logon user=rsharma type=2 src=WS-BILL-07",
 f"{ts(2,44,30)} DC-01 4624 SUCCESS logon user=svc_backup type=3 src=WS-BILL-07 note=first use from a workstation",
]
for i in range(6):
    auth.append(f"{ts(2,52,10+i*4)} SRV-EHR-01 4625 FAILED logon user=administrator type=3 src=WS-BILL-07 note=password spray")
auth += [
 f"{ts(2,58,2)} SRV-EHR-01 4624 SUCCESS logon user=svc_backup type=10 src=WS-BILL-07 note=RDP",
 f"{ts(3,36,40)} SRV-EHR-01 4688 note=process audit on",
]
(OUT/"auth_events.log").write_text("\n".join(auth)+"\n")

# ---- USB (SetupAPI / Event 20001) ----
(OUT/"usb_events.log").write_text("\n".join([
 f"{ts(3,10,4)} SRV-EHR-01 USB_INSERT vid=0781 pid=5581 serial=4C530001230815112394 desc=\"SanDisk Ultra USB 3.0\" user=svc_backup",
 f"{ts(3,10,31)} SRV-EHR-01 FILE_COPY src=E:\\tools\\rclone.exe dst=C:\\Users\\Public\\rc.exe",
 f"{ts(3,19,50)} SRV-EHR-01 USB_REMOVE serial=4C530001230815112394",
]) + "\n")

# ---- firewall ----
fw = [
 f"{ts(2,14,31)} FW-EDGE ALLOW WS-BILL-07 10.20.5.17 -> 203.0.113.45:80 bytes=412311",
 f"{ts(2,46,0)}  FW-EDGE ALLOW WS-BILL-07 10.20.5.17 -> 198.51.100.77:443 bytes=1840 note=C2 beacon",
 f"{ts(2,58,1)}  FW-INT  ALLOW WS-BILL-07 10.20.5.17 -> 10.20.1.10:3389 bytes=90210 note=RDP to SRV-EHR-01",
]
bytes_total = 0
for minute in range(22, 31):
    b = random.randint(150, 260) * 1_000_000
    bytes_total += b
    fw.append(f"{ts(3,minute,0)} FW-EDGE ALLOW SRV-EHR-01 10.20.1.10 -> 198.51.100.77:443 bytes={b} note=sustained upload")
fw.append(f"{ts(3,30,45)} FW-EDGE SUMMARY SRV-EHR-01 -> 198.51.100.77:443 total_bytes={bytes_total}")
fw.append(f"{ts(4,3,0)}  FW-EDGE DENY  SRV-EHR-01 10.20.1.10 -> 198.51.100.77:443 note=blocked by IR team")
(OUT/"firewall.log").write_text("\n".join(fw)+"\n")

# ---- file audit (sampled) ----
fa = []
for i,name in enumerate(["patients_2026.mdf","radiology_idx.db","billing_q3.xlsx","lab_results.csv","discharge_summ.docx"]):
    fa.append(f"{ts(3,35,20+i*6)} SRV-EHR-01 FILE_RENAME D:\\EHR\\{name} -> D:\\EHR\\{name}.omega")
fa.append(f"{ts(3,36,5)} SRV-EHR-01 FILE_CREATE D:\\EHR\\README_OMEGA.txt note=ransom note (dropped in every directory)")
fa.append(f"{ts(3,47,30)} SRV-EHR-01 AUDIT summary: 48,213 files renamed to *.omega in 12m10s")
(OUT/"file_audit.log").write_text("\n".join(fa)+"\n")

# ---- EDR / SOC alerts ----
(OUT/"edr_alerts.log").write_text("\n".join([
 f"{ts(3,31,45)} EDR HIGH   SRV-EHR-01 shadow copy deletion",
 f"{ts(3,47,30)} EDR CRIT   SRV-EHR-01 mass file rename (ransomware heuristic)",
 f"{ts(3,52,0)}  SOC PAGE   on-call analyst paged",
 f"{ts(4,3,0)}   SOC ACTION firewall block 198.51.100.77; SRV-EHR-01 network cable unplugged (isolated, left powered ON)",
 f"{ts(4,12,0)}  IR  FIRST RESPONDER on scene (Server Room B)",
]) + "\n")
print("logs written to", OUT)
