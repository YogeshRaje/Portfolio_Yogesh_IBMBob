"""
set_slide_timings.py
====================
Sets slide auto-advance timings in Yogesh_Raje_Portfolio_Presentation.pptx
so that PowerPoint exports a ~150-second video using:
  File → Export → Create a Video → Use Recorded Timings and Narrations

Total: 17 slides  ×  custom durations  =  150 seconds exactly

Run:  python set_slide_timings.py
"""

from pptx import Presentation
from pptx.util import Pt
from lxml import etree
import copy, os

INPUT  = "Yogesh_Raje_Portfolio_Presentation.pptx"
OUTPUT = "Yogesh_Raje_Portfolio_Video_Ready.pptx"

# ── Slide durations in seconds (must sum to exactly 150) ──────────────────
#  Slide 1  – Title               10s  (opening impression)
#  Slide 2  – Agenda               6s  (quick overview)
#  Slide 3  – Project Overview     8s
#  Slide 4  – About Yogesh Raje    9s
#  Slide 5  – SDLC Methodology     9s
#  Slide 6  – Phase 1 Req          9s
#  Slide 7  – Phase 2 PAAR Loop   10s  (core AI design)
#  Slide 8  – Phase 3 Architecture  9s
#  Slide 9  – Phase 4 Development   9s
#  Slide 10 – Phase 5 Granite AI   10s  (key integration)
#  Slide 11 – Phase 6 Testing       8s
#  Slide 12 – Portfolio Screenshot  10s (visual demo)
#  Slide 13 – AI Chat Demo          10s (visual demo)
#  Slide 14 – Tech Stack            9s
#  Slide 15 – Deployment            9s
#  Slide 16 – Metrics & Cert        8s
#  Slide 17 – Closing               7s
# ─────────────────────────────────────────────────────────────────────────
DURATIONS = [10, 6, 8, 9, 9, 9, 10, 9, 9, 10, 8, 10, 10, 9, 9, 8, 7]

assert len(DURATIONS) == 17,  f"Expected 17 durations, got {len(DURATIONS)}"
assert sum(DURATIONS) == 150, f"Durations sum to {sum(DURATIONS)}, expected 150"

print(f"Total duration: {sum(DURATIONS)}s  across {len(DURATIONS)} slides")

# ── Open presentation ─────────────────────────────────────────────────────
prs = Presentation(INPUT)
assert len(prs.slides) == 17, f"Expected 17 slides, got {len(prs.slides)}"

# ── EMU / timing constants ────────────────────────────────────────────────
# PowerPoint stores slide timing in milliseconds in the XML spTree / timing
# The relevant element is <p:transition> with advTm (advance time in ms)
# and <p:sld> show="1" and advance attributes

NSMAP_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NSMAP_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

def set_slide_advance(slide, duration_sec):
    """
    Set the slide auto-advance time and enable auto-advance.
    duration_sec: seconds before auto-advance to next slide.
    """
    duration_ms = duration_sec * 1000  # convert to milliseconds

    spTree = slide.shapes._spTree   # root sp tree element (<p:spTree>)
    slide_elem = spTree.getparent() # <p:cSld> → parent is <p:sld>

    # Find or create <p:transition> as a child of <p:sld>
    sld_elem = slide_elem.getparent()  # walk up to <p:sld>

    # The slide XML root is the <p:sld> element
    sld_root = slide._element  # lxml element for <p:sld>

    # Find existing <p:transition> or create one
    ns = f"{{{NSMAP_P}}}"
    trans_tag = f"{ns}transition"

    trans = sld_root.find(trans_tag)
    if trans is None:
        trans = etree.SubElement(sld_root, trans_tag)

    # Set advance-on-time attributes
    trans.set("advTm",    str(duration_ms))   # auto-advance time in ms
    trans.set("advClick", "0")                # do NOT advance on mouse click
    # Note: advClick="0" means only timer advances it — good for video export

    # Also set spd (speed) for smooth feel
    trans.set("spd", "fast")

    return duration_ms


# ── Apply timings ─────────────────────────────────────────────────────────
for idx, (slide, dur) in enumerate(zip(prs.slides, DURATIONS), start=1):
    ms = set_slide_advance(slide, dur)
    print(f"  Slide {idx:02d}: {dur:2d}s  ({ms} ms)")

# ── Also set presentation-level "use timings" flag ───────────────────────
# This ensures File→Export→Video defaults to "Use Recorded Timings"
prs_xml = prs.element   # <p:presentation> lxml element directly
ns_p = f"{{{NSMAP_P}}}"

# Find or create <p:showPr>
show_pr = prs_xml.find(f"{ns_p}showPr")
if show_pr is None:
    show_pr = etree.SubElement(prs_xml, f"{ns_p}showPr")
show_pr.set("useTimings", "1")
show_pr.set("loop",       "0")

# ── Save ─────────────────────────────────────────────────────────────────
prs.save(OUTPUT)
print(f"\n[OK] Saved: {OUTPUT}")
print(f"     Slides: {len(prs.slides)}")
print(f"     Total duration: {sum(DURATIONS)}s")
print()
print("=" * 60)
print("  HOW TO EXPORT AS VIDEO IN POWERPOINT:")
print("=" * 60)
print()
print("  1. Open:  Yogesh_Raje_Portfolio_Video_Ready.pptx")
print("  2. Click: File > Export > Create a Video")
print("  3. Quality: Full HD (1080p)")
print("  4. Select: 'Use Recorded Timings and Narrations'")
print("  5. Click:  Create Video")
print("  6. Save as: Yogesh_Raje_Portfolio_Video.mp4")
print()
print("  Result: ~150-second video (2 min 30 sec)")
print("=" * 60)
