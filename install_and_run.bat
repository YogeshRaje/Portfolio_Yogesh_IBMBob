@echo off
title Yogesh Portfolio — AI-Powered Setup and Launch
color 0A
chcp 65001 > nul 2>&1

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║     YOGESH — Personal Portfolio Website                     ║
echo  ║     Agentic AI  .  Machine Learning  .  Quantum Computing   ║
echo  ║     Powered by IBM Granite  .  ibm/granite-3-3-8b-instruct  ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.

:: ══════════════════════════════════════════════════════════════
::  STEP 1 — Check Node.js
:: ══════════════════════════════════════════════════════════════
echo  [1/5] Checking Node.js installation...
node --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo  [ERROR] Node.js is not installed or not found in PATH.
    echo.
    echo  ───────────────────────────────────────────────────────────
    echo  HOW TO INSTALL NODE.JS:
    echo    1. Open your browser and go to: https://nodejs.org
    echo    2. Download the LTS version (recommended)
    echo    3. Run the installer with default settings
    echo    4. Restart this window and run this file again
    echo  ───────────────────────────────────────────────────────────
    echo.
    pause
    exit /b 1
) ELSE (
    for /f "tokens=*" %%i in ('node --version') do set NODE_VER=%%i
    echo  [OK] Node.js found: %NODE_VER%
)

:: ══════════════════════════════════════════════════════════════
::  STEP 2 — Check npm
:: ══════════════════════════════════════════════════════════════
echo.
echo  [2/5] Checking npm...
npm --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo  [ERROR] npm not found. Please reinstall Node.js from https://nodejs.org
    pause
    exit /b 1
) ELSE (
    for /f "tokens=*" %%i in ('npm --version') do set NPM_VER=%%i
    echo  [OK] npm found: v%NPM_VER%
)

:: ══════════════════════════════════════════════════════════════
::  STEP 3 — Verify project files
:: ══════════════════════════════════════════════════════════════
echo.
echo  [3/5] Verifying project files...

set MISSING=0

IF NOT EXIST "index.html" (
    echo  [MISSING] index.html — portfolio website
    set MISSING=1
)
IF NOT EXIST "server.js" (
    echo  [MISSING] server.js — web server with IBM Granite AI
    set MISSING=1
)
IF NOT EXIST "package.json" (
    echo  [MISSING] package.json — project configuration
    set MISSING=1
)
IF NOT EXIST "SDLC_PLAN.md" (
    echo  [WARNING] SDLC_PLAN.md — Agentic AI SDLC documentation (optional)
)

IF %MISSING% EQU 1 (
    echo.
    echo  [ERROR] One or more required files are missing.
    echo  Please ensure all project files are in the same folder as this .bat file.
    echo.
    pause
    exit /b 1
)
echo  [OK] All required project files verified.

:: ══════════════════════════════════════════════════════════════
::  STEP 4 — IBM Granite AI Configuration (optional)
:: ══════════════════════════════════════════════════════════════
echo.
echo  [4/5] Checking IBM Granite AI configuration...
echo.
echo  ───────────────────────────────────────────────────────────────
echo  IBM GRANITE AI ASSISTANT SETUP (OPTIONAL)
echo  ───────────────────────────────────────────────────────────────
echo  The AI assistant works in FALLBACK mode without API keys.
echo  To enable FULL IBM Granite AI responses:
echo.
echo    Option A — Set environment variables (recommended):
echo      set IBM_API_KEY=your_ibm_cloud_api_key
echo      set IBM_PROJECT_ID=your_watsonx_project_id
echo.
echo    Option B — Edit server.js:
echo      Line 23: IBM_API_KEY    = 'your_api_key_here'
echo      Line 24: IBM_PROJECT_ID = 'your_project_id_here'
echo.
echo    Get your keys at: https://cloud.ibm.com
echo    Create watsonx.ai project at: https://dataplatform.cloud.ibm.com
echo  ───────────────────────────────────────────────────────────────
echo.

IF DEFINED IBM_API_KEY (
    echo  [OK] IBM_API_KEY is set — IBM Granite AI will be active!
) ELSE (
    echo  [INFO] IBM_API_KEY not set — running in intelligent fallback mode.
    echo         The AI assistant will still answer questions using built-in knowledge.
)
echo.

:: ══════════════════════════════════════════════════════════════
::  STEP 5 — Start server and open browser
:: ══════════════════════════════════════════════════════════════
echo  [5/5] Starting Yogesh Portfolio server...
echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║  Server is starting on http://localhost:3000                 ║
echo  ║  Your browser will open automatically in 2 seconds          ║
echo  ║                                                              ║
echo  ║  Features:                                                   ║
echo  ║  ● Portfolio: About, Expertise, Skills, Programs             ║
echo  ║  ● Testimonials, Contact Form                                ║
echo  ║  ● AI Chat Widget (IBM Granite / Fallback Mode)              ║
echo  ║                                                              ║
echo  ║  Press Ctrl+C in this window to stop the server             ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.

:: Open browser after 2 seconds
start "" cmd /c "timeout /t 2 >nul && start http://localhost:3000"

:: Start the Node.js server (this window stays open showing logs)
node server.js

echo.
echo  Server stopped.
pause
