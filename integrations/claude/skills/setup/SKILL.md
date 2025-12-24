---
name: agent-inspector-setup
description: Install and configure Agent Inspector for AI agent security analysis. Set up MCP tools, IDE connection, and proxy configuration. Use when user asks to install, setup, configure agent-inspector, or when starting a new security analysis project.
---

# Agent Inspector Setup

This skill helps you install and configure Agent Inspector for AI agent security analysis.

## Quick Start

1. **Install**: `pip install agent-inspector`
2. **Start**: `agent-inspector anthropic` (or `agent-inspector openai`)
3. **Verify**: Dashboard at http://localhost:7100

## Available Commands

| Command | Description |
|---------|-------------|
| `/agent-inspector:scan` | Run static security scan on current workspace |
| `/agent-inspector:scan path/` | Scan specific folder |
| `/agent-inspector:analyze` | Run dynamic runtime analysis |
| `/agent-inspector:correlate` | Cross-reference static + dynamic findings |
| `/agent-inspector:fix REC-XXX` | Fix a specific recommendation |
| `/agent-inspector:fix` | Fix highest priority blocking issue |
| `/agent-inspector:status` | Check dynamic analysis availability |
| `/agent-inspector:gate` | Check production gate status |
| `/agent-inspector:report` | Generate full security report |

## MCP Tools Available (17 total)

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
