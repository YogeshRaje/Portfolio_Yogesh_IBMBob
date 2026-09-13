# 🧠 Yogesh — Personal Portfolio Website

> **Technical Trainer · Agentic AI · Machine Learning · Quantum Computing**  
> Powered by **IBM Granite** (`ibm/granite-3-3-8b-instruct`) via **IBM watsonx.ai**

![Node.js](https://img.shields.io/badge/Node.js-18%2B-green?logo=node.js)
![IBM Granite](https://img.shields.io/badge/IBM%20Granite-3.3--8B-blue?logo=ibm)
![watsonx.ai](https://img.shields.io/badge/IBM-watsonx.ai-0062FF?logo=ibm)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![SDLC](https://img.shields.io/badge/SDLC-Agentic%20AI-purple)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Live Demo](#live-demo)
- [Features](#features)
- [Agentic AI Architecture](#agentic-ai-architecture)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [IBM Granite Setup](#ibm-granite-setup)
- [Technology Stack](#technology-stack)
- [SDLC Phases](#sdlc-phases)
- [Screenshots](#screenshots)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

A **full-stack personal portfolio web application** for Yogesh — an expert Technical Trainer specialising in:

| Domain | Topics |
|--------|--------|
| 🤖 **Agentic AI** | LLM Agents, IBM Granite, LangChain, AutoGen, RAG, CrewAI, ReAct |
| 📊 **Machine Learning** | Deep Learning, NLP, MLOps, TensorFlow, PyTorch, Scikit-learn |
| ⚛️ **Quantum Computing** | Qiskit, PennyLane, VQE, QAOA, Quantum ML, Shor's & Grover's |

The application includes a **floating IBM Granite–powered AI assistant** that uses an **Agentic PAAR loop** (Perceive → Assess → Act → Reflect) to answer visitors' queries about training programs, expertise, booking, and technical topics in real time.

> Built following all phases of the **Agentic AI SDLC** — see [`SDLC_PLAN.md`](SDLC_PLAN.md) for the full plan.

---

## Live Demo

```
http://localhost:3000
```

Run locally with one command:

```bash
node server.js
```

Or double-click **`install_and_run.bat`** on Windows.

---

## Features

### 🌐 Portfolio Sections
- **Hero** — Animated gradient, role highlights, IBM Granite AI CTA
- **About** — Biography, triple animated orbital rings, stats (500+ trained, 98% satisfaction)
- **Expertise** — 3 domain cards with technology tag pills
- **Skills** — 16 animated proficiency bars across 4 groups
- **Training Programs** — 6 structured programs with level badges
- **Testimonials** — Participant reviews from Infosys, IIT Bombay, TCS
- **Contact** — Enquiry form + full contact details
- **Footer** — IBM Granite powered badge

### 🤖 IBM Granite AI Chat Widget
- **Floating chat button** — accessible from every section
- **IBM Granite model** — `ibm/granite-3-3-8b-instruct` via watsonx.ai
- **Yogesh persona** — system prompt injects full trainer profile
- **Agentic PAAR loop** — Perceive intent → Assess → Act (Granite) → Reflect
- **IAM token caching** — auto-refreshes every ~56 minutes
- **Multi-turn memory** — retains last 12 messages per session
- **Suggested prompts** — quick-start questions for new visitors
- **Intelligent fallback** — 6 topic-matched offline responses when API not configured
- **Markdown rendering** — `**bold**`, bullet lists formatted in chat bubbles

### 🔒 Security
- API key stored **server-side only** — never sent to the browser
- IBM IAM token exchange handled in `server.js`

---

## Agentic AI Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  AGENTIC PAAR LOOP                               │
│                                                                  │
│   PERCEIVE          ASSESS           ACT            REFLECT      │
│   ─────────         ──────           ───            ───────      │
│   Parse user    →   Classify    →   Call IBM    →   Evaluate     │
│   message           intent          Granite         quality      │
│                     (FAQ /          completion      & persona    │
│   Extract           Program /       OR return       alignment    │
│   entities          Booking /       fallback                     │
│                     Technical)      response                     │
└─────────────────────────────────────────────────────────────────┘
         │                                        │
         ▼                                        ▼
   Client (browser)                       IBM watsonx.ai
   POST /api/chat                   ibm/granite-3-3-8b-instruct
```

**Flow:**

1. User types a message in the chat widget
2. Browser sends `POST /api/chat` with conversation history
3. `server.js` exchanges IBM API key → IAM Bearer token (cached)
4. Granite receives: system prompt (Yogesh persona) + message history
5. Response returned as JSON `{ reply, model }`
6. Browser renders the reply with Markdown formatting
7. History trimmed to last 12 turns for token efficiency

---

## Project Structure

```
Portfolio_Yogesh_IBMBob/
│
├── index.html            # Complete SPA — portfolio + AI chat widget
│                         # (HTML5 + CSS3 + Vanilla JS, fully self-contained)
│
├── server.js             # Node.js HTTP server
│                         # ├── Static file serving
│                         # ├── POST /api/chat — IBM Granite endpoint
│                         # ├── IAM token auth + caching
│                         # └── Fallback mode when API not configured
│
├── package.json          # Project metadata & npm scripts
│
├── install_and_run.bat   # Windows one-click launcher
│                         # ├── Node.js version check
│                         # ├── File integrity verification
│                         # ├── IBM Granite config display
│                         # └── Server start + browser open
│
├── SDLC_PLAN.md          # Full Agentic AI SDLC documentation
│                         # (13 sections: Requirements → Deployment)
│
├── README.md             # This file
├── .gitignore            # Git ignore rules
└── requirements.txt      # Dependency manifest
```

---

## Quick Start

### Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Node.js | ≥ 18.x | [nodejs.org](https://nodejs.org) |
| npm | ≥ 8.x | Bundled with Node.js |
| Git | any | [git-scm.com](https://git-scm.com) |

### 1 — Clone the repository

```bash
git clone https://github.com/YogeshRaje/Portfolio_Yogesh_IBMBob.git
cd Portfolio_Yogesh_IBMBob
```

### 2 — Run (no install needed — zero npm dependencies)

```bash
node server.js
```

Open **http://localhost:3000** in your browser.

### 3 — Windows shortcut

Double-click **`install_and_run.bat`** — it checks Node.js, verifies files, shows IBM Granite setup instructions, starts the server, and opens the browser automatically.

---

## IBM Granite Setup

The AI assistant runs in **intelligent fallback mode** by default (no API key required).  
To enable **full IBM Granite AI** responses, configure your IBM Cloud credentials:

### Option A — Environment Variables (Recommended)

**Windows CMD:**
```cmd
set IBM_API_KEY=your_ibm_cloud_api_key
set IBM_PROJECT_ID=your_watsonx_project_id
node server.js
```

**Windows PowerShell:**
```powershell
$env:IBM_API_KEY    = "your_ibm_cloud_api_key"
$env:IBM_PROJECT_ID = "your_watsonx_project_id"
node server.js
```

**Linux / macOS:**
```bash
export IBM_API_KEY="your_ibm_cloud_api_key"
export IBM_PROJECT_ID="your_watsonx_project_id"
node server.js
```

### Option B — Edit `server.js` directly

Open [`server.js`](server.js) and set lines 23–24:

```javascript
const IBM_API_KEY    = process.env.IBM_API_KEY    || 'YOUR_API_KEY_HERE';
const IBM_PROJECT_ID = process.env.IBM_PROJECT_ID || 'YOUR_PROJECT_ID_HERE';
```

### Getting Your IBM Credentials

| Step | Action |
|------|--------|
| 1 | Create a free account at [cloud.ibm.com](https://cloud.ibm.com) |
| 2 | Create a **watsonx.ai** service instance |
| 3 | Create a new **project** in [dataplatform.cloud.ibm.com](https://dataplatform.cloud.ibm.com) |
| 4 | Copy the **Project ID** from project settings |
| 5 | Go to **Manage → Access → API Keys** → Create API Key |
| 6 | Set both as environment variables (Option A above) |

---

## Technology Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Runtime | **Node.js ≥ 18** | Zero npm dependencies — built-ins only |
| HTTP Server | `node:http` | Static files + REST API |
| HTTPS Client | `node:https` | IBM watsonx.ai calls |
| Frontend | **HTML5 + CSS3 + Vanilla JS** | Single file, no framework |
| AI Model | **IBM Granite 3.3 8B Instruct** | `ibm/granite-3-3-8b-instruct` |
| AI Platform | **IBM watsonx.ai** | Text Chat REST API v2023-05-29 |
| Auth | IBM IAM OAuth 2.0 | Bearer token with server-side caching |
| Installer | Windows Batch Script | 5-step verification + launch |

---

## SDLC Phases

This project was built following the **Agentic AI SDLC** documented in [`SDLC_PLAN.md`](SDLC_PLAN.md):

| Phase | Description | Status |
|-------|-------------|--------|
| 1 — Requirements Analysis | Stakeholders, functional & non-functional requirements | ✅ |
| 2 — Agentic AI System Design | PAAR loop, tools, system prompt, context management | ✅ |
| 3 — Architecture & UI/UX | System architecture diagram, design principles | ✅ |
| 4 — Development | Sprint plan, implementation decisions | ✅ |
| 5 — AI Integration | IBM Granite API config, environment variables | ✅ |
| 6 — Testing & Validation | 12 test cases (UI + AI), acceptance criteria | ✅ |
| 7 — Deployment & Operations | Local, cloud (Code Engine, Vercel, Railway, Docker) | ✅ |

---

## Deployment

### Local (Default)
```bash
node server.js
# → http://localhost:3000
```

### IBM Code Engine
```bash
ibmcloud ce application create \
  --name yogesh-portfolio \
  --image icr.io/your-ns/yogesh-portfolio \
  --env IBM_API_KEY=xxx \
  --env IBM_PROJECT_ID=xxx
```

### Vercel
```bash
vercel --prod
# Set IBM_API_KEY and IBM_PROJECT_ID in the Vercel dashboard
```

### Railway / Render
Push this repo and set the two environment variables in the dashboard.

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```
```bash
docker build -t yogesh-portfolio .
docker run -p 3000:3000 \
  -e IBM_API_KEY=xxx \
  -e IBM_PROJECT_ID=xxx \
  yogesh-portfolio
```

---

## Screenshots

| Section | Description |
|---------|-------------|
| Hero | Animated gradient name, role badges, 3 CTA buttons |
| About | Triple orbital rings, bio, 4 stat cards |
| Expertise | Domain cards with hover lift and gradient top border |
| Skills | Animated proficiency bars (CSS transition) |
| Programs | 6 program cards with colour-coded level badges |
| AI Chat | IBM Granite floating widget with typing indicator |

---

## Contributing

Pull requests welcome. For major changes, please open an issue first.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Author

**Yogesh** — Technical Trainer  
🤖 Agentic AI &nbsp;·&nbsp; 📊 Machine Learning &nbsp;·&nbsp; ⚛️ Quantum Computing

- 📧 yogesh@aigenius.in
- 📍 Pune, Maharashtra, India
- 🔗 [linkedin.com/in/yogesh-ai-trainer](https://linkedin.com/in/yogesh-ai-trainer)
- 🌐 [Portfolio](https://github.com/YogeshRaje/Portfolio_Yogesh_IBMBob)

---

<div align="center">
  <sub>AI Assistant powered by <strong>IBM Granite</strong> · <code>ibm/granite-3-3-8b-instruct</code> via IBM watsonx.ai</sub>
</div>
