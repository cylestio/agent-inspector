# Agent Inspector - Installation Guide

> **Execute ALL steps. Display the welcome message at the end.**

---

## QUICK REFERENCE

```
COMMANDS:
  ✅ agent-inspector anthropic    (correct)
  ✅ agent-inspector openai       (correct)
  ❌ agent-inspector serve        (WRONG - does not exist!)

URLS:
  ✅ http://localhost:4000/agent-workflow/{project-name}      (Anthropic)
  ✅ http://localhost:4000/agent-workflow/{project-name}/v1   (OpenAI)
  ❌ http://localhost:4000                                     (won't track sessions)

PORTS:
  4000 = LLM Proxy (for agent's base_url)
  7100 = Dashboard + MCP Server
```

---

## STEP 1: INSTALL PACKAGE

```bash
cd {PROJECT_FOLDER}
python -m venv venv
source venv/bin/activate
pip install agent-inspector
```

---

## STEP 2: CREATE CONFIG FILES

### 2.1 Create `.cursor/mcp.json`

```bash
mkdir -p .cursor
```

Write this file:
```json
{
  "mcpServers": {
    "agent-inspector": {
      "type": "streamable-http",
      "url": "http://localhost:7100/mcp"
    }
  }
}
```

### 2.2 Create `.cursor/rules/agent-inspector.mdc`

```bash
mkdir -p .cursor/rules
```

Write this file:
```markdown
---
description: Agent Inspector security analysis
globs: ["**/*.py", "**/*.ts", "**/*.js"]
---

# Agent Inspector

Commands: /agent-scan, /agent-analyze, /agent-fix, /agent-gate, /agent-report
Dashboard: http://localhost:7100
```

### 2.3 Copy slash commands

```bash
mkdir -p .cursor/commands
```

**IMPORTANT: You must READ and COPY the FULL content of each file!**

For each of these 7 files:
1. READ the source file from `integrations/cursor/cursor-commands/`
2. WRITE the FULL content to `.cursor/commands/`

| Source | Destination |
|--------|-------------|
| `integrations/cursor/cursor-commands/agent-scan.md` | `.cursor/commands/agent-scan.md` |
| `integrations/cursor/cursor-commands/agent-fix.md` | `.cursor/commands/agent-fix.md` |
| `integrations/cursor/cursor-commands/agent-analyze.md` | `.cursor/commands/agent-analyze.md` |
| `integrations/cursor/cursor-commands/agent-correlate.md` | `.cursor/commands/agent-correlate.md` |
| `integrations/cursor/cursor-commands/agent-gate.md` | `.cursor/commands/agent-gate.md` |
| `integrations/cursor/cursor-commands/agent-report.md` | `.cursor/commands/agent-report.md` |
| `integrations/cursor/cursor-commands/agent-status.md` | `.cursor/commands/agent-status.md` |

**DO NOT create empty files or write minimal content!**
Each file contains 70-140 lines of detailed instructions. Copy ALL of it.

---

## STEP 3: EDIT AGENT CODE (REQUIRED!)

**You must EDIT the Python files that create LLM clients.**

Find files with `Anthropic(` or `OpenAI(`:
```bash
grep -rn "Anthropic\|OpenAI" --include="*.py"
```

**Add `base_url` parameter:**

```python
# BEFORE:
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# AFTER (for project named "my-agent"):
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    base_url="http://localhost:4000/agent-workflow/my-agent"
)
```

For OpenAI, add `/v1` at the end:
```python
base_url="http://localhost:4000/agent-workflow/my-agent/v1"
```

**Verify your edit:**
```bash
grep -rn "base_url.*localhost:4000" --include="*.py"
```
If no results → you didn't edit the file!

---

## STEP 4: START SERVER

```bash
source venv/bin/activate
agent-inspector anthropic
```

Or for OpenAI: `agent-inspector openai`

**Keep it running in a terminal.**

---

## STEP 5: RELOAD MCP SERVERS

Tell user:
> Go to **Cursor Settings → Tools & MCP** → Click the reload/refresh button on MCP servers

---

## STEP 6: DISPLAY WELCOME MESSAGE (REQUIRED!)

**Copy this EXACT banner (spells CYLESTIO):**

```
 ██████╗██╗   ██╗██╗     ███████╗███████╗████████╗██╗ ██████╗ 
██╔════╝╚██╗ ██╔╝██║     ██╔════╝██╔════╝╚══██╔══╝██║██╔═══██╗
██║      ╚████╔╝ ██║     █████╗  ███████╗   ██║   ██║██║   ██║
██║       ╚██╔╝  ██║     ██╔══╝  ╚════██║   ██║   ██║██║   ██║
╚██████╗   ██║   ███████╗███████╗███████║   ██║   ██║╚██████╔╝
 ╚═════╝   ╚═╝   ╚══════╝╚══════╝╚══════╝   ╚═╝   ╚═╝ ╚═════╝ 
                    AGENT INSPECTOR
```

**Then show:**

✅ **Installation Complete!**

| Command | Description |
|---------|-------------|
| `/agent-scan` | Run security scan |
| `/agent-analyze` | Runtime analysis |
| `/agent-fix REC-XXX` | Fix an issue |
| `/agent-gate` | Check production readiness |
| `/agent-report` | Generate report |

**Quick Start:**
1. Reload MCP servers (Settings → Tools & MCP → Reload)
2. Type `/agent-scan` to scan your code
3. Visit http://localhost:7100 for dashboard

---

## CHECKLIST

Before finishing, verify:

- [ ] Package installed
- [ ] `.cursor/mcp.json` created
- [ ] `.cursor/rules/agent-inspector.mdc` created  
- [ ] Slash commands copied with FULL content (each file 70-140 lines, not empty!)
- [ ] **Agent code EDITED with base_url** (grep shows results)
- [ ] Server started (`agent-inspector anthropic`)
- [ ] **Welcome message displayed with CYLESTIO banner**

---

## TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| `'serve' is not one of 'openai', 'anthropic'` | Use `agent-inspector anthropic` not `serve` |
| Sessions not captured | Edit agent code to add `base_url` (Step 3) |
| MCP tools unavailable | Reload MCP servers in Settings, check server is running |

---

## DON'T DO THESE

❌ `agent-inspector serve` → WRONG command  
❌ `base_url="http://localhost:4000"` → Missing workflow ID  
❌ Creating your own ASCII art → Copy the exact CYLESTIO banner  
❌ Mentioning base_url without editing files → Actually edit the code  
❌ Finishing without welcome message → Always show it  
❌ Creating empty/minimal slash command files → Copy FULL content from source files
