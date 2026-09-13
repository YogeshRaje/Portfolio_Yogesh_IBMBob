# Yogesh Portfolio — Agentic AI SDLC Plan

> **Project:** Personal Portfolio Web Application for Yogesh — Technical Trainer  
> **Specialisations:** Agentic AI · Machine Learning · Quantum Computing  
> **AI Integration:** IBM Granite Model (ibm/granite-3-3-8b-instruct) via IBM watsonx.ai  
> **Methodology:** Agentic AI Software Development Lifecycle (SDLC)  
> **Version:** 1.0.0  
> **Date:** 2025  

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Phase 1 — Requirements Analysis](#2-phase-1--requirements-analysis)
3. [Phase 2 — Agentic AI System Design](#3-phase-2--agentic-ai-system-design)
4. [Phase 3 — Architecture & UI/UX Design](#4-phase-3--architecture--uiux-design)
5. [Phase 4 — Development](#5-phase-4--development)
6. [Phase 5 — Agentic AI Integration](#6-phase-5--agentic-ai-integration)
7. [Phase 6 — Testing & Validation](#7-phase-6--testing--validation)
8. [Phase 7 — Deployment & Operations](#8-phase-7--deployment--operations)
9. [Technology Stack](#9-technology-stack)
10. [File Structure](#10-file-structure)
11. [Agent Persona & Behaviour Specification](#11-agent-persona--behaviour-specification)
12. [Risk Register](#12-risk-register)
13. [Success Metrics](#13-success-metrics)

---

## 1. Executive Summary

This document defines the full Agentic AI SDLC for designing, developing, and deploying a **personal portfolio web application** for **Yogesh**, an expert Technical Trainer in Agentic AI, Machine Learning, and Quantum Computing.

The application is a **single-page, Node.js-served portfolio website** enriched with an **IBM Granite-powered AI assistant** that can autonomously resolve visitors' queries about Yogesh's expertise, training programs, booking, and the subject domains he teaches.

The AI assistant follows an **agentic loop pattern** (Perceive → Reason → Act → Reflect) and uses IBM watsonx.ai's Granite model to generate contextually accurate, persona-aligned responses.

---

## 2. Phase 1 — Requirements Analysis

### 2.1 Stakeholder Identification

| Stakeholder       | Role                                    | Requirement Priority |
|-------------------|-----------------------------------------|----------------------|
| Yogesh            | Portfolio owner, primary beneficiary    | P0 — Must Have       |
| Corporate Clients | Companies seeking AI/ML trainers        | P0 — Must Have       |
| Individual Learners | Professionals upskilling              | P1 — Should Have     |
| Universities      | Academic institutions seeking trainer   | P1 — Should Have     |
| Recruiters        | Talent acquisition seeking SMEs         | P2 — Could Have      |

### 2.2 Functional Requirements

#### Portfolio Sections
- [x] **Hero Section** — Name, title, animated gradient, CTAs
- [x] **About Section** — Bio, stats (500+ trained, 98% satisfaction), animated rings
- [x] **Expertise Section** — Agentic AI, Machine Learning, Quantum Computing cards
- [x] **Skills Section** — Animated proficiency bars per domain
- [x] **Training Programs** — 6 structured programs with level, duration, format
- [x] **Testimonials** — 3 participant reviews from recognisable companies
- [x] **Contact Section** — Form + contact details + social links
- [x] **Footer** — Navigation links, copyright

#### Agentic AI Assistant
- [x] **Floating chat widget** — accessible from every page section
- [x] **IBM Granite model integration** — via watsonx.ai REST API
- [x] **Contextual persona** — assistant knows Yogesh's full profile
- [x] **Agentic loop** — perceive user intent → plan response → act → reflect
- [x] **Tool use simulation** — booking tool, program lookup tool, FAQ tool
- [x] **Conversation memory** — multi-turn context retained in session
- [x] **Fallback handling** — offline/demo mode when API unavailable
- [x] **Suggested prompts** — quick-action buttons to seed conversation

### 2.3 Non-Functional Requirements

| Category        | Requirement                                           |
|-----------------|-------------------------------------------------------|
| Performance     | Page load < 2s; AI response < 5s                      |
| Accessibility   | WCAG 2.1 AA compliant; keyboard navigable             |
| Responsiveness  | Mobile, tablet, desktop breakpoints                   |
| Security        | API key stored server-side; never exposed to client   |
| Portability     | Zero-dependency Node.js server; runs on any OS        |
| Usability       | Single .bat file setup for non-technical users        |

### 2.4 Constraints

- **No external CDN dependencies** — all assets inlined or self-hosted
- **Node.js built-in modules only** for the static server (http, fs, path)
- **IBM Granite** specifically required as the LLM backbone
- **Single HTML file** + minimal JS/CSS for maximum portability

---

## 3. Phase 2 — Agentic AI System Design

### 3.1 Agentic Architecture: PAAR Loop

```
┌─────────────────────────────────────────────────────────────┐
│                    YOGESH AI ASSISTANT                       │
│                    (Agentic PAAR Loop)                       │
├──────────────┬──────────────┬──────────────┬────────────────┤
│   PERCEIVE   │    ASSESS    │     ACT      │    REFLECT     │
│              │              │              │                │
│ Parse user   │ Classify     │ Select tool  │ Evaluate       │
│ message      │ intent:      │ or generate  │ response       │
│              │ • FAQ        │ direct       │ quality        │
│ Extract      │ • Program    │ Granite      │                │
│ entities     │   query      │ completion   │ Check persona  │
│              │ • Booking    │              │ alignment      │
│ Build        │ • Technical  │ Format &     │                │
│ context      │ • Fallback   │ stream reply │ Log for        │
│ window       │              │              │ learning       │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

### 3.2 Agent Tools (Simulated)

| Tool Name           | Trigger Intent        | Action                                      |
|---------------------|-----------------------|---------------------------------------------|
| `lookup_programs`   | "tell me about your programs", "what courses" | Return structured program list  |
| `book_session`      | "book", "schedule", "enrol"                    | Redirect to contact section     |
| `get_profile`       | "who are you", "about yogesh"                  | Return trainer biography        |
| `answer_technical`  | Domain questions (AI, ML, Quantum)             | IBM Granite completion          |
| `get_contact_info`  | "email", "contact", "reach"                    | Return contact details          |
| `list_testimonials` | "reviews", "testimonials", "feedback"          | Return participant quotes        |

### 3.3 System Prompt (Granite Persona)

```
You are an intelligent AI assistant embedded in the personal portfolio of YOGESH,
a world-class Technical Trainer specialising in Agentic AI, Machine Learning, and
Quantum Computing. You are powered by IBM Granite.

Your persona:
- Professional, knowledgeable, and encouraging
- You represent Yogesh's expertise and values
- You help visitors learn about programs, book sessions, and answer technical questions
- You never fabricate information about Yogesh's credentials
- You acknowledge when something is outside your knowledge

Yogesh's profile:
- 500+ professionals trained, 98% satisfaction rate
- 50+ workshops delivered
- Programs: AI Foundations, Applied ML, Agentic AI Masterclass, Quantum Intensive,
  LLMs & Prompt Engineering, Enterprise Custom Training
- Location: Pune, Maharashtra, India
- Email: yogesh@aigenius.in
```

### 3.4 Context Window Management

- **System prompt** injected once at session start
- **Conversation history** maintained as rolling array (last 10 turns)
- **Token budget**: ~2,000 tokens reserved for response; history trimmed if needed
- **Entity memory**: program preferences, user name extracted and persisted

---

## 4. Phase 3 — Architecture & UI/UX Design

### 4.1 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT                                │
│  Browser (index.html + inline CSS/JS)                        │
│  ┌──────────────┐    ┌──────────────────────────────────┐   │
│  │ Portfolio    │    │  AI Chat Widget                  │   │
│  │ Sections     │    │  - Floating button               │   │
│  │              │    │  - Message thread                │   │
│  │              │    │  - Suggested prompts             │   │
│  │              │    │  - Streaming response display    │   │
│  └──────────────┘    └────────────┬─────────────────────┘   │
└───────────────────────────────────┼─────────────────────────┘
                                    │ POST /api/chat (JSON)
┌───────────────────────────────────┼─────────────────────────┐
│                     SERVER (server.js)                       │
│                                   │                          │
│  ┌─────────────────────────────── ▼ ─────────────────────┐  │
│  │  /api/chat endpoint                                    │  │
│  │  1. Parse request body                                 │  │
│  │  2. Build Granite messages array                       │  │
│  │  3. POST to watsonx.ai REST API                        │  │
│  │  4. Return AI response as JSON                         │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Static file server (index.html, assets)               │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼──────────────────┐
                    │       IBM watsonx.ai              │
                    │  Model: ibm/granite-3-3-8b-instruct│
                    │  Endpoint: us-south.ml.cloud.ibm.com│
                    └───────────────────────────────────┘
```

### 4.2 UI/UX Design Principles

- **Dark futuristic theme** — Deep navy (#0a0f1e) with cyan/purple/green accents
- **Glassmorphism nav** — Frosted glass navigation bar
- **Animated hero** — Grid background + radial gradients + rotating rings
- **Card-based layout** — Expertise cards, program cards, testimonial cards
- **Floating AI widget** — Bottom-right, pulsing beacon, expandable chat drawer
- **Smooth scroll** — CSS `scroll-behavior: smooth`
- **Mobile-first breakpoints** — Collapse to single column at 768px

---

## 5. Phase 4 — Development

### 5.1 Development Iterations

#### Sprint 1 — Static Portfolio (Day 1)
- Hero, About, Expertise, Skills sections
- Navigation with scroll-spy
- Responsive layout

#### Sprint 2 — Programs & Social Proof (Day 1)
- Training Programs grid
- Testimonials section
- Contact form with validation feedback
- Footer

#### Sprint 3 — Agentic AI Layer (Day 1–2)
- Floating chat widget HTML/CSS
- Chat JavaScript (message handling, API calls, streaming display)
- Server-side `/api/chat` endpoint
- IBM Granite API integration
- Fallback demo mode

#### Sprint 4 — Polish & Packaging (Day 2)
- Animations, hover effects
- Mobile responsiveness
- .bat installer
- SDLC documentation

### 5.2 Key Implementation Decisions

| Decision                    | Choice                          | Rationale                                    |
|-----------------------------|---------------------------------|----------------------------------------------|
| Server framework            | Node.js built-in `http`         | Zero dependencies; maximum portability       |
| AI API call location        | Server-side only                | API key security — never sent to browser     |
| Chat UI pattern             | Floating widget                 | Non-intrusive; accessible from all sections  |
| Response mode               | JSON REST (non-streaming)       | Simpler; works without EventSource on server |
| Model selection             | granite-3-3-8b-instruct         | Fast, instruction-tuned, IBM-official        |
| Fallback strategy           | Intelligent pre-programmed responses | UX continuity when API unavailable      |

---

## 6. Phase 5 — Agentic AI Integration

### 6.1 IBM Granite API Configuration

```
Endpoint Base: https://us-south.ml.cloud.ibm.com
Auth: POST /identity/token → Bearer token
Inference: POST /ml/v1/text/chat?version=2023-05-29
Model: ibm/granite-3-3-8b-instruct
Max tokens: 600
Temperature: 0.7
```

### 6.2 Agentic Flow Diagram

```
User types message
       │
       ▼
  Client sends POST /api/chat
  { messages: [...history], userMessage: "..." }
       │
       ▼
  Server: Build system prompt + history
       │
       ▼
  Server: Call IBM watsonx.ai
  (ibm/granite-3-3-8b-instruct)
       │
       ├── Success → Return { reply: "..." }
       │
       └── Failure → Return fallback response
       │
       ▼
  Client: Append message to thread
  Client: Update conversation history
       │
       ▼
  User reads response → continues conversation
```

### 6.3 Environment Variables

| Variable              | Description                             | Required |
|-----------------------|-----------------------------------------|----------|
| `IBM_API_KEY`         | IBM Cloud API key for watsonx.ai        | Yes      |
| `IBM_PROJECT_ID`      | watsonx.ai project ID                   | Yes      |
| `IBM_REGION`          | Region (default: us-south)              | No       |
| `PORT`                | Server port (default: 3000)             | No       |

---

## 7. Phase 6 — Testing & Validation

### 7.1 Test Cases

#### Portfolio UI Tests
| Test ID | Description                          | Expected Result        |
|---------|--------------------------------------|------------------------|
| UI-001  | Page loads at localhost:3000         | Status 200, HTML served|
| UI-002  | Nav links scroll to correct section  | Smooth scroll          |
| UI-003  | Contact form submit feedback         | Button shows ✅ Sent   |
| UI-004  | Mobile layout at 375px width         | Single-column layout   |
| UI-005  | All 6 program cards render           | No overflow, aligned   |

#### Agentic AI Tests
| Test ID | Description                          | Expected Result                    |
|---------|--------------------------------------|------------------------------------|
| AI-001  | Chat widget opens on button click    | Panel slides in                    |
| AI-002  | "Who is Yogesh?" query               | Bio response with expertise        |
| AI-003  | "Tell me about Quantum Computing"    | Granite technical response         |
| AI-004  | "Book a session" query               | Redirects + contact info           |
| AI-005  | API unavailable (no API key)         | Graceful fallback, no crash        |
| AI-006  | Multi-turn conversation              | Context retained across turns      |
| AI-007  | Suggested prompt click               | Auto-sends query                   |

### 7.2 Acceptance Criteria

- [ ] All 5 portfolio sections render correctly
- [ ] AI assistant responds to any user query
- [ ] IBM Granite used as the LLM (confirmed via model_id in API response)
- [ ] Fallback works when API key not configured
- [ ] `.bat` file launches server and opens browser in < 10 seconds
- [ ] Mobile layout works on 375px viewport
- [ ] No console errors on page load

---

## 8. Phase 7 — Deployment & Operations

### 8.1 Local Deployment (Primary)

```bash
# Windows
double-click install_and_run.bat

# Manual
node server.js
# Open: http://localhost:3000
```

### 8.2 IBM Granite API Key Setup

1. Create account at https://cloud.ibm.com
2. Create a watsonx.ai service instance
3. Create a project and note the Project ID
4. Generate an API key under Manage → Access → API Keys
5. Set environment variables before running:
   ```
   set IBM_API_KEY=your_api_key_here
   set IBM_PROJECT_ID=your_project_id_here
   ```
   Or edit `server.js` lines marked `// CONFIGURE HERE`

### 8.3 Production Deployment Options

| Platform       | Command / Notes                                        |
|----------------|--------------------------------------------------------|
| IBM Code Engine | `ibmcloud ce application create --name yogesh-portfolio` |
| Vercel         | `vercel --prod` (add env vars in dashboard)            |
| Railway        | Connect GitHub repo, set env vars                      |
| Docker         | `docker build -t yogesh-portfolio . && docker run -p 3000:3000` |

---

## 9. Technology Stack

| Layer           | Technology                              | Version  |
|-----------------|-----------------------------------------|----------|
| Runtime         | Node.js                                 | ≥ 18.x   |
| HTTP Server     | Node.js `http` (built-in)              | —        |
| Frontend        | HTML5 + CSS3 + Vanilla JavaScript       | —        |
| AI Model        | IBM Granite 3.3 8B Instruct             | Latest   |
| AI Platform     | IBM watsonx.ai                          | v1       |
| AI API          | watsonx.ai Text Chat REST API           | 2023-05-29|
| Installer       | Windows Batch Script (.bat)             | —        |
| Package Manager | npm                                     | ≥ 8.x    |

---

## 10. File Structure

```
yogesh-portfolio/
├── index.html              # Complete SPA: portfolio + AI chat widget
├── server.js               # Node.js HTTP server + /api/chat endpoint
├── package.json            # Project metadata
├── install_and_run.bat     # One-click Windows launcher
└── SDLC_PLAN.md            # This document — full SDLC plan
```

---

## 11. Agent Persona & Behaviour Specification

### 11.1 Personality Traits

- **Expert** — speaks with authority on AI, ML, Quantum domains
- **Encouraging** — motivates learners, celebrates curiosity
- **Concise** — no unnecessary fluff; direct, useful answers
- **Professional** — represents Yogesh's brand and reputation

### 11.2 Tone Examples

| User Query                          | Agent Tone                        |
|-------------------------------------|-----------------------------------|
| "What is a qubit?"                  | Educational, patient, analogy-rich|
| "How do I book a session?"          | Helpful, action-oriented          |
| "Is Yogesh good at teaching?"       | Confident, evidence-based         |
| "Explain Agentic AI to a beginner"  | Clear, structured, jargon-free    |

### 11.3 Guardrails

- Does NOT generate harmful content
- Does NOT fabricate Yogesh's credentials
- Does NOT promise specific pricing
- Does NOT collect sensitive personal data
- ALWAYS redirects booking requests to the contact form

---

## 12. Risk Register

| Risk                                    | Probability | Impact | Mitigation                                    |
|-----------------------------------------|-------------|--------|-----------------------------------------------|
| IBM API key not configured              | Medium      | High   | Intelligent fallback responses built-in        |
| watsonx.ai API downtime                 | Low         | Medium | Fallback mode; status message to user          |
| Token limit exceeded in long chats      | Low         | Low    | History trimmed to last 10 turns               |
| User submits inappropriate queries      | Low         | Medium | Granite's built-in safety filters              |
| Node.js not installed on target machine | Medium      | High   | .bat file checks and provides download link    |
| Port 3000 in use                        | Low         | Low    | Server prints error with clear message         |

---

## 13. Success Metrics

| Metric                           | Target          | Measurement Method          |
|----------------------------------|-----------------|------------------------------|
| Page load time                   | < 2 seconds     | Browser DevTools Network tab |
| AI response latency              | < 5 seconds     | Chat widget timestamp delta  |
| Contact form submission rate     | > 15%           | Server-side logging          |
| Chat widget engagement rate      | > 40% of visits | JS event logging             |
| Mobile usability score           | > 90/100        | Google Lighthouse            |
| Visitor-to-booking conversion    | > 10%           | Contact form + follow-up     |

---

## Appendix A — Agentic AI SDLC vs Traditional SDLC

| Dimension              | Traditional SDLC              | Agentic AI SDLC                          |
|------------------------|-------------------------------|------------------------------------------|
| Requirements           | Static, upfront               | Living document; agents surface new reqs |
| Design                 | Human-designed flows          | Agent behaviour + tool use designed      |
| Development            | Deterministic code            | Probabilistic AI + deterministic shell   |
| Testing                | Unit/integration tests        | + Prompt testing, hallucination checks   |
| Deployment             | Ship once                     | Continuous prompt & model updates        |
| Monitoring             | Logs, metrics                 | + Conversation analytics, agent traces   |

---

*Document authored following Agentic AI SDLC principles.*  
*IBM Granite model (ibm/granite-3-3-8b-instruct) powers the AI assistant.*  
*© 2025 Yogesh — All rights reserved.*
