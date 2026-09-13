@echo off
title Yogesh Raje Portfolio — AI-Powered Setup and Launch
color 0A
chcp 65001 > nul 2>&1

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║     YOGESH RAJE — Personal Portfolio Website                ║
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
    echo  ─────────────────────────────────────────────────────────────
    echo  HOW TO INSTALL NODE.JS:
    echo    1. Open your browser and go to: https://nodejs.org
    echo    2. Download the LTS version (recommended)
    echo    3. Run the installer with default settings
    echo    4. RESTART this window and run this file again
    echo  ─────────────────────────────────────────────────────────────
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
    echo  [INFO] SDLC_PLAN.md — Agentic AI SDLC documentation (optional)
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
echo  ─────────────────────────────────────────────────────────────────
echo  IBM GRANITE AI ASSISTANT — CREDENTIALS STATUS
echo  ─────────────────────────────────────────────────────────────────

:: Check .env file existence
IF NOT EXIST ".env" (
    echo  [WARNING] .env file not found.
    echo            Creating a template .env — please fill in your credentials.
    echo.
    (
        echo # Yogesh Portfolio .env
        echo IBM_API_KEY=YOUR_IBM_API_KEY_HERE
        echo IBM_PROJECT_ID=YOUR_PROJECT_ID_HERE
        echo IBM_REGION=us-south
        echo PORT=3000
    ) > .env
)

:: Parse .env to check if IBM_API_KEY and IBM_PROJECT_ID are configured
set ENV_KEY_SET=0
set ENV_PROJ_SET=0

IF EXIST ".env" (
    for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
        if /i "%%A"=="IBM_API_KEY" (
            if not "%%B"=="YOUR_IBM_API_KEY_HERE" (
                if not "%%B"=="" (
                    set ENV_KEY_SET=1
                )
            )
        )
        if /i "%%A"=="IBM_PROJECT_ID" (
            if not "%%B"=="YOUR_PROJECT_ID_HERE" (
                if not "%%B"=="" (
                    set ENV_PROJ_SET=1
                )
            )
        )
    )
)

IF %ENV_KEY_SET% EQU 1 (
    echo  [OK] IBM_API_KEY    : configured in .env
) ELSE IF DEFINED IBM_API_KEY (
    echo  [OK] IBM_API_KEY    : set as environment variable
    set ENV_KEY_SET=1
) ELSE (
    echo  [WARN] IBM_API_KEY    : not set — running in fallback mode
)

IF %ENV_PROJ_SET% EQU 1 (
    echo  [OK] IBM_PROJECT_ID : configured in .env
) ELSE IF DEFINED IBM_PROJECT_ID (
    echo  [OK] IBM_PROJECT_ID : set as environment variable
    set ENV_PROJ_SET=1
) ELSE (
    echo  [WARN] IBM_PROJECT_ID : not set — running in fallback mode
)

echo.

IF %ENV_KEY_SET% EQU 1 IF %ENV_PROJ_SET% EQU 1 (
    echo  [IBM GRANITE] ACTIVE — Full AI responses powered by IBM Granite!
) ELSE (
    echo  [IBM GRANITE] FALLBACK MODE — AI will use intelligent pre-built responses.
    echo.
    echo  To enable full IBM Granite AI:
    echo    1. Edit .env in this folder
    echo    2. Set IBM_API_KEY and IBM_PROJECT_ID
    echo    3. Get keys at: https://cloud.ibm.com
)
echo.
echo  ─────────────────────────────────────────────────────────────────
echo.

:: ══════════════════════════════════════════════════════════════
::  STEP 5 — Start server and open browser
:: ══════════════════════════════════════════════════════════════
echo  [5/5] Starting Yogesh Portfolio server...
echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║   Server starting on: http://localhost:3000                  ║
echo  ║   Browser opens automatically in 3 seconds                  ║
echo  ║                                                              ║
echo  ║   Portfolio Sections:                                        ║
echo  ║   • Hero · About · Expertise · Skills                       ║
echo  ║   • Training Programs · Testimonials · Contact              ║
echo  ║                                                              ║
echo  ║   AI Features (IBM Granite):                                 ║
echo  ║   • Floating Chat Widget (bottom-right)                      ║
echo  ║   • Ask AI Assistant button in nav                           ║
echo  ║   • Multi-turn conversation with memory                      ║
echo  ║   • Model: ibm/granite-3-3-8b-instruct                      ║
echo  ║                                                              ║
echo  ║   Press Ctrl+C in this window to stop the server            ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.

:: Open browser after 3 seconds
start "" cmd /c "timeout /t 3 >nul && start http://localhost:3000"

:: Start the Node.js server (this window stays open showing logs)
node server.js

echo.
echo  ─────────────────────────────────────────────────────────────────
echo  Server stopped. Press any key to exit.
echo  ─────────────────────────────────────────────────────────────────
echo.
pause
