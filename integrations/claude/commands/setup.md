---
description: Install, configure, and ensure Agent Inspector is running for AI agent security analysis. Handles installation, server startup, provider detection, MCP tools, and IDE connection. Use when user asks to install, setup, configure agent-inspector, ensure it's running, or when starting a new security analysis project.
---

# Agent Inspector Setup

Agent inspector is a tool that provides static analysis, dynamic security checks, debugging and runtime monitoring.

Follow these steps exactly

## FOLLOW THESE EXACT STEPS

First, display this banner:
```
┌─────────────────────────────────────────────┐
│  Verifying Agent Inspector status...        │
└─────────────────────────────────────────────┘
```

**Task Tracking:** Use task management (e.g., TodoWrite) to track steps 1.1-1.2 (and 2.1-2.2 if needed). Mark each in-progress/completed as you go.

### Step 1: Quick Check (MCP + Server)

#### 1.1 Check if MCP Tool is Available

Check if the `get_security_patterns` MCP function is available to you. This is an MCP tool, not a bash command.

#### 1.2 Check if Server is Running

**Only if MCP tool is available from step 1.1**, call:
```
get_security_patterns()
```

**If it returns data** → Server is running → **Setup complete! Skip to Step 7 to report success.**

**If MCP unavailable or server not running** → Continue to Step 2.

### Step 2: Environment Check (only if Step 1 failed)

#### 2.1 Identify Package Manager

Run this single command to check all available package managers:

```bash
echo "uvx:$(command -v uvx 2>/dev/null || echo 'not found')" && echo "pipx:$(command -v pipx 2>/dev/null || echo 'not found')" && echo "pip3:$(command -v pip3 2>/dev/null || echo 'not found')" && echo "pip:$(command -v pip 2>/dev/null || echo 'not found')"
```

Use the **first one found** in this priority order: `uv/uvx` → `pipx` → `pip3` → `pip`

**Remember this choice** - you'll use it for installation in Step 3.

#### 2.2 Check if agent-inspector is Installed

Using the package manager identified above:

**For uv/uvx:**
```bash
uv tool list 2>/dev/null | grep agent-inspector
```

**For pipx:**
```bash
pipx list 2>/dev/null | grep -q agent-inspector && agent-inspector --version
```

**For pip/pip3:**
```bash
pip3 show agent-inspector 2>/dev/null || pip show agent-inspector 2>/dev/null
```

If any returns version info → Package is installed
If all fail → Package is NOT installed

#### 2.3 Display Status Box

After completing checks, display this summary box (don't add any of your own)

```
╔══════════════════════════════════════════════════════════════╗
║                   Agent Inspector Status                     ║
╠══════════════════════════════════════════════════════════════╣
║  Package Manager:  {uvx|pipx|pip3|pip} {✓|✗}                 ║
║  Package Installed: {version or "Not installed"} {✓|✗}      ║
║  MCP Available:    {Yes|No} {✓|✗}                            ║
║  Server Running:   No {✗}                                    ║
╚══════════════════════════════════════════════════════════════╝
```

Use `✓` for success/available and `✗` for failure/unavailable.

Continue to Step 3.

### Step 3: Install or Update `agent-inspector` service

Use the package manager identified in Step 2.1:

**For uv (if uvx available):**
```bash
uv tool install agent-inspector --upgrade
```

**For pipx:**
```bash
pipx upgrade agent-inspector || pipx install agent-inspector
```

**For pip3:**
```bash
pip3 install --upgrade agent-inspector
```

**For pip:**
```bash
pip install --upgrade agent-inspector
```

### Step 4: Detect Provider

If you already know the provider of the project you're about to scan, you can skip this step.

If not, try to identify from the code or do the following steps:

Run
```bash
grep -rl "import anthropic\|from anthropic" . --include="*.py" | head -1
```

If that returns a file → provider is `anthropic`

Otherwise run:
```bash
grep -rl "import openai\|from openai" . --include="*.py" | head -1
```

If that returns a file → provider is `openai`

If neither returns anything → ask user: "Which LLM provider does your agent use: anthropic or openai?"

### Step 5: Start Server

Run the appropriate command based on the package manager from Step 2.1 (use `anthropic` or `openai` based on Step 4):

**For uv/uvx:**
```bash
nohup uvx agent-inspector anthropic > /tmp/agent-inspector.log 2>&1 &
```

**For pipx/pip:**
```bash
nohup agent-inspector anthropic > /tmp/agent-inspector.log 2>&1 &
```

Wait for it to start:
```bash
sleep 5
```

Verify the server is responding:
```bash
curl -s http://localhost:7100/health
```

**Expected response:** `{"status":"ok","service":"live_trace"}`

If the health check fails, check the logs:
```bash
cat /tmp/agent-inspector.log
```

### Step 6: Verify MCP Connection

After confirming the server is running via health check, verify MCP tools work:
```
get_security_patterns()
```

### Step 7: Report Status

After completing setup, always show this status report:

**If everything works:**
```
Agent Inspector Status:
✓ Server running: Yes (http://localhost:7100)
✓ MCP connected: Yes

Ready to scan! Run /agent-inspector:scan to start.
```

**If server running but MCP tools not loaded in Claude Code:**
```
Agent Inspector Status:
✓ Server running: Yes (http://localhost:7100)
⚠ MCP connected: Plugin installed but tools not loaded

Please restart Claude Code for MCP tools to become available.
After restart, run /agent-inspector:setup again to verify.
```

**If server running but MCP connection fails:**
```
Agent Inspector Status:
✓ Server running: Yes (http://localhost:7100)
✗ MCP connected: No (server not responding)

Recommendations:
- Run /mcp to reload the MCP connection
- Check server logs: cat /tmp/agent-inspector.log
```

**If server not running:**
```
Agent Inspector Status:
✗ Server running: No
✗ MCP connected: No

Recommendations:
- Start server manually: agent-inspector {provider}
- Check if port 7100 is in use: lsof -ti:7100
- Verify installation: pip install --upgrade agent-inspector
```

---

## Reference

**CLI syntax** (required):
```
agent-inspector anthropic
agent-inspector openai
```

**Ports:**
- Dashboard: http://localhost:7100
- Proxy: http://localhost:4000

## Available Commands

| Command | Description |
|---------|-------------|
| `/agent-inspector:setup` | Install and configure Agent Inspector |
| `/agent-inspector:scan` | Run static security scan on current workspace |
| `/agent-inspector:scan path/` | Scan specific folder |
| `/agent-inspector:analyze` | Run dynamic runtime analysis |
| `/agent-inspector:correlate` | Cross-reference static + dynamic findings |
| `/agent-inspector:fix REC-XXX` | Fix a specific recommendation |
| `/agent-inspector:fix` | Fix highest priority blocking issue |
| `/agent-inspector:status` | Check dynamic analysis availability |
| `/agent-inspector:gate` | Check production gate status |
| `/agent-inspector:report` | Generate full security report |
| `/agent-inspector:debug` | Debug workflow - explore agents, sessions, events |


## IDE Registration

When starting Agent Inspector work, register the connection:

```
register_ide_connection(
  ide_type="claude-code",
  agent_workflow_id="{project_name}",
  workspace_path="{full_path}",
  model="{your_model}"  # e.g., "claude-sonnet-4"
)
```

Send ONE heartbeat at the start of work:
```
ide_heartbeat(connection_id="{id}", is_developing=true)
```

### Model Name Mapping

Use your actual model identifier:

| AI Model | Model Value |
|----------|-------------|
| Claude Opus 4.5 | `claude-opus-4-5-20251101` |
| Claude Sonnet 4 | `claude-sonnet-4-20250514` |
| Claude Sonnet 3.5 | `claude-3-5-sonnet-20241022` |
| GPT-4o | `gpt-4o` |
| GPT-4 Turbo | `gpt-4-turbo` |
| Other models | Use your actual model identifier |

Check your system prompt for the exact model ID (e.g., "You are powered by claude-opus-4-5-20251101").

## Derive agent_workflow_id

Auto-derive from (priority order):
1. Git remote: `github.com/acme/my-agent.git` -> `my-agent`
2. Package name: `pyproject.toml` or `package.json`
3. Folder name: `/projects/my-bot` -> `my-bot`

**Do NOT ask the user for agent_workflow_id - derive it automatically.**

## Dynamic Analysis Setup

To capture runtime behavior, configure your agent's base_url:

```python
# OpenAI
client = OpenAI(base_url=f"http://localhost:4000/agent-workflow/{AGENT_WORKFLOW_ID}")

# Anthropic
client = Anthropic(base_url=f"http://localhost:4000/agent-workflow/{AGENT_WORKFLOW_ID}")
```

Use the **same agent_workflow_id** for static and dynamic analysis to get unified results.

## Dashboard URLs

| Page | URL |
|------|-----|
| Overview | http://localhost:7100/agent-workflow/{id} |
| Static Analysis | http://localhost:7100/agent-workflow/{id}/static-analysis |
| Dynamic Analysis | http://localhost:7100/agent-workflow/{id}/dynamic-analysis |
| Recommendations | http://localhost:7100/agent-workflow/{id}/recommendations |
| Reports | http://localhost:7100/agent-workflow/{id}/reports |
| Sessions | http://localhost:7100/agent-workflow/{id}/sessions |


## Troubleshooting

| Problem | Solution |
|---------|----------|
| Command not found | Re-install using: `uv tool install agent-inspector` or `pipx install agent-inspector` or `pip install agent-inspector` |
| Module not found | Reinstall: `pip install --force-reinstall agent-inspector` or `pipx install agent-inspector --force` |
| MCP tools unavailable | Reload Claude Code, verify server running |
| Connection refused | Server not running - check with `curl -s http://localhost:7100/health`, restart with `agent-inspector {provider}` |
| Port 7100 in use | Kill existing process: `lsof -ti:7100 \| xargs kill` |
| Port 4000 in use | Kill existing process: `lsof -ti:4000 \| xargs kill` |
| Permission denied | Check pip/python environment is activated |

## Common Error Messages

**If installation fails:**
```
ERROR: Failed to install agent-inspector.

Please run manually (try in order):
  uvx install agent-inspector
  pipx install agent-inspector
  pip install agent-inspector

If permission issues with pip, try:
  pip install --user agent-inspector
```

**If server won't start:**
```
ERROR: Agent Inspector failed to start.

Check the log file:
  cat /tmp/agent-inspector.log

Common issues:
1. Port already in use - kill existing process
2. Missing dependencies - reinstall package
3. Python version - requires Python 3.9+

To start manually in a terminal:
  agent-inspector {provider}
```

**If MCP connection fails after startup:**
```
ERROR: Server started but MCP connection failed.

The server is running but MCP tools are not available.

Try:
1. Wait a few more seconds for full initialization
2. Reload Claude Code: /mcp to verify connection
3. Check server logs: cat /tmp/agent-inspector.log
```
