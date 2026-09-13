/**
 * Yogesh Portfolio — Node.js Server
 * Serves static files + Agentic AI API endpoint (IBM Granite via watsonx.ai)
 *
 * SETUP:
 *   1. Edit .env in the project root and set your IBM credentials:
 *        IBM_API_KEY      — your IBM Cloud API key
 *        IBM_PROJECT_ID   — your watsonx.ai project ID
 *   2. Run: node server.js   (or double-click install_and_run.bat)
 *   3. Open: http://localhost:3000
 */

'use strict';

const http  = require('http');
const https = require('https');
const fs    = require('fs');
const path  = require('path');
const url   = require('url');

// ──────────────────────────────────────────────────────────────
//  .ENV LOADER  (built-in — no dotenv package required)
//  Reads .env from the project root and injects into process.env
//  before any other config is read. Existing env vars take priority.
// ──────────────────────────────────────────────────────────────
(function loadDotEnv() {
  const envPath = path.join(__dirname, '.env');
  if (!fs.existsSync(envPath)) return;
  const lines = fs.readFileSync(envPath, 'utf8').split(/\r?\n/);
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;          // skip blanks & comments
    const eqIdx = trimmed.indexOf('=');
    if (eqIdx === -1) continue;                                  // skip malformed lines
    const key = trimmed.slice(0, eqIdx).trim();
    const val = trimmed.slice(eqIdx + 1).trim()
                       .replace(/^["']|["']$/g, '');            // strip optional quotes
    if (key && !(key in process.env)) {                          // env var wins over .env
      process.env[key] = val;
    }
  }
  console.log('  [.env] Loaded environment from .env');
})();

// ──────────────────────────────────────────────────────────────
//  IBM GRANITE CONFIGURATION  (reads from .env or environment)
// ──────────────────────────────────────────────────────────────
const IBM_API_KEY    = process.env.IBM_API_KEY    || '';
const IBM_PROJECT_ID = process.env.IBM_PROJECT_ID || '';
const PORT           = parseInt(process.env.PORT) || 3000;

// Normalise region: accept either a short code (us-south) or a full URL
// and always resolve to just the hostname component for URL construction.
let IBM_REGION_HOST  = 'us-south.ml.cloud.ibm.com';
const rawRegion = (process.env.IBM_REGION || 'us-south').trim();
if (rawRegion.startsWith('http')) {
  // e.g. "https://us-south.ml.cloud.ibm.com" — extract hostname
  try {
    IBM_REGION_HOST = new url.URL(rawRegion).hostname;
  } catch (_) {
    IBM_REGION_HOST = 'us-south.ml.cloud.ibm.com';
  }
} else if (rawRegion.includes('.ml.cloud.ibm.com')) {
  // e.g. "us-south.ml.cloud.ibm.com"
  IBM_REGION_HOST = rawRegion;
} else {
  // e.g. "us-south" → construct full hostname
  IBM_REGION_HOST = `${rawRegion}.ml.cloud.ibm.com`;
}

const WATSONX_PATH   = '/ml/v1/text/chat?version=2023-05-29';
const IAM_URL        = 'https://iam.cloud.ibm.com/identity/token';
const GRANITE_MODEL  = 'ibm/granite-3-3-8b-instruct';

// ──────────────────────────────────────────────────────────────
//  STATIC FILE MIME TYPES
// ──────────────────────────────────────────────────────────────
const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css':  'text/css',
  '.js':   'application/javascript',
  '.json': 'application/json',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.svg':  'image/svg+xml',
  '.ico':  'image/x-icon',
  '.woff': 'font/woff',
  '.woff2':'font/woff2',
};

// ──────────────────────────────────────────────────────────────
//  IBM IAM TOKEN CACHE  (token valid ~3600s; refresh at 3400s)
// ──────────────────────────────────────────────────────────────
let cachedToken   = null;
let tokenExpiry   = 0;

function getIAMToken() {
  return new Promise((resolve, reject) => {
    // Return cached token if still valid
    if (cachedToken && Date.now() < tokenExpiry) {
      return resolve(cachedToken);
    }

    const postData = `grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=${encodeURIComponent(IBM_API_KEY)}`;
    const iamParsed = new url.URL(IAM_URL);
    const options   = {
      hostname: iamParsed.hostname,
      path:     iamParsed.pathname + iamParsed.search,
      port:     443,
      method:   'POST',
      headers:  {
        'Content-Type':   'application/x-www-form-urlencoded',
        'Accept':         'application/json',
        'Content-Length': Buffer.byteLength(postData),
      },
    };

    const req = https.request(options, res => {
      let body = '';
      res.on('data', chunk => { body += chunk; });
      res.on('end', () => {
        try {
          const json = JSON.parse(body);
          if (json.access_token) {
            cachedToken = json.access_token;
            tokenExpiry = Date.now() + 3400 * 1000; // refresh 200s before expiry
            resolve(cachedToken);
          } else {
            reject(new Error('IAM token error: ' + (json.errorMessage || json.error || body.slice(0, 200))));
          }
        } catch (e) {
          reject(new Error('Failed to parse IAM response: ' + body.slice(0, 200)));
        }
      });
    });
    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

// ──────────────────────────────────────────────────────────────
//  IBM GRANITE CHAT COMPLETION
// ──────────────────────────────────────────────────────────────
const SYSTEM_PROMPT = `You are an intelligent AI assistant embedded in the personal portfolio of YOGESH RAJE, a world-class Technical Trainer specialising in Agentic AI, Machine Learning, and Quantum Computing. You are powered by IBM Granite (ibm/granite-3-3-8b-instruct) via IBM watsonx.ai.

Your persona: Professional, knowledgeable, and encouraging. You represent Yogesh Raje's brand and values.

Yogesh Raje's profile:
- Expert Technical Trainer: Agentic AI, Machine Learning, Quantum Computing
- 500+ professionals trained, 98% satisfaction rate, 50+ workshops delivered
- Based in Pune, Maharashtra, India
- Email: yogesh.raje@aigenius.in | LinkedIn: linkedin.com/in/yogeshraje
- GitHub: github.com/YogeshRaje | Portfolio: https://github.com/YogeshRaje/Portfolio_Yogesh_IBMBob
- Programs: AI Foundations Bootcamp (40h, Beginner), Applied Machine Learning (60h, Intermediate), Agentic AI Masterclass (48h, Advanced), Quantum Computing Intensive (36h, Advanced), LLMs & Prompt Engineering (24h, Intermediate), Enterprise Custom Training (Flexible)
- Expertise: IBM Granite, watsonx.ai, LangChain, AutoGen, CrewAI, RAG, Qiskit, PennyLane, TensorFlow, PyTorch

Instructions:
- Answer questions about Yogesh Raje's training programs, expertise, and contact details accurately
- Answer technical questions about Agentic AI, Machine Learning, and Quantum Computing clearly and concisely
- For booking requests, always direct the user to the contact form on the portfolio or to yogesh.raje@aigenius.in
- Use **bold** for key terms and - for bullet lists when it aids clarity
- Keep responses concise (under 250 words) and action-oriented
- Never fabricate Yogesh Raje's credentials or promise specific pricing
- Always be encouraging and professional
- This portfolio was built using the Agentic AI SDLC methodology with IBM Bob AI assistance`;

function callGranite(messages) {
  return new Promise(async (resolve, reject) => {
    let token;
    try {
      token = await getIAMToken();
    } catch (e) {
      return reject(new Error('Auth failed: ' + e.message));
    }

    const payload = JSON.stringify({
      model_id:   GRANITE_MODEL,
      project_id: IBM_PROJECT_ID,
      messages:   [
        { role: 'system', content: SYSTEM_PROMPT },
        ...messages,
      ],
      parameters: {
        max_new_tokens:     600,
        temperature:        0.7,
        top_p:              0.95,
        repetition_penalty: 1.1,
      },
    });

    const options = {
      hostname: IBM_REGION_HOST,
      path:     WATSONX_PATH,
      port:     443,
      method:   'POST',
      headers:  {
        'Content-Type':   'application/json',
        'Accept':         'application/json',
        'Authorization':  'Bearer ' + token,
        'Content-Length': Buffer.byteLength(payload),
      },
    };

    const req = https.request(options, res => {
      let body = '';
      res.on('data', chunk => { body += chunk; });
      res.on('end', () => {
        try {
          const json = JSON.parse(body);
          // watsonx.ai text/chat returns: { choices: [{ message: { content: "..." } }] }
          // Also handle legacy results[0].generated_text format
          const text =
            json?.choices?.[0]?.message?.content   ||   // OpenAI-compatible chat format
            json?.results?.[0]?.generated_text       ||  // watsonx generate format
            null;

          if (text) {
            resolve(text.trim());
          } else {
            // Surface a useful error from the API response if present
            const apiErr = json?.error?.message || json?.message || JSON.stringify(json).slice(0, 300);
            reject(new Error('Unexpected Granite response: ' + apiErr));
          }
        } catch (e) {
          reject(new Error('Failed to parse Granite response: ' + body.slice(0, 200)));
        }
      });
    });
    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

// ──────────────────────────────────────────────────────────────
//  HTTP SERVER
// ──────────────────────────────────────────────────────────────
const server = http.createServer(async (req, res) => {

  // ── CORS headers (allow browser fetch from same origin) ──
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    return res.end();
  }

  // ── POST /api/chat — Agentic AI endpoint ──
  if (req.method === 'POST' && req.url === '/api/chat') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', async () => {
      try {
        const { messages } = JSON.parse(body);
        if (!Array.isArray(messages) || messages.length === 0) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          return res.end(JSON.stringify({ error: 'messages array required' }));
        }

        // Check if API key is configured
        if (!IBM_API_KEY || IBM_API_KEY === 'YOUR_IBM_API_KEY_HERE') {
          res.writeHead(503, { 'Content-Type': 'application/json' });
          return res.end(JSON.stringify({
            error: 'IBM API key not configured. Set IBM_API_KEY and IBM_PROJECT_ID in .env',
            fallback: true,
          }));
        }

        const reply = await callGranite(messages);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ reply, model: GRANITE_MODEL }));

      } catch (err) {
        console.error('[/api/chat] Error:', err.message);
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: err.message }));
      }
    });
    return;
  }

  // ── Static file server ──
  let reqPath  = req.url.split('?')[0]; // strip query string
  let filePath = path.join(__dirname, reqPath === '/' ? 'index.html' : reqPath);
  const ext    = path.extname(filePath) || '.html';
  const contentType = MIME[ext] || 'text/plain';

  fs.readFile(filePath, (err, data) => {
    if (err) {
      // Fallback to index.html for SPA-style routing
      if (err.code === 'ENOENT') {
        fs.readFile(path.join(__dirname, 'index.html'), (err2, data2) => {
          if (err2) {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            return res.end('404 — File Not Found');
          }
          res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
          res.end(data2);
        });
      } else {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Server Error');
      }
      return;
    }
    res.writeHead(200, { 'Content-Type': contentType });
    res.end(data);
  });
});

server.listen(PORT, () => {
  const apiConfigured = !!(IBM_API_KEY && IBM_API_KEY !== 'YOUR_IBM_API_KEY_HERE' && IBM_PROJECT_ID);
  console.log('');
  console.log('  ╔══════════════════════════════════════════════════════╗');
  console.log('  ║      Yogesh Portfolio Server — Running!              ║');
  console.log('  ╠══════════════════════════════════════════════════════╣');
  console.log(`  ║   Local:   http://localhost:${PORT}                    ║`);
  console.log(`  ║   Model:   ${GRANITE_MODEL}     ║`);
  console.log(`  ║   Region:  ${IBM_REGION_HOST.padEnd(42)}║`);
  console.log(`  ║   AI API:  ${apiConfigured ? '✅ IBM Granite fully configured!    ' : '⚠️  API key/project not set         '}  ║`);
  console.log('  ╠══════════════════════════════════════════════════════╣');
  if (!apiConfigured) {
    console.log('  ║  To enable IBM Granite AI, edit .env:                ║');
    console.log('  ║    IBM_API_KEY=your_ibm_cloud_api_key                ║');
    console.log('  ║    IBM_PROJECT_ID=your_watsonx_project_id            ║');
    console.log('  ║  Get keys → https://cloud.ibm.com                   ║');
    console.log('  ╠══════════════════════════════════════════════════════╣');
  }
  console.log('  ║   Press Ctrl+C to stop the server                    ║');
  console.log('  ╚══════════════════════════════════════════════════════╝');
  console.log('');
});
