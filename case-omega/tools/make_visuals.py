#!/usr/bin/env python3
"""Render (a) terminal-style 'screenshots' from REAL command output files and
(b) the scene sketch map. Output: screenshots/*.png, 01_first_responder/scene_sketch.png"""
import pathlib, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
R = pathlib.Path(__file__).resolve().parent.parent

def terminal(text, out, title):
    lines = text.rstrip().splitlines()
    h = max(2.2, 0.28 * len(lines) + 0.9)
    fig = plt.figure(figsize=(12, h), facecolor="#1e1e1e")
    fig.text(0.01, 1 - 0.35 / h, f"● ● ●   {title}", color="#aaa", fontsize=9, family="monospace", va="top")
    for i, l in enumerate(lines):
        c = "#7ee787" if l.startswith("$") else ("#ffa657" if ("OK" in l or "MATCH" in l) else "#d4d4d4")
        fig.text(0.01, 1 - (0.8 + 0.28 * i) / h, l[:150], color=c, fontsize=8.3, family="monospace", va="top")
    fig.savefig(out, dpi=120, facecolor=fig.get_facecolor()); plt.close(fig)

terminal((R/"02_evidence_collection/acquisition_log.txt").read_text(),
         R/"screenshots/01_dd_acquisition_and_sha256.png", "analyst@forensic-ws: dd imaging + SHA-256 verification")
terminal((R/"04_timeline/correlation_findings.txt").read_text() +
         "\n$ head -6 04_timeline/timeline.csv | cut -c1-140\n" +
         "\n".join(l[:140] for l in (R/"04_timeline/timeline.csv").read_text().splitlines()[:6]),
         R/"screenshots/02_timeline_correlation.png", "analyst@forensic-ws: python3 build_timeline.py")

import subprocess
out = subprocess.run("strings -t x 02_evidence_collection/image/SRV-EHR-01.dd | grep -iE 'omega|WinUpdate|vssadmin|upd_svc'",
                     shell=True, cwd=R, capture_output=True, text=True).stdout
terminal("$ strings -t x SRV-EHR-01.dd | grep -iE 'omega|WinUpdate|vssadmin|upd_svc'\n" + out,
         R/"screenshots/03_strings_artifacts_in_image.png", "analyst@forensic-ws: artifact search in disk image")
# ---------- scene sketch ----------
fig, ax = plt.subplots(figsize=(11, 7)); ax.set_xlim(0, 22); ax.set_ylim(0, 14); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(Rectangle((0.5, 0.5), 21, 13, fill=False, lw=2.5))
ax.text(11, 13.9, "SCENE SKETCH - Server Room B, City Hospital (FICTIONAL) - not to scale", ha="center", fontsize=12, weight="bold")
ax.add_patch(Rectangle((9.5, 0.1), 3, 0.8, color="#bbb")); ax.text(11, 0.45, "DOOR (card access, logged)", ha="center", fontsize=8)
def box(x, y, w, h, label, c="#cfe3ff"):
    ax.add_patch(Rectangle((x, y), w, h, fc=c, ec="k")); ax.text(x + w/2, y + h/2, label, ha="center", va="center", fontsize=8)
for i in range(4): box(2 + i*1.6, 10, 1.4, 3, f"Rack {chr(65+i)}", "#e8e8e8")
box(10, 9.5, 3.2, 3.2, "E1  SRV-EHR-01\n(powered ON,\nnetwork unplugged)", "#ffd6d6")
box(14.5, 9.5, 2.6, 3.2, "E2  SRV-DB-02\n(not encrypted)", "#e8f5e9")
box(18.2, 9.5, 2.6, 3.2, "Core switch\nSW-CORE-1", "#fff3cd")
box(2, 4.5, 4.5, 2.5, "Analyst bench\n(forensic WS + write-blocker)", "#e0f7fa")
box(8, 4, 3.5, 2.2, "E3  Evidence table\ntags + bags", "#fff9c4")
box(13.5, 4, 3.5, 2.2, "E4  USB drive\nSanDisk 4C53..2394\n(found on E1 chassis,\nremoved 03:19)", "#ffd6d6")
box(18, 4, 3, 2.2, "E5  Backup NAS\n(shadow copies gone)", "#ffe0b2")
ax.text(1, 2.2, "E6  WS-BILL-07 (Billing, 2nd floor) - seized separately", fontsize=8)
ax.text(1, 1.6, "E7  Cloud/Network: firewall + DC-01 + mail-gateway logs (exported by admin, hashed)", fontsize=8)
ax.add_patch(FancyArrowPatch((11, 0.9), (11.3, 4), arrowstyle="->", mutation_scale=15))
ax.add_patch(FancyArrowPatch((11.6, 6.3), (11.6, 9.4), arrowstyle="->", mutation_scale=15))
ax.text(1, 8.0, "Photographer positions: P1 (door), P2 (front of E1), P3 (rear cabling of E1)", fontsize=8)
for (x, y, l) in [(10, 1.8, "P1"), (11.5, 8.3, "P2"), (11.5, 13.3, "P3")]:
    ax.scatter(x, y, marker="^", color="red", s=70); ax.text(x + .25, y, l, color="red", fontsize=9)
ax.text(17, 2.2, "N", fontsize=12, weight="bold"); ax.annotate("", (17.3, 3), (17.3, 2.3), arrowprops=dict(arrowstyle="->"))
fig.savefig(R/"01_first_responder/scene_sketch.png", dpi=130, bbox_inches="tight")
print("visuals done")
