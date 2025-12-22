# Agent Inspector Templates

Integration templates for AI coding assistants (Claude Code & Cursor).

## Quick Start

### 1. Start Agent Inspector

```bash
uvx cylestio-perimeter run --config path/to/config.yaml
```

**Default ports:**
- Proxy: `http://localhost:4000` (point your agent here)
- Dashboard/MCP: `http://localhost:7100`

### 2. Connect Your IDE

#### Claude Code

```bash
claude mcp add --transport http agent-inspector http://localhost:7100/mcp
```

#### Cursor

Create `.cursor/mcp.json` in your project (or `~/.cursor/mcp.json` globally):

```json
{
  "mcpServers": {
    "agent-inspector": {
      "url": "http://localhost:7100/mcp"
    }
  }
}
```

Then restart Cursor and approve the MCP server when prompted.

### 3. Verify

- **Claude Code:** Run `/mcp` - should show 17+ tools
- **Cursor:** Ask "What MCP tools are available?"

---

## Available MCP Tools (17+)

### Analysis Tools
| Tool | Purpose |
|------|---------|
| `get_security_patterns` | OWASP LLM Top 10 patterns |
| `create_analysis_session` | Start analysis session |
| `store_finding` | Record security finding |
| `complete_analysis_session` | Finalize with risk score |
| `get_findings` | Retrieve findings |
| `update_finding_status` | Mark FIXED/IGNORED |

### Knowledge Tools
| Tool | Purpose |
|------|---------|
| `get_owasp_control` | OWASP control details (LLM01-LLM10) |
| `get_fix_template` | Remediation templates |

### Recommendation Tools
| Tool | Purpose |
|------|---------|
| `get_recommendations` | List recommendations for workflow |
| `get_recommendation_detail` | Get full details for a recommendation |
| `start_fix` | Mark recommendation as FIXING |
| `complete_fix` | Mark recommendation as FIXED |
| `dismiss_recommendation` | Dismiss with documented reason |

### Agent Workflow Lifecycle Tools
| Tool | Purpose |
|------|---------|
| `get_agent_workflow_state` | Check static/dynamic data exists |
| `get_tool_usage_summary` | Runtime tool usage patterns |
| `get_agent_workflow_correlation` | Correlate static ↔ dynamic |
| `get_gate_status` | Check if production is blocked |

### Agent Discovery Tools
| Tool | Purpose |
|------|---------|
| `get_agents` | List agents |
| `update_agent_info` | Link/name agents |

### IDE Connection Tools
| Tool | Purpose |
|------|---------|
| `register_ide_connection` | Register IDE as connected |
| `ide_heartbeat` | Keep connection alive |
| `disconnect_ide` | Disconnect IDE |
| `get_ide_connection_status` | Check connection status |

---

## Usage

### Commands

| Command | What It Does |
|---------|--------------|
| `/scan` | Run security scan on current workspace |
| `/scan path/` | Scan specific folder |
| `/fix REC-XXX` | Fix a specific recommendation |
| `/fix` | Fix highest priority blocking issue |

### Run a Security Scan

Ask your AI assistant:
> "Run a security scan on this codebase"

The scan evaluates your agent against **7 security categories**:
1. **PROMPT** - Injection, jailbreak (LLM01)
2. **OUTPUT** - Insecure output handling (LLM02)
3. **TOOL** - Dangerous tools (LLM07/08)
4. **DATA** - Secrets, PII exposure (LLM06)
5. **MEMORY** - RAG/context security
6. **SUPPLY** - Dependencies (LLM05)
7. **BEHAVIOR** - Excessive agency (LLM08/09)

### Fix Security Issues

Each finding gets a recommendation (REC-XXX). Fix them with:
> "/fix REC-001"

The AI will:
1. Read and understand the vulnerability
2. Analyze your codebase patterns
3. Apply a contextual, intelligent fix
4. Track the fix in the audit trail

### Test Your Agent (Dynamic Analysis)

Configure your agent to use the proxy:

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:4000/agent-workflow/my-project")

# or Anthropic
from anthropic import Anthropic
client = Anthropic(base_url="http://localhost:4000/agent-workflow/my-project")
```

### View Results

| URL | What It Shows |
|-----|---------------|
| `http://localhost:7100` | Dashboard home |
| `http://localhost:7100/agent-workflow/{id}/static-analysis` | Static scan findings |
| `http://localhost:7100/agent-workflow/{id}/recommendations` | All recommendations |
| `http://localhost:7100/agent-workflow/{id}/sessions` | Dynamic sessions |

---

## Optional: Install Rules/Skills

### Cursor Rules

```bash
mkdir -p .cursor/rules
cp templates/cursor-rules/agent-inspector.mdc .cursor/rules/
```

### Claude Code

**Quick setup (recommended):**
```bash
cp templates/claude-code/CLAUDE.md ./CLAUDE.md
```

**Detailed skills (optional):**
```bash
mkdir -p .claude/skills
cp templates/skills/static-analysis/SKILL.md .claude/skills/
cp templates/skills/dynamic-analysis/SKILL.md .claude/skills/
cp templates/skills/auto-fix/SKILL.md .claude/skills/
```

---

## Templates Directory

```
templates/
├── README.md                    # This file (human guide)
├── AGENT_INSPECTOR_SETUP.md     # AI agent setup instructions
├── skills/                      # Claude Code skills (detailed)
│   ├── static-analysis/SKILL.md  # Complete /scan workflow
│   ├── dynamic-analysis/SKILL.md # Runtime tracing setup
│   └── auto-fix/SKILL.md         # Complete /fix workflow
├── cursor-rules/                # Cursor rules
│   ├── .cursorrules
│   └── agent-inspector.mdc       # Main Cursor rule file
└── claude-code/                 # Claude Code templates
    └── CLAUDE.md                 # Project-level skills file
```

### Which File Goes Where?

| IDE | File | Destination |
|-----|------|-------------|
| Cursor | `agent-inspector.mdc` | `.cursor/rules/agent-inspector.mdc` |
| Claude Code | `CLAUDE.md` | `./CLAUDE.md` (project root) |
| Claude Code | `skills/*.md` | `.claude/skills/` (optional, for detailed guidance) |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| MCP server not found | Ensure server is running on port 7100 |
| Connection refused | Check `curl http://localhost:4000/health` |
| Tools not showing | Restart IDE after adding mcp.json |

---

## Ports Reference

| Port | Service |
|------|---------|
| 4000 | Proxy (LLM API routing) |
| 7100 | Dashboard + MCP endpoint |
