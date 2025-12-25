---
description: Install, configure, and ensure Agent Inspector is running for AI agent security analysis. Handles installation, server startup, provider detection, MCP tools, and IDE connection. Use when user asks to install, setup, configure agent-inspector, ensure it's running, or when starting a new security analysis project.
---

# Agent Inspector Setup

Agent Inspector is a security analysis server that provides MCP tools for scanning AI agent code.

Follow these steps exactly

## FOLLOW THESE EXACT STEPS

### Step 1: Try MCP Tool

Call this MCP tool to check if server is running:
```
get_security_patterns()
```

**If it returns data** → Server is running. Done. Proceed with your task.

**If it fails** → Continue to Step 2.

### Step 2: Install or Update

Always run this to ensure latest version:
```bash
pip install --upgrade agent-inspector
```

### Step 3: Detect Provider

If you already know the provider of the project you're about to scan, you can skip this step.

If not, try to indentify from the code or do the following steps:

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

### Step 4: Start Server

Run exactly (use `anthropic` or `openai` based on Step 3):
```bash
nohup agent-inspector anthropic > /tmp/agent-inspector.log 2>&1 &
```

Wait for it to start:
```bash
sleep 5
```

### Step 5: Verify with MCP

Call the MCP tool again:
```
get_security_patterns()
```

### Step 6: Report Status

After completing setup, always show this status report:

**If everything works:**
```
Agent Inspector Status:
✓ Server running: Yes (http://localhost:7100)
✓ MCP connected: Yes

Ready to scan! Run /agent-inspector:scan to start.
```

**If server running but MCP fails:**
```
Agent Inspector Status:
✓ Server running: Yes (http://localhost:7100)
✗ MCP connected: No

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

## MCP Tools Available (20 total)

### Analysis Tools
| Tool | Description |
|------|-------------|
| `get_security_patterns` | Get OWASP LLM Top 10 patterns for analysis |
| `create_analysis_session` | Start session for agent workflow |
| `store_finding` | Record a security finding |
| `complete_analysis_session` | Finalize session and calculate risk score |
| `get_findings` | Retrieve stored findings |
| `update_finding_status` | Mark finding as FIXED or IGNORED |

### Knowledge Tools
| Tool | Description |
|------|-------------|
| `get_owasp_control` | Get specific OWASP control details (LLM01-LLM10) |
| `get_fix_template` | Get remediation template for a finding type |

### Agent Workflow Lifecycle Tools
| Tool | Description |
|------|-------------|
| `get_agent_workflow_state` | Check what analysis exists (static/dynamic/both) |
| `get_tool_usage_summary` | Get tool usage patterns from dynamic sessions |
| `get_agent_workflow_correlation` | Correlate static findings with dynamic runtime |

### Agent Discovery Tools
| Tool | Description |
|------|-------------|
| `get_agents` | List agents (filter by agent_workflow_id or "unlinked") |
| `update_agent_info` | Link agents to agent workflows, set display names |

### Workflow Query Tools
| Tool | Description |
|------|-------------|
| `get_workflow_agents` | List agents with system prompts, session counts, last 10 sessions |
| `get_workflow_sessions` | Query sessions with filters (agent_id, status) and pagination |
| `get_session_events` | Get events in a session with type filtering and pagination |

### IDE Connection Tools
| Tool | Description |
|------|-------------|
| `register_ide_connection` | Register your IDE as connected |
| `ide_heartbeat` | Keep connection alive, signal active development |
| `disconnect_ide` | Disconnect IDE from Agent Inspector |
| `get_ide_connection_status` | Check current IDE connection status |

## IDE Registration

When starting Agent Inspector work, register the connection:

```
register_ide_connection(
  ide_type="claude-code",
  agent_workflow_id="{project_name}",
  workspace_path="{full_path}",
  model="{your_model}"  // e.g., "claude-sonnet-4"
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

## The 7 Security Categories

| # | Category | OWASP | Focus |
|---|----------|-------|-------|
| 1 | PROMPT | LLM01 | Injection, jailbreak |
| 2 | OUTPUT | LLM02 | XSS, downstream injection |
| 3 | TOOL | LLM07/08 | Dangerous tools |
| 4 | DATA | LLM06 | Secrets, PII |
| 5 | MEMORY | - | RAG, context security |
| 6 | SUPPLY | LLM05 | Dependencies |
| 7 | BEHAVIOR | LLM08/09 | Excessive agency |

## Recommendation Lifecycle

```
PENDING -> FIXING -> FIXED -> VERIFIED
              |
         DISMISSED/IGNORED
```

## Dashboard URLs

| Page | URL |
|------|-----|
| Overview | http://localhost:7100/agent-workflow/{id} |
| Static Analysis | http://localhost:7100/agent-workflow/{id}/static-analysis |
| Dynamic Analysis | http://localhost:7100/agent-workflow/{id}/dynamic-analysis |
| Recommendations | http://localhost:7100/agent-workflow/{id}/recommendations |
| Reports | http://localhost:7100/agent-workflow/{id}/reports |
| Sessions | http://localhost:7100/agent-workflow/{id}/sessions |

## Dynamic Analysis - 4 Check Categories

| # | Category | Focus |
|---|----------|-------|
| 1 | Resource Management | Token/tool bounds, variance, cost |
| 2 | Environment | Model pinning, tool coverage |
| 3 | Behavioral | Stability, predictability, outliers |
| 4 | Data | PII detection at runtime |

## Correlation States

| State | Meaning | Priority |
|-------|---------|----------|
| VALIDATED | Static issue confirmed at runtime | Highest - FIX FIRST! |
| UNEXERCISED | Code path never executed | Test gap |
| THEORETICAL | Static issue, safe at runtime | Lower priority |
| RUNTIME_ONLY | Found only during runtime | Different fix approach |

## Gate Status

- **BLOCKED**: CRITICAL or HIGH issues remain open → can't ship
- **OPEN**: All blocking issues resolved → ready for production

## Setup Checklist

When setting up Agent Inspector for a new project:

- [ ] Ran `pip install agent-inspector`
- [ ] Started server: `agent-inspector anthropic` or `agent-inspector openai`
- [ ] Verified dashboard at http://localhost:7100
- [ ] Registered IDE connection
- [ ] (For dynamic analysis) Updated agent code with `base_url` pointing to proxy
- [ ] Ran first security scan

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Command not found | Re-run: `pip install agent-inspector` |
| Module not found | Reinstall: `pip install --force-reinstall agent-inspector` |
| MCP tools unavailable | Reload Claude Code, verify server running |
| Connection refused | Server not running - restart with `agent-inspector {provider}` |
| Port 7100 in use | Kill existing process: `lsof -ti:7100 \| xargs kill` |
| Port 4000 in use | Kill existing process: `lsof -ti:4000 \| xargs kill` |
| Permission denied | Check pip/python environment is activated |

## Common Error Messages

**If installation fails:**
```
ERROR: Failed to install agent-inspector.

Please run manually:
  pip install agent-inspector

If permission issues, try:
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
