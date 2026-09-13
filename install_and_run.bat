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
::  STEP 4 — IBM Granite AI Configuration via .env
:: ══════════════════════════════════════════════════════════════
echo.
echo  [4/5] Checking IBM Granite AI configuration (.env)...
echo.
echo  ───────────────────────────────────────────────────────────────
echo  IBM GRANITE AI ASSISTANT — .env SETUP (RECOMMENDED)
echo  ───────────────────────────────────────────────────────────────
echo.
echo  Edit the .env file in this folder and set your credentials:
echo.
echo    IBM_API_KEY=your_ibm_cloud_api_key_here
echo    IBM_PROJECT_ID=your_watsonx_project_id_here
echo.
echo  The server reads .env automatically on startup (no restart
echo  needed after editing — just re-run this file).
echo.
echo  How to get your keys:
echo    IBM API Key   → https://cloud.ibm.com  ^> Manage ^> Access ^> API Keys
echo    Project ID    → https://dataplatform.cloud.ibm.com ^> your project ^> Settings
echo.
echo  ⚠  NEVER commit .env to git — it is already in .gitignore.
echo  ───────────────────────────────────────────────────────────────
echo.

:: Check .env file existence and whether IBM_API_KEY is set
IF NOT EXIST ".env" (
    echo  [WARNING] .env file not found.
    echo            Please create a .env file in the same folder as this script.
    echo.
)

:: Parse .env to check if IBM_API_KEY has been filled in
set ENV_KEY_SET=0
IF EXIST ".env" (
    for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
        if /i "%%A"=="IBM_API_KEY" (
            if not "%%B"=="YOUR_IBM_API_KEY_HERE" (
                if not "%%B"=="" (
                    set ENV_KEY_SET=1
                )
            )
        )
    )
)

IF %ENV_KEY_SET% EQU 1 (
    echo  [OK] IBM_API_KEY found in .env — IBM Granite AI will be active!
) ELSE IF DEFINED IBM_API_KEY (
    echo  [OK] IBM_API_KEY set as environment variable — IBM Granite AI will be active!
) ELSE (
    echo  [INFO] IBM_API_KEY not configured — running in intelligent fallback mode.
    echo         Edit .env to enable full IBM Granite responses.
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
