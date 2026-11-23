#!/usr/bin/env python3
"""Parse all simulated logs, merge into one UTC-normalised timeline, flag key
phases, and draw a visualization. Usage: python3 build_timeline.py"""
import csv, re, pathlib
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).resolve().parent
LOGS = HERE / "logs"
TS = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2})\s+(.*)$")

PHASES = [  # (keyword, phase) - first match wins, most specific first
    ("shadows", "6 Defence evasion"), ("wbadmin", "6 Defence evasion"),
    ("schtasks", "7 Persistence"), ("REG_SET", "7 Persistence"),
    ("--run", "8 Impact"), (".omega", "8 Impact"), ("README_OMEGA", "8 Impact"),
    ("mass file rename", "8 Impact"),
    ("SOC", "9 Response"), ("FIRST RESPONDER", "9 Response"), ("blocked by IR", "9 Response"),
    ("claim_88213.docm", "1 Initial access"), ("WINWORD.EXE", "1 Initial access"),
    ("lsass", "3 Credential access"), ("password spray", "3 Credential access"),
    ("C2 beacon", "3 Credential access"), ("first use from a workstation", "3 Credential access"),
    ("RDP", "4 Lateral movement"),
    ("USB_", "5 Staging / exfil"), ("rclone", "5 Staging / exfil"),
    ("rc.exe", "5 Staging / exfil"), ("sustained upload", "5 Staging / exfil"),
    ("SUMMARY", "5 Staging / exfil"),
    ("upd_svc.exe", "2 Execution"), ("203.0.113.45", "2 Execution"),
]
def phase(text):
    for k, p in PHASES:
        if k in text: return p
    return "0 Context"

events = []
for f in sorted(LOGS.glob("*.log")):
    for line in f.read_text().splitlines():
        m = TS.match(line)
        if m:
            events.append((datetime.fromisoformat(m.group(1)), f.stem, m.group(2).strip()))
with open(LOGS / "browser_history.csv") as fh:
    for r in csv.DictReader(fh):
        events.append((datetime.fromisoformat(r["timestamp"]), "browser_history",
                       f'{r["host"]} {r["user"]} visited {r["url"]}'))
events.sort(key=lambda e: e[0])

with open(HERE / "timeline.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["timestamp_IST", "timestamp_UTC", "source", "phase", "event"])
    for t, src, txt in events:
        w.writerow([t.isoformat(), t.astimezone(__import__("datetime").timezone.utc).isoformat(),
                    src, phase(txt), txt])

# ---- correlation checks (printed + saved) ----
def first(sub):
    return next((t for t, _, x in events if sub in x), None)
checks = {
  "Phish delivered -> macro runs": (first("claim_88213.docm"), first("WINWORD.EXE")),
  "PowerShell -> payload download": (first("WINWORD.EXE"), first("download upd_svc.exe")),
  "Credential dump -> svc_backup first use": (first("lsass"), first("first use from a workstation")),
  "svc_backup RDP -> USB insert": (first("type=10"), first("USB_INSERT")),
  "USB insert -> bulk upload starts": (first("USB_INSERT"), first("sustained upload")),
  "Upload ends -> shadow copy deletion": (first("SUMMARY"), first("vssadmin delete")),
  "Encryption start -> EDR critical alert": (first("--run"), first("mass file rename (ransomware")),
  "EDR critical -> containment": (first("mass file rename (ransomware"), first("blocked by IR")),
}
lines = ["CORRELATION CHECKS (time deltas)"]
for k, (a, b) in checks.items():
    lines.append(f"- {k}: {b - a}")
t0, t1 = first("WINWORD.EXE"), first("blocked by IR")
lines.append(f"- TOTAL dwell time (first execution -> containment): {t1 - t0}")
(HERE / "correlation_findings.txt").write_text("\n".join(lines) + "\n")
print("\n".join(lines))

# ---- visualization ----
order = sorted({phase(x) for _, _, x in events})
colors = plt.cm.tab10.colors
fig, ax = plt.subplots(figsize=(13, 6.5))
for t, src, txt in events:
    p = phase(txt)
    ax.scatter(t, order.index(p), s=60, color=colors[order.index(p) % 10], zorder=3)
for i, p in enumerate(order):
    ev = [t for t, _, x in events if phase(x) == p]
    ax.hlines(i, min(ev), max(ev), color=colors[i % 10], alpha=.35, lw=6, zorder=2)
labels = {"USB_INSERT": ("USB inserted 03:10", (-95, 12)), "sustained upload": ("~1.8 GB exfil 03:22-03:30", (8, -16)),
          ".omega": ("Encryption 03:35-03:47", (8, 10)), "blocked by IR": ("Contained 04:03", (-90, 10)),
          "WINWORD.EXE": ("Macro runs 02:14", (8, 10)), "vssadmin delete": ("Shadow copies wiped 03:31", (-150, 10)),
          "schtasks": ("Persistence 03:33", (-110, 10))}
for t, _, x in events:
    for k, (lab, off) in list(labels.items()):
        if k in x:
            ax.annotate(lab, (t, order.index(phase(x))), textcoords="offset points",
                        xytext=off, fontsize=8)
            labels.pop(k); break
ax.set_yticks(range(len(order))); ax.set_yticklabels(order)
ax.invert_yaxis(); ax.grid(axis="x", alpha=.3)
ax.set_title("Case Omega - Attack timeline, 10 Nov 2026 (IST) - SIMULATED DATA")
ax.set_xlabel("Time (IST)")
fig.autofmt_xdate(); fig.tight_layout()
fig.savefig(HERE / "timeline.png", dpi=130)
print("wrote timeline.csv, correlation_findings.txt, timeline.png")
