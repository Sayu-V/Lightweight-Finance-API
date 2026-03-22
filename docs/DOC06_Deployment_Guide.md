# Lightweight Finance API — Deployment Guide

**Document ID:** DOC-06  
**Version:** 1.0  
**Project:** Lightweight Finance API  
**Author:** Sayu V | Yenepoya University  
**Programme:** IBM SkillsBuild Student Project | 2023–2026 Batch  
**Date:** March 2025  
**Format:** Markdown (.md)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Prerequisites](#2-prerequisites)
3. [Get the Code](#3-get-the-code)
4. [Method A — Run Locally (Python)](#4-method-a--run-locally-python)
5. [Method B — Run with Docker](#5-method-b--run-with-docker)
6. [Verify the Deployment](#6-verify-the-deployment)
7. [Environment Configuration](#7-environment-configuration)
8. [Dockerfile — Line-by-Line Explanation](#8-dockerfile--line-by-line-explanation)
9. [Stopping and Restarting](#9-stopping-and-restarting)
10. [Troubleshooting](#10-troubleshooting)
11. [Cloud Deployment Concepts](#11-cloud-deployment-concepts)
12. [Deployment Checklist](#12-deployment-checklist)

---

## 1. Overview

This guide provides complete step-by-step instructions for deploying the Lightweight Finance API on any machine. Two deployment methods are covered:

| Method | Tool Required | Best For | Setup Time |
|--------|--------------|----------|-----------|
| **A — Local Python** | Python 3.10+ | Development, quick testing | ~2 minutes |
| **B — Docker** | Docker Desktop | Consistent, portable deployment | ~3–5 minutes |

Both methods serve the API at:

```
http://localhost:8000
```

Interactive documentation is available at:

```
http://localhost:8000/docs      ← Swagger UI (recommended)
http://localhost:8000/redoc     ← ReDoc
```

> **Data persistence note:** All income, expense, and budget data is stored in memory. The data is cleared every time the server stops or restarts. This is expected behaviour for v1.

---

## 2. Prerequisites

### Method A — Local Python

| Requirement | Minimum Version | How to Check | Install |
|-------------|----------------|--------------|---------|
| Python | 3.10 or higher | `python --version` or `python3 --version` | [python.org/downloads](https://www.python.org/downloads/) |
| pip | Any recent version | `pip --version` | Included with Python |
| Git | Any recent version | `git --version` | [git-scm.com](https://git-scm.com/) |

### Method B — Docker

| Requirement | Minimum Version | How to Check | Install |
|-------------|----------------|--------------|---------|
| Docker Desktop | Latest stable | `docker --version` | [docs.docker.com/get-docker](https://docs.docker.com/get-docker/) |
| Git | Any recent version | `git --version` | [git-scm.com](https://git-scm.com/) |

> **Note for Windows users:** Docker Desktop on Windows requires WSL 2 (Windows Subsystem for Linux 2) or Hyper-V. Both are supported. Run all commands in PowerShell or Command Prompt (not Git Bash for Docker commands).

### Checking Your Python Version

```bash
# macOS / Linux
python3 --version

# Windows
python --version
```

Expected output (any 3.10.x or higher):

```
Python 3.10.12
```

If your version is below 3.10, download and install the latest Python from [python.org](https://www.python.org/downloads/) before continuing.

---

## 3. Get the Code

### Clone the Repository

```bash
git clone https://github.com/Sayu-V/Lightweight-Finance-API.git
cd Lightweight-Finance-API
```

### Verify the Project Structure

After cloning, your directory should contain:

```
Lightweight-Finance-API/
├── main.py             ← FastAPI application (routes + storage)
├── models.py           ← Pydantic request models
├── requirements.txt    ← Python dependencies
├── Dockerfile          ← Docker build instructions
├── README.md           ← Project overview
└── docs/
    ├── PROPOSAL        ← Project Proposal
    ├── HLD             ← High-Level Design
    ├── LLD             ← Low-Level Design
    └── FINAL_REPORT.md ← Final Report
```

If any of these files are missing, re-clone the repository or check that you are on the correct branch:

```bash
git branch        # see current branch
git checkout main # switch to main if needed
```

---

## 4. Method A — Run Locally (Python)

Use this method for quick development and testing. No Docker required.

### Step 1 — Create a Virtual Environment (Recommended)

A virtual environment keeps the project's dependencies isolated from your system Python.

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

You should see `(venv)` appear at the start of your terminal prompt, confirming the virtual environment is active.

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs `fastapi` and `uvicorn`. Expected output (last line):

```
Successfully installed anyio-... fastapi-... uvicorn-...
```

> **Tip:** If you see `ERROR: Could not find a version that satisfies the requirement`, ensure your pip is up to date: `pip install --upgrade pip`

### Step 3 — Start the Server

**Development mode (with auto-reload on file changes):**

```bash
uvicorn main:app --reload
```

**Production mode (stable, no auto-reload):**

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Step 4 — Confirm the Server is Running

Look for this output in your terminal:

```
INFO:     Will watch for changes in these directories: ['/path/to/project']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

The key line is:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Open your browser and navigate to `http://localhost:8000/docs` to see the Swagger UI.

### Uvicorn Command Flags Explained

| Flag | Purpose | Example |
|------|---------|---------|
| `main:app` | Module name (`main.py`) and FastAPI instance name (`app`) | Always required |
| `--reload` | Auto-restart server when code changes | Development only |
| `--host 0.0.0.0` | Listen on all network interfaces (not just localhost) | Required for Docker |
| `--port 8000` | Port number to listen on | Default is 8000 |
| `--workers 4` | Number of worker processes (v2 with PostgreSQL) | Production only |

---

## 5. Method B — Run with Docker

Use this method for a consistent, reproducible environment that matches production deployment. Docker eliminates "works on my machine" issues.

### Step 1 — Verify Docker is Running

```bash
docker --version
```

Expected output:

```
Docker version 24.0.5, build ced0996
```

Also confirm the Docker daemon is running:

```bash
docker info
```

If you see `ERROR: Cannot connect to the Docker daemon`, open Docker Desktop and wait for it to fully start before continuing.

### Step 2 — Build the Docker Image

From inside the project directory (where the `Dockerfile` is located):

```bash
docker build -t finance-api .
```

**Flag explanation:**

| Part | Meaning |
|------|---------|
| `docker build` | Build a Docker image from a Dockerfile |
| `-t finance-api` | Tag (name) the image as `finance-api` |
| `.` | Use the current directory as the build context |

**Expected output (last few lines):**

```
Step 5/5 : CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
 ---> Running in a8b3c2d1e4f5
Removing intermediate container a8b3c2d1e4f5
 ---> 9f8e7d6c5b4a
Successfully built 9f8e7d6c5b4a
Successfully tagged finance-api:latest
```

### Step 3 — Run the Container

```bash
docker run -p 8000:8000 finance-api
```

**Flag explanation:**

| Part | Meaning |
|------|---------|
| `docker run` | Create and start a new container |
| `-p 8000:8000` | Map host port 8000 to container port 8000 |
| `finance-api` | The image name we tagged in Step 2 |

**Run in detached mode (background):**

```bash
docker run -d -p 8000:8000 --name finance-api-container finance-api
```

| Additional Flag | Meaning |
|----------------|---------|
| `-d` | Detached — runs in the background |
| `--name finance-api-container` | Gives the container a memorable name |

### Step 4 — Confirm the Container is Running

```bash
docker ps
```

Expected output:

```
CONTAINER ID   IMAGE         COMMAND                  CREATED         STATUS         PORTS                    NAMES
a1b2c3d4e5f6   finance-api   "uvicorn main:app --…"   5 seconds ago   Up 4 seconds   0.0.0.0:8000->8000/tcp   finance-api-container
```

The key columns are **STATUS** (`Up`) and **PORTS** (`0.0.0.0:8000->8000/tcp`).

---

## 6. Verify the Deployment

Use these checks after either deployment method to confirm everything is working correctly.

### Check 1 — Swagger UI Loads

Open your browser:

```
http://localhost:8000/docs
```

You should see the FastAPI Swagger UI listing 5 endpoints:

```
POST  /income
POST  /expense
GET   /summary
POST  /budget
GET   /budget-status
```

### Check 2 — Quick curl Test

Run this command in a new terminal window (keep the server running in the original):

```bash
curl http://localhost:8000/summary
```

Expected response:

```json
{"total_income":0,"total_expense":0,"balance":0}
```

### Check 3 — Full Endpoint Verification

Run all five endpoints in sequence:

```bash
# 1. Add income
curl -s -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": 5000, "source": "Salary"}' | python3 -m json.tool

# 2. Add expense
curl -s -X POST http://localhost:8000/expense \
  -H "Content-Type: application/json" \
  -d '{"amount": 200, "category": "Groceries"}' | python3 -m json.tool

# 3. Get summary
curl -s http://localhost:8000/summary | python3 -m json.tool

# 4. Set budget
curl -s -X POST http://localhost:8000/budget \
  -H "Content-Type: application/json" \
  -d '{"limit": 3000}' | python3 -m json.tool

# 5. Get budget status
curl -s http://localhost:8000/budget-status | python3 -m json.tool
```

> **Note:** The `-s` flag silences curl's progress meter. `python3 -m json.tool` pretty-prints the JSON response.

**Expected outputs in sequence:**

```json
{ "message": "Income added successfully" }
{ "message": "Expense added successfully" }
{ "total_income": 5000.0, "total_expense": 200.0, "balance": 4800.0 }
{ "message": "Budget set successfully" }
{ "budget": 3000.0, "spent": 200.0, "remaining": 2800.0 }
```

### Check 4 — Validation Test (Error Case)

```bash
curl -s -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": -100, "source": "Test"}' | python3 -m json.tool
```

Expected (HTTP 400):

```json
{
    "detail": "Amount must be greater than 0"
}
```

If all four checks pass, the deployment is successful. ✅

---

## 7. Environment Configuration

### Current State (v1)

The v1 application has no environment variables. All configuration is hardcoded:

| Setting | Value | Location |
|---------|-------|----------|
| Host | `0.0.0.0` | `Dockerfile` CMD |
| Port | `8000` | `Dockerfile` CMD |
| App title | `"Lightweight Finance API"` | `main.py` FastAPI constructor |
| Storage | In-memory Python lists | `main.py` module level |

### Planned for v2 — `.env` Configuration

When PostgreSQL and JWT authentication are added in v2, the application will read configuration from a `.env` file. The structure will be:

```bash
# .env — copy from .env.example and fill in values
# Never commit .env to version control

DATABASE_URL=postgresql://user:password@localhost:5432/finance_db
SECRET_KEY=your-256-bit-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_ENV=development
```

```bash
# .env.example — safe to commit (no real values)
DATABASE_URL=postgresql://user:password@localhost:5432/finance_db
SECRET_KEY=replace-with-a-strong-random-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_ENV=development
```

> **Security rule:** The `.env` file containing real values is **always** in `.gitignore`. Only `.env.example` is committed to version control.

### Changing the Port

To run on a different port (e.g. 9000):

**Local:**

```bash
uvicorn main:app --port 9000
```

**Docker:**

```bash
docker run -p 9000:8000 finance-api
```

This maps host port 9000 to container port 8000. Access via `http://localhost:9000`.

---

## 8. Dockerfile — Line-by-Line Explanation

Here is the complete Dockerfile with each line explained:

```dockerfile
# Use official Python image as the base
# python:3.10 = Python 3.10 on Debian Linux
# Using a specific version ensures reproducibility
FROM python:3.10

# Set the working directory inside the container
# All subsequent commands run from this directory
# Files copied to the container land here
WORKDIR /app

# Copy all files from the current directory on the host
# into the /app directory inside the container
# The first . = source (host), second . = destination (container /app)
COPY . .

# Install Python dependencies from requirements.txt
# --no-cache-dir reduces the image size by not caching pip downloads
RUN pip install --no-cache-dir -r requirements.txt

# Tell Docker that the container listens on port 8000
# This is documentation — it does not actually publish the port
# Port publishing happens with -p flag in docker run
EXPOSE 8000

# The command to run when the container starts
# uvicorn = the ASGI server
# main:app = module main.py, FastAPI instance named app
# --host 0.0.0.0 = listen on all interfaces (required in Docker)
# --port 8000 = listen on port 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Why `--host 0.0.0.0` is Required in Docker

By default, Uvicorn listens only on `127.0.0.1` (localhost inside the container). This means traffic from outside the container (including from your host machine via `-p 8000:8000`) cannot reach it. Setting `--host 0.0.0.0` tells Uvicorn to accept connections on all network interfaces, making the port-mapping work correctly.

```
Without 0.0.0.0:   Host ──→ Container port 8000 ──→ 127.0.0.1:8000 ✗ (unreachable)
With    0.0.0.0:   Host ──→ Container port 8000 ──→ 0.0.0.0:8000   ✓ (reachable)
```

### Docker Image Size Optimisation (v2)

For production, replace `python:3.10` with `python:3.10-slim` to reduce the image size from ~1 GB to ~150 MB:

```dockerfile
FROM python:3.10-slim    # Use this in production
```

---

## 9. Stopping and Restarting

### Stop Local Server

Press `Ctrl + C` in the terminal where the server is running.

```
^C
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [12346]
```

### Stop Docker Container

**If running in foreground:** Press `Ctrl + C`

**If running in detached mode (`-d`):**

```bash
# Stop the container (graceful shutdown)
docker stop finance-api-container

# Or by container ID (get from docker ps)
docker stop a1b2c3d4e5f6
```

### Restart a Stopped Container

```bash
# Restart without rebuilding
docker start finance-api-container

# View logs to confirm it started
docker logs finance-api-container
```

### Rebuild After Code Changes

If you change `main.py` or `models.py`, you must rebuild the image:

```bash
docker build -t finance-api .
docker run -p 8000:8000 finance-api
```

> **Local (Method A):** If you started with `--reload`, code changes are applied automatically without restarting.

### Remove Old Containers and Images

```bash
# List all containers (including stopped)
docker ps -a

# Remove a stopped container
docker rm finance-api-container

# Remove the image
docker rmi finance-api

# Remove all stopped containers and dangling images (cleanup)
docker system prune
```

---

## 10. Troubleshooting

### Problem: `port is already in use` on startup

**Error message:**
```
ERROR:    [Errno 98] address already in use
```
or
```
Error response from daemon: driver failed programming external connectivity:
Bind for 0.0.0.0:8000 failed: port is already in use
```

**Cause:** Another process is already using port 8000.

**Fix — Find and kill the process:**

```bash
# macOS / Linux
lsof -i :8000
kill -9 <PID>

# Windows (PowerShell)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Alternative fix — Use a different port:**

```bash
# Local
uvicorn main:app --port 8001

# Docker
docker run -p 8001:8000 finance-api
```

---

### Problem: `ModuleNotFoundError: No module named 'fastapi'`

**Cause:** Dependencies are not installed, or you are outside the virtual environment.

**Fix:**

```bash
# Check if venv is active (should see (venv) in prompt)
# If not, activate it:
source venv/bin/activate     # macOS/Linux
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Then reinstall
pip install -r requirements.txt
```

---

### Problem: `uvicorn: command not found`

**Cause:** Uvicorn is not in your PATH, or the virtual environment is not active.

**Fix:**

```bash
# Activate virtual environment first
source venv/bin/activate

# Or run uvicorn via Python module
python -m uvicorn main:app --reload
```

---

### Problem: Docker build fails with `COPY failed: file not found`

**Cause:** You are running `docker build` from the wrong directory.

**Fix:** Make sure you are inside the project folder (where the `Dockerfile` lives):

```bash
cd Lightweight-Finance-API
ls Dockerfile    # should show: Dockerfile
docker build -t finance-api .
```

---

### Problem: `curl: (7) Failed to connect to localhost port 8000`

**Cause:** The server is not running or is running on a different port.

**Fix:**

```bash
# Check if anything is listening on port 8000
curl http://localhost:8000/docs

# Check Docker containers
docker ps

# Check local process
lsof -i :8000    # macOS/Linux
```

---

### Problem: `422 Unprocessable Entity` on all requests

**Cause:** The request body is missing the `Content-Type: application/json` header, or the JSON is malformed.

**Fix:**

```bash
# Always include -H "Content-Type: application/json"
curl -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "source": "Test"}'
```

---

### Problem: `ImportError: cannot import name 'X' from 'models'`

**Cause:** The `models.py` file is missing or has been renamed.

**Fix:**

```bash
ls -la       # check models.py exists
cat models.py  # check it contains Income, Expense, Budget classes
```

---

### Problem: Server starts but data disappears

**Cause:** This is expected behaviour. The API uses in-memory storage — all data is cleared when the server restarts.

**This is not a bug.** It is a documented limitation of v1. Persistent storage (PostgreSQL) is planned for v2.

---

## 11. Cloud Deployment Concepts

The Lightweight Finance API is designed with cloud readiness in mind. Its stateless, containerised architecture maps directly onto the three main cloud deployment patterns.

### Option A — AWS Elastic Container Service (ECS)

```
Developer machine
    │
    ▼ docker build -t finance-api .
Docker image
    │
    ▼ docker push to Amazon ECR (Elastic Container Registry)
Amazon ECR (image registry)
    │
    ▼ ECS task definition references the image
AWS ECS (container orchestration)
    │
    ▼ exposes port 8000 via Application Load Balancer
Public URL: https://api.yourdomain.com
```

**Key AWS services needed:**
- Amazon ECR — stores the Docker image
- Amazon ECS (Fargate) — runs the container without managing servers
- Application Load Balancer — routes traffic and handles HTTPS
- AWS Secrets Manager — stores DATABASE_URL and SECRET_KEY (v2)

### Option B — Azure Container Instances (ACI)

```bash
# Build and push to Azure Container Registry
az acr build --registry myregistry --image finance-api .

# Deploy to Azure Container Instances
az container create \
  --resource-group mygroup \
  --name finance-api \
  --image myregistry.azurecr.io/finance-api:latest \
  --ports 8000 \
  --cpu 0.5 \
  --memory 0.5
```

### Option C — AWS Lambda (Serverless)

FastAPI can run on AWS Lambda using the `Mangum` adapter, which wraps the ASGI app:

```python
# main.py addition for Lambda
from mangum import Mangum

app = FastAPI(...)
# ... routes ...

handler = Mangum(app)    # Lambda invokes this
```

**Why this API is cloud-ready:**

| Cloud Principle | This API |
|----------------|----------|
| Stateless | ✅ No server-side sessions; any instance handles any request |
| Containerised | ✅ Docker image runs on any container runtime |
| Lightweight | ✅ Minimal dependencies — fast cold-start for serverless |
| JSON API | ✅ Standard format for all cloud API gateways |
| Port configurable | ✅ Uvicorn `--port` flag is environment-driven |

> **Important:** Before deploying to cloud, replace in-memory storage with PostgreSQL (v2) to ensure data persists across container restarts.

---

## 12. Deployment Checklist

Use this checklist before any demo or submission to confirm the deployment is complete and working.

### Pre-Deployment

- [ ] Python 3.10+ installed (`python3 --version`)
- [ ] Git installed (`git --version`)
- [ ] Docker Desktop installed and running (`docker info`) ← if using Docker
- [ ] Repository cloned (`git clone ...`)
- [ ] All project files present (`main.py`, `models.py`, `requirements.txt`, `Dockerfile`)

### Local Deployment (Method A)

- [ ] Virtual environment created and activated (`source venv/bin/activate`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Server started (`uvicorn main:app --reload`)
- [ ] Terminal shows `Uvicorn running on http://127.0.0.1:8000`
- [ ] `http://localhost:8000/docs` loads in browser

### Docker Deployment (Method B)

- [ ] Image built without errors (`docker build -t finance-api .`)
- [ ] Container started (`docker run -p 8000:8000 finance-api`)
- [ ] `docker ps` shows container with STATUS `Up`
- [ ] `http://localhost:8000/docs` loads in browser

### Functional Verification

- [ ] Swagger UI shows all 5 endpoints (POST /income, POST /expense, GET /summary, POST /budget, GET /budget-status)
- [ ] `curl http://localhost:8000/summary` returns `{"total_income":0,"total_expense":0,"balance":0}`
- [ ] `POST /income` with valid body returns `{"message": "Income added successfully"}`
- [ ] `POST /income` with `amount: -1` returns HTTP 400
- [ ] `POST /expense` with missing field returns HTTP 422
- [ ] `GET /budget-status` returns correct `budget`, `spent`, and `remaining` after setting budget and adding expenses

### Documentation

- [ ] `http://localhost:8000/docs` is accessible and fully renders all endpoints
- [ ] `http://localhost:8000/redoc` is accessible
- [ ] `http://localhost:8000/openapi.json` returns valid JSON schema

---

## Appendix — requirements.txt

The current `requirements.txt` contains:

```
fastapi
uvicorn
```

**Recommended improvement** — pin versions for reproducibility:

```
fastapi==0.111.0
uvicorn==0.30.1
```

To generate a pinned requirements file from your current environment:

```bash
pip freeze > requirements.txt
```

> **Warning:** `pip freeze` includes all transitive dependencies and may produce a very long file. For production use, pin only your direct dependencies and let pip resolve the rest.

---

*Document ID: DOC-06 | Lightweight Finance API | Yenepoya University | IBM SkillsBuild Project*  
*Version 1.0 | For academic use*
