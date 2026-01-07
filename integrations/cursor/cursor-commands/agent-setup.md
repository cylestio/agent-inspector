# Agent Inspector Setup

Install, configure, upgrade, and ensure Agent Inspector is running for AI agent security analysis.

## Instructions

### Step 1: Quick Check (Server Status)

First, display this banner:
```
┌─────────────────────────────────────────────┐
│  Verifying Agent Inspector status...        │
└─────────────────────────────────────────────┘
```

Check if the server is running:
```bash
curl -s http://localhost:7100/health
```

**If returns `{"status":"ok"}`** → Server is running → **Continue to Step 1.2 to check for updates.**

**If connection refused or no response** → Continue to Step 2.

### Step 1.2: Check for Updates (even if server is running)

Always ensure the latest version is installed:

```bash
# Try in order until one works:
uv tool install agent-inspector --upgrade 2>/dev/null || \
pipx upgrade agent-inspector 2>/dev/null || \
pip install --upgrade agent-inspector 2>/dev/null || \
echo "Upgrade check complete"
```

After upgrade, **skip to Step 6 to report success.**

### Step 2: Check Installation

#### 2.1 Identify Package Manager

Run this command to check available package managers:
```bash
echo "pip:$(command -v pip 2>/dev/null || echo 'not found')"
```

**Note:** This guide uses pip (virtual environment). For global install options (uvx, pipx), see CLI Reference below.

#### 2.2 Check if Installed

```bash
pip show agent-inspector 2>/dev/null | grep Version
```

If version shown → Package is installed → Skip to Step 4
If no output → Package is NOT installed → Continue to Step 3

#### 2.3 Display Status

```
╔══════════════════════════════════════════════════════════════╗
║                   Agent Inspector Status                     ║
╠══════════════════════════════════════════════════════════════╣
║  Package Installed: {version or "Not installed"} {✓|✗}      ║
║  Server Running:   {Yes|No} {✓|✗}                            ║
╚══════════════════════════════════════════════════════════════╝
```

### Step 3: Install or Upgrade

**If not installed:**
```bash
pip install agent-inspector
```

**If already installed, upgrade to latest:**
```bash
pip install --upgrade agent-inspector
```

### Step 4: Detect Provider

Check the codebase for LLM provider:

```bash
grep -rl "import anthropic\|from anthropic" . --include="*.py" | head -1
```

If returns a file → provider is `anthropic`

Otherwise:
```bash
grep -rl "import openai\|from openai" . --include="*.py" | head -1
```

If returns a file → provider is `openai`

If neither → ask user: "Which LLM provider does your agent use: anthropic or openai?"

### Step 5: Start Server

Start the server (use the detected provider):
```bash
nohup agent-inspector anthropic > /tmp/agent-inspector.log 2>&1 &
```

Or for OpenAI: `agent-inspector openai`

Wait and verify:
```bash
sleep 3 && curl -s http://localhost:7100/health
```

**Expected response:** `{"status":"ok","service":"live_trace"}`

If failed, check logs:
```bash
cat /tmp/agent-inspector.log
```

### Step 6: Report Status

**If server running:**
```
✓ Agent Inspector is running!

Dashboard: http://localhost:7100
Proxy: http://localhost:4000

Ready to scan! Run /agent-scan to start.
```

**If server failed to start:**
```
✗ Agent Inspector failed to start.

Check logs: cat /tmp/agent-inspector.log

Common issues:
- Port 7100 in use: lsof -ti:7100 | xargs kill
- Port 4000 in use: lsof -ti:4000 | xargs kill
- Reinstall: pip install --upgrade agent-inspector
```

---

## CLI Reference

**Basic commands:**
```bash
agent-inspector anthropic    # For Anthropic/Claude agents
agent-inspector openai       # For OpenAI agents
```

**Ports (default):**
- Proxy: http://localhost:4000
- Dashboard: http://localhost:7100

**CLI Options:**

| Flag | Description |
|------|-------------|
| `--port`, `-p` | Override proxy port (default: 4000) |
| `--ui-port` | Override dashboard port (default: 7100) |
| `--base-url` | Override LLM provider base URL |
| `--use-local-storage` | Enable persistent SQLite storage |
| `--local-storage-path` | Custom database path |
| `--log-level` | DEBUG, INFO, WARNING, ERROR, CRITICAL |
| `--no-presidio` | Disable PII detection |

**Examples:**
```bash
# Use custom ports
agent-inspector anthropic --port 5000 --ui-port 8100

# Point to a different LLM endpoint (e.g., Azure OpenAI, local model)
agent-inspector openai --base-url https://my-azure-openai.openai.azure.com

# Enable debug logging with persistent storage
agent-inspector anthropic --use-local-storage --log-level DEBUG
```

---

## Configure Your Agent

To capture runtime behavior, configure your agent's base_url:

```python
# OpenAI
client = OpenAI(base_url="http://localhost:4000/agent-workflow/{agent_workflow_id}")

# Anthropic
client = Anthropic(base_url="http://localhost:4000/agent-workflow/{agent_workflow_id}")
```

Replace `{agent_workflow_id}` with your project name (derived from git repo, package name, or folder).

---

## Available Commands

| Command | Description |
|---------|-------------|
| `/agent-setup` | Install, configure, start Agent Inspector |
| `/agent-scan` | Run static security scan |
| `/agent-analyze` | Run dynamic runtime analysis |
| `/agent-fix REC-XXX` | Fix a specific recommendation |
| `/agent-correlate` | Cross-reference static + dynamic findings |
| `/agent-gate` | Check production readiness |
| `/agent-report` | Generate security report |
| `/agent-status` | Check dynamic analysis availability |

