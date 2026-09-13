"""
voiceover_script.py
===================
Step 1 of 2 — Generates voiceover audio for each slide using
Microsoft Edge TTS (neural voice — no API key required).

Slide timings (must match Yogesh_Raje_Portfolio_Video_Ready.pptx):
  Slide 01: 10s  Slide 02:  6s  Slide 03:  8s  Slide 04:  9s
  Slide 05:  9s  Slide 06:  9s  Slide 07: 10s  Slide 08:  9s
  Slide 09:  9s  Slide 10: 10s  Slide 11:  8s  Slide 12: 10s
  Slide 13: 10s  Slide 14:  9s  Slide 15:  9s  Slide 16:  8s
  Slide 17:  7s  TOTAL: 150s

Voice: Microsoft Aria (en-US, Neural) — clear, professional
Run:   python voiceover_script.py
"""

import asyncio, os, sys
import edge_tts

# ── Voice selection ────────────────────────────────────────────────────────
# en-US-AriaNeural  — clear professional female voice
# en-US-GuyNeural   — professional male voice
VOICE = "en-US-AriaNeural"
RATE  = "+5%"   # slightly faster for 150s pacing
OUT_DIR = "voiceover_segments"
os.makedirs(OUT_DIR, exist_ok=True)

# ── Voiceover script per slide ─────────────────────────────────────────────
# Each script is carefully paced to fit within its slide duration.
# Approx 2.5–3 words per second at normal TTS speed.
SCRIPTS = {
    1: """Welcome to the Yogesh Raje Personal Portfolio — an AI-powered web application
built using IBM Granite and the complete Agentic AI Software Development Lifecycle.""",

    2: """Today we will cover the project overview, Yogesh Raje's trainer profile,
all seven phases of the Agentic AI SDLC, the live portfolio, AI chat demo,
technology stack, and deployment.""",

    3: """This is a full-stack portfolio web application for Yogesh Raje — a world-class
technical trainer. It features an IBM Granite AI assistant, zero npm dependencies,
and was deployed to GitHub using Node dot j s.""",

    4: """Yogesh Raje is a Technical Trainer and Subject Matter Expert specialising in
Agentic AI, Machine Learning, and Quantum Computing. He has trained over 500 professionals,
delivered 50 workshops, and maintains a 98 percent satisfaction rate.""",

    5: """The project follows the Agentic AI SDLC — seven phases from requirements through
deployment. Unlike traditional SDLC, it adds agent capability definition, PAAR loop design,
and treats the system prompt as code.""",

    6: """Phase One is Requirements Analysis. We identified five stakeholders, defined
sixteen functional requirements covering eight portfolio sections and eight AI assistant features,
plus nine non-functional requirements around performance, security, and compatibility.""",

    7: """Phase Two is the Agentic AI System Design using the PAAR Loop —
Perceive the user message, Assess the intent, Act by calling IBM Granite,
and Reflect using persona constraints in the system prompt.""",

    8: """Phase Three covers the three-tier system architecture — the browser client,
the Node dot j s server with the Granite endpoint, and IBM Cloud hosting the
watsonx dot a i model. The UI uses a dark navy theme with cyan and indigo accents.""",

    9: """Phase Four is Development across five sprints — building the static portfolio,
adding domain content and testimonials, the contact section, the AI chat widget,
and finally the Node dot j s server with IBM Granite integration.""",

    10: """Phase Five is IBM Granite AI Integration. The five-step flow: user types a message,
browser posts to the API, server fetches an IBM I A M token, calls the Granite model,
and returns the reply. The API key is stored server-side only — never in the browser.""",

    11: """Phase Six is Testing and Validation. All twelve test cases passed —
six portfolio UI tests and six AI assistant tests. All eight acceptance criteria were met,
including zero API key exposure and full fallback mode functionality.""",

    12: """Here is the live portfolio running at localhost 3000. The hero section shows
Yogesh Raje's name in an animated gradient, with three call-to-action buttons.
The about section features orbital ring animations and four key statistics.""",

    13: """The IBM Granite AI chat widget floats in the bottom-right corner.
Visitors can ask questions about training programs, Agentic AI, Machine Learning,
and Quantum Computing. The assistant uses multi-turn memory and Markdown rendering.""",

    14: """The technology stack uses Node dot j s version 22, all built-in modules,
IBM Granite 3.3 eight billion instruct via watsonx dot a i, and IBM I A M OAuth.
Zero external npm packages are required — the server runs with no install step.""",

    15: """Phase Seven is Deployment. The server starts with node server dot j s and displays
a confirmation banner showing the model, region, and API status. The project was
deployed to GitHub and verified with HTTP 200 across all eight content checks.""",

    16: """All success metrics were achieved — eight of eight portfolio sections,
twelve of twelve test cases passed, and all eight risks mitigated including
API key security, token refresh, and fallback mode coverage.""",

    17: """Thank you. The Yogesh Raje Personal Portfolio is live at localhost 3000
and deployed at github dot com slash YogeshRaje slash Portfolio underscore Yogesh underscore IBM Bob.
Powered by IBM Granite via watsonx dot a i. Built with IBM Bob.""",
}

assert len(SCRIPTS) == 17, f"Expected 17 scripts, got {len(SCRIPTS)}"

# ── Generate audio per slide ───────────────────────────────────────────────
async def generate_segment(slide_num: int, text: str) -> str:
    out_path = os.path.join(OUT_DIR, f"slide_{slide_num:02d}.mp3")
    communicate = edge_tts.Communicate(text.strip(), VOICE, rate=RATE)
    await communicate.save(out_path)
    size = os.path.getsize(out_path)
    print(f"  Slide {slide_num:02d}: saved {out_path}  ({size:,} bytes)")
    return out_path

async def main():
    print(f"Generating {len(SCRIPTS)} voiceover segments...")
    print(f"Voice: {VOICE}  Rate: {RATE}")
    print(f"Output dir: {OUT_DIR}/")
    print("-" * 50)
    tasks = [generate_segment(n, t) for n, t in sorted(SCRIPTS.items())]
    paths = await asyncio.gather(*tasks)
    print("-" * 50)
    print(f"[OK] Generated {len(paths)} audio segments in '{OUT_DIR}/'")
    print()
    print("Next step: run  python add_voiceover.py")

if __name__ == "__main__":
    asyncio.run(main())
