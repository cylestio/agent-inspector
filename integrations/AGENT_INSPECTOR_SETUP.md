# Agent Inspector - Installation Guide for AI Assistants

> **Purpose:** Complete guide for Cursor IDE to install and configure Agent Inspector.
> 
> **Your job:** Execute EVERY step. Be smart. Handle edge cases. Succeed 100%.

---

## 🚨 MANDATORY EXECUTION SEQUENCE - READ THIS FIRST!

**You MUST complete these steps IN ORDER. Do NOT skip any step.**

```
STEP 1-7:  Setup (venv, pip install, config files, etc.)
STEP 8:    ⚠️ START THE SERVER ← MANDATORY - Server must be running!
STEP 8.5:  Add auto-startup (recommended)
STEP 9:    Tell user to reload IDE
STEP 10:   Register IDE connection
STEP 11:   Run first scan (if code exists)
STEP 12:   Verify completion
STEP 13:   ⚠️ DISPLAY WELCOME MESSAGE ← MANDATORY - Final step!
```

### ⛔ YOU ARE NOT DONE UNTIL:
1. ✅ Agent Inspector server is RUNNING (Step 8)
2. ✅ User has seen the WELCOME MESSAGE with ASCII banner (Step 13)

**If you finish without showing the welcome message, YOU HAVE FAILED.**

### ⚠️ CRITICAL COMMANDS - MEMORIZE THESE:

| Action | ✅ CORRECT Command | ❌ WRONG (will fail) |
|--------|-------------------|---------------------|
| Start server | `agent-inspector anthropic` | `agent-inspector serve` |
| Start server | `agent-inspector openai` | `agent-inspector start` |

**There is NO `serve`, `start`, or `run` subcommand!**

---

## ⚠️ COMMANDS THAT WILL HANG - NEVER RUN

```bash
# ❌ NEVER - will freeze your session
curl http://localhost:...
wget http://...
nc -z localhost ...
ping ...
python -i ...
```

---

## STEP 1: UNDERSTAND THE ENVIRONMENT

### 1.1 Determine Agent Project Location

Ask yourself: Where is the agent code the user wants to analyze?

**Typical scenario:** Agent Inspector is installed directly in the customer's agent repository. The agent being secured is the one where you're installing Agent Inspector.

- If user said "this project" or "this agent" → use current workspace root
- If user specified a path → use that path
- If unclear → ask: "Which folder contains your agent code?"

Store this as `{AGENT_PROJECT_FOLDER}`.

**Examples:**
- Standalone agent: `/home/user/my-sales-bot/` → Agent Inspector analyzes "my-sales-bot"
- Monorepo: `/home/user/company-ai/agents/support-bot/` → Agent Inspector analyzes "support-bot"

> ⚠️ **CRITICAL: Open the agent project folder directly in Cursor!**
>
> Cursor only detects `.cursor/rules` and `.cursor/commands` at the **workspace root**. If you open a parent folder containing multiple projects, the `.cursor` directory inside subfolders will NOT be detected.
>
> ❌ **Wrong:** Open `/home/user/all-my-projects/` → `.cursor` in `my-agent/` subfolder is ignored
> ✅ **Correct:** Open `/home/user/all-my-projects/my-agent/` directly

### 1.2 Check if Inside cylestio-perimeter Repo (Local Dev Mode)

```bash
# Check for cylestio-perimeter pyproject.toml in parent directories
ls ../../pyproject.toml 2>/dev/null | head -1
# OR
ls ../../../pyproject.toml 2>/dev/null | head -1
```

If found and contains "cylestio-perimeter" → **Local Dev Mode**
Otherwise → **Production Mode**

### 1.3 Check/Create Virtual Environment

```bash
# Check if venv exists
ls {AGENT_PROJECT_FOLDER}/venv/bin/activate 2>/dev/null && echo "VENV_EXISTS" || echo "NO_VENV"
```

**If NO_VENV:**
```bash
cd {AGENT_PROJECT_FOLDER}
python -m venv venv
```

**Activate venv for subsequent commands:**
```bash
source {AGENT_PROJECT_FOLDER}/venv/bin/activate
```

---

## STEP 2: INSTALL PACKAGE

**Always run installation** - `pip install` is idempotent and will update if needed.

### Production Mode:
```bash
source {AGENT_PROJECT_FOLDER}/venv/bin/activate
pip install agent-inspector
```

### Local Dev Mode:
```bash
source {AGENT_PROJECT_FOLDER}/venv/bin/activate
# Adjust path depth based on agent location relative to repo root:
# - repo/temp/agents/my-agent/ → pip install ../../../
# - repo/examples/my-agent/ → pip install ../../
pip install {RELATIVE_PATH_TO_REPO_ROOT}
```

**Verify success:** Output must show "Successfully installed" or "Requirement already satisfied".

---

## STEP 3: VERIFY CURSOR VERSION

**Requirement:** Cursor 1.6 or later is required for slash commands.

> **Note:** Custom slash commands are a beta feature in Cursor. If commands don't appear, see Troubleshooting at the end of this guide.

Verify the user has Cursor 1.6+:
- Help → About Cursor → Check version number
- If older than 1.6, user must update Cursor first

---

## STEP 4: CONFIGURE MCP CONNECTION

### Configure `.cursor/mcp.json`

**First, check if file exists:**
```bash
cat {AGENT_PROJECT_FOLDER}/.cursor/mcp.json 2>/dev/null || echo "FILE_NOT_FOUND"
```

**If FILE_NOT_FOUND:** Create new file:
```bash
mkdir -p {AGENT_PROJECT_FOLDER}/.cursor
```
Then write:
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

**If file EXISTS:** Parse JSON and check if `agent-inspector` entry exists:
- If `agent-inspector` exists with correct config → skip
- If `agent-inspector` exists with wrong config → update the entry
- If `agent-inspector` missing → add it while PRESERVING other servers

**Example merge:**
```json
{
  "mcpServers": {
    "existing-server": { "command": "...", "args": ["..."] },
    "agent-inspector": {
      "type": "streamable-http",
      "url": "http://localhost:7100/mcp"
    }
  }
}
```

---

## STEP 5: INSTALL CURSOR RULES FILE

### Create `.cursor/rules/agent-inspector.mdc`

```bash
mkdir -p {AGENT_PROJECT_FOLDER}/.cursor/rules
```

**Copy from package template** if available:
- Look for: `integrations/cursor/cursor-rules/agent-inspector.mdc` in the installed package or repo
- Copy to: `{AGENT_PROJECT_FOLDER}/.cursor/rules/agent-inspector.mdc`

If template not found, create the rules file with this minimal content:

```markdown
---
description: Agent Inspector - AI Agent Security Analysis (scan, analyze, fix, correlate)
globs: ["**/*.py", "**/*.ts", "**/*.js"]
---

# Agent Inspector Integration

**MCP Server:** `http://localhost:7100/mcp`
**Dashboard:** `http://localhost:7100`

## Commands

- `/agent-scan` - Run static security scan on current workspace
- `/agent-scan path/` - Scan specific folder
- `/agent-analyze` - Run dynamic runtime analysis
- `/agent-correlate` - Correlate static findings with runtime data
- `/agent-fix REC-XXX` - Fix a specific recommendation
- `/agent-fix` - Fix highest priority blocking issue
- `/agent-status` - Get dynamic analysis status
- `/agent-gate` - Check production gate status
- `/agent-report` - Generate security assessment report (returns markdown)

## Static Analysis - 7 Security Categories

1. PROMPT - Injection, jailbreak (LLM01)
2. OUTPUT - Insecure output handling (LLM02)
3. TOOL - Dangerous tools without constraints (LLM07/08)
4. DATA - Secrets, PII exposure (LLM06)
5. MEMORY - RAG/context security
6. SUPPLY - Unpinned dependencies (LLM05)
7. BEHAVIOR - Excessive agency (LLM08/09)

## Dynamic Analysis - 4 Check Categories

1. Resource Management - Token/tool bounds, variance
2. Environment - Model pinning, tool coverage
3. Behavioral - Stability, predictability, outliers
4. Data - PII detection at runtime

## Correlation States (Phase 5)

- VALIDATED - Static issue confirmed at runtime (FIX FIRST!)
- UNEXERCISED - Code path never executed
- THEORETICAL - Static issue, but safe at runtime
- RUNTIME_ONLY - Found only during runtime

## Fix Workflow

Recommendations follow: PENDING → FIXING → FIXED → VERIFIED

Use MCP tools: `start_fix()`, `complete_fix()`, `dismiss_recommendation()`
```

---

## STEP 6: INSTALL SLASH COMMANDS (CRITICAL!)

⚠️ **Without this step, `/agent-scan`, `/agent-fix`, etc. will NOT work!**

Cursor 1.6+ supports custom slash commands via `.cursor/commands/` directory. These enable native `/agent-scan`, `/agent-fix`, `/agent-gate` etc. commands in the chat.

**Create the commands directory:**
```bash
mkdir -p {AGENT_PROJECT_FOLDER}/.cursor/commands
```

**Copy slash command files from package template:**

Look for: `integrations/cursor/cursor-commands/` in the installed package or repo

Copy ALL `.md` files to: `{AGENT_PROJECT_FOLDER}/.cursor/commands/`

```bash
# If in local dev mode (inside cylestio-perimeter repo):
cp {REPO_ROOT}/integrations/cursor/cursor-commands/*.md {AGENT_PROJECT_FOLDER}/.cursor/commands/

# Commands to copy:
# - agent-scan.md       → /agent-scan
# - agent-fix.md        → /agent-fix
# - agent-analyze.md    → /agent-analyze  
# - agent-correlate.md  → /agent-correlate
# - agent-gate.md       → /agent-gate
# - agent-report.md     → /agent-report
# - agent-status.md     → /agent-status
```

**Verify commands are installed:**
```bash
ls {AGENT_PROJECT_FOLDER}/.cursor/commands/
# Should show: agent-analyze.md  agent-correlate.md  agent-fix.md  agent-gate.md  agent-report.md  agent-scan.md  agent-status.md
```

**How it works:**
- When user types `/` in Cursor chat, these commands appear in the dropdown
- Selecting a command loads the markdown content as instructions for the AI
- Commands reference Agent Inspector MCP tools automatically

### Optional: Detailed Skills

For more comprehensive skill files, check `integrations/skills/` (if available):
- `static-analysis/SKILL.md` - Complete `/agent-scan` workflow
- `auto-fix/SKILL.md` - Complete `/agent-fix` workflow with prioritization
- `dynamic-analysis/SKILL.md` - Runtime tracing setup

---

## STEP 7: UPDATE AGENT CODE TO USE PROXY

### 7.1 Determine the Workflow ID

The workflow ID identifies your agent in Agent Inspector. Use the **project folder name** by default.

```
{WORKFLOW_ID} = name of the agent project folder

Examples:
- /home/user/my-sales-bot/     → WORKFLOW_ID = "my-sales-bot"
- /home/user/agents/chatbot/   → WORKFLOW_ID = "chatbot"
- /home/user/company-ai/       → WORKFLOW_ID = "company-ai"
```

### 7.2 Search for LLM Client Initialization

```bash
grep -rn "Anthropic\|OpenAI" {AGENT_PROJECT_FOLDER} --include="*.py" | head -20
```

### 7.3 Update base_url with Workflow-Based URL (PREFERRED)

**For each match, update or add `base_url` using the workflow format:**

```python
# Anthropic - use workflow-based URL:
client = Anthropic(
    api_key="...",
    base_url="http://localhost:4000/agent-workflow/{WORKFLOW_ID}"
)

# OpenAI - use workflow-based URL:
client = OpenAI(
    api_key="...",
    base_url="http://localhost:4000/agent-workflow/{WORKFLOW_ID}/v1"
)
```

**Real examples:**

```python
# For a project named "my-sales-bot":
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    base_url="http://localhost:4000/agent-workflow/my-sales-bot"
)

# For a project named "customer-support-agent":
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="http://localhost:4000/agent-workflow/customer-support-agent/v1"
)
```

### Why Workflow-Based URLs?

| URL Type | Example | Benefit |
|----------|---------|---------|
| ❌ Basic | `http://localhost:4000` | Traffic not associated with workflow |
| ✅ Workflow | `http://localhost:4000/agent-workflow/my-bot` | Traffic tracked per agent, appears in dashboard correctly |

**The workflow-based URL ensures:**
- All LLM calls are tracked under the correct agent workflow
- Dashboard shows sessions organized by agent
- Dynamic analysis works correctly
- Correlation between static findings and runtime data is accurate

### 7.4 Check Existing base_url

- If `base_url` already uses workflow format (`localhost:4000/agent-workflow/...`) → verify workflow ID is correct
- If `base_url` uses basic format (`localhost:4000`) → UPDATE to workflow format
- If `base_url` missing → ADD with workflow format

**YOU MUST EDIT THE ACTUAL FILES** - use your file editing tools to make these changes.

---

## STEP 8: START AGENT INSPECTOR SERVER (REQUIRED)

```
╔══════════════════════════════════════════════════════════════════╗
║  ⚠️  MANDATORY STEP - DO NOT SKIP                                 ║
║                                                                   ║
║  The Agent Inspector server MUST be running for MCP to work.      ║
║  Either start it yourself OR tell the user exactly how to start.  ║
║                                                                   ║
║  If you skip this step, the user will get "MCP tools unavailable" ║
║  errors and think the installation failed.                        ║
╚══════════════════════════════════════════════════════════════════╝
```

### 8.1 Start the Server

**Try to start it yourself** in a background terminal.

⚠️ **CORRECT COMMAND FORMAT:**
```bash
agent-inspector {PROVIDER}
```
Where `{PROVIDER}` is either `anthropic` or `openai` - nothing else!

❌ **WRONG COMMANDS (DO NOT USE):**
```bash
# These will FAIL - there is no 'serve' command!
agent-inspector serve          # WRONG!
agent-inspector serve --port   # WRONG!
agent-inspector start          # WRONG!
agent-inspector run            # WRONG!
```

✅ **CORRECT COMMANDS:**
```bash
# For Anthropic-based agents:
source {AGENT_PROJECT_FOLDER}/venv/bin/activate
agent-inspector anthropic &

# For OpenAI-based agents:
source {AGENT_PROJECT_FOLDER}/venv/bin/activate
agent-inspector openai &
```

#### Local Dev Mode:
```bash
source {AGENT_PROJECT_FOLDER}/venv/bin/activate
cylestio-perimeter run --config {PATH_TO_CONFIG} &
```

### 8.2 Verify Server is Running

After starting, verify the server is accessible:
- Dashboard should be at: http://localhost:7100
- MCP endpoint should be at: http://localhost:7100/mcp

**If background execution fails or isn't supported**, tell the user:

> "Please start Agent Inspector in a separate terminal:
> ```bash
> source venv/bin/activate
> agent-inspector anthropic
> ```
> (Use `agent-inspector openai` if your agent uses OpenAI)
> Keep it running while using the security tools."

⚠️ **REMEMBER:** The command is `agent-inspector anthropic` or `agent-inspector openai`. NOT `agent-inspector serve`!

### 8.3 Wait for Server Startup

The server takes 2-3 seconds to initialize. Wait before proceeding.

---

## STEP 8.5: INTEGRATE INTO AUTO-STARTUP (RECOMMENDED)

**Goal:** Make Agent Inspector start automatically with your project so users don't have to manually start it each time.

### Check if Project Has Startup Scripts

```bash
ls {AGENT_PROJECT_FOLDER}/start_mcp_servers.py 2>/dev/null || \
ls {AGENT_PROJECT_FOLDER}/run.py 2>/dev/null || \
ls {AGENT_PROJECT_FOLDER}/start.py 2>/dev/null || \
echo "NO_STARTUP_SCRIPT"
```

### If Startup Script Exists

1. Add Agent Inspector to the startup script
2. Use the venv's agent-inspector command: `venv/bin/agent-inspector`
3. Start with: `agent-inspector anthropic` (or `openai` for OpenAI-based agents)
4. Add it BEFORE other MCP servers (with 3-second wait time)

⚠️ **CORRECT COMMAND:** `agent-inspector anthropic` or `agent-inspector openai`
❌ **NOT:** `agent-inspector serve` (this command does not exist!)

**Example integration (for start_mcp_servers.py or run.py):**

```python
import os
import subprocess
import time

# Get venv's agent-inspector path
venv_bin = os.path.join(os.path.dirname(__file__), "venv", "bin")
agent_inspector_cmd = os.path.join(venv_bin, "agent-inspector")

# Start Agent Inspector first
# Use "anthropic" or "openai" depending on the LLM provider
subprocess.Popen(
    [agent_inspector_cmd, "anthropic"],  # or "openai"
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
print("Starting Agent Inspector on http://localhost:7100")
time.sleep(3)  # Wait for startup

# ... rest of your startup script
```

### If No Startup Script Exists

**Option A:** Create a simple startup script:

```python
#!/usr/bin/env python3
"""start_services.py - Start Agent Inspector and related services"""
import os
import subprocess
import sys

def main():
    venv_bin = os.path.join(os.path.dirname(__file__), "venv", "bin")
    agent_inspector = os.path.join(venv_bin, "agent-inspector")
    
    if os.path.exists(agent_inspector):
        print("🚀 Starting Agent Inspector...")
        # Use "anthropic" or "openai" - NOT "serve"!
        subprocess.Popen(
            [agent_inspector, "anthropic"],  # or "openai" for OpenAI-based agents
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✅ Agent Inspector started on http://localhost:7100")
    else:
        print("❌ agent-inspector not found. Run: pip install agent-inspector")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**Option B:** Document the manual start command clearly in README or project docs.

### Why Auto-Startup Matters

- Users won't have to remember to start Agent Inspector manually
- Prevents "MCP tools unavailable" errors
- Professional, seamless experience

---

## STEP 9: RELOAD IDE TO CONNECT MCP

**For Cursor - Multiple options:**

1. **Settings UI (easiest):** Go to Settings → Tools & MCP → click refresh/reload on MCP servers
2. **Command Palette:** Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux), type "Reload Window"
3. **Full Restart:** Quit and reopen Cursor

> "To connect to Agent Inspector MCP:
> - Go to **Settings → Tools & MCP** and reload the MCP servers
> - Or press `Cmd+Shift+P` → 'Developer: Reload Window'
> - Or restart Cursor
> 
> You should see 'agent-inspector' with 17 tools enabled."

---

## STEP 10: REGISTER IDE CONNECTION (AUTOMATIC)

⚠️ **CRITICAL: This step MUST succeed. If it fails, retry on EVERY subsequent MCP tool call.**

**When to register:**
- ✅ Immediately after installation (during first scan - see STEP 11)
- ✅ Before every security analysis request (scan, analyze, fix, etc.) - auto-switches workflow
- ✅ Registration is idempotent - safe to call every time

**Key principle:** Always register IDE for the agent workflow being analyzed, not the parent repo!

**Typical setup:** Most customers install Agent Inspector directly in their agent's repo, so the workflow ID matches the agent's folder name.

### 9.1 Determine Your Model Name

**You MUST know what AI model you are.** Check your system prompt or self-identify:

| If you are... | Use model value |
|---------------|-----------------|
| Claude Opus 4.5 | `"claude-opus-4.5"` |
| Claude Sonnet 4 | `"claude-sonnet-4"` |
| Claude Sonnet 3.5 | `"claude-sonnet-3.5"` |
| GPT-4o | `"gpt-4o"` |
| GPT-4 Turbo | `"gpt-4-turbo"` |
| Other | Use your actual model identifier |

**If unsure, check:** Your system prompt often says "powered by X" or "You are X".

### 9.2 How to Register IDE Connection

Registration happens automatically as part of every scan/analysis command (see STEP 11). Here's the pattern:

```
register_ide_connection(
  ide_type="cursor",              // REQUIRED: always "cursor"
  agent_workflow_id="my-agent",   // REQUIRED: from scan target folder name
  workspace_path="/path/to/project",  // REQUIRED: full workspace path
  model="claude-sonnet-4"         // REQUIRED: your AI model name
)
```

**Parameter values:**
| Parameter | How to determine |
|-----------|------------------|
| `ide_type` | Always `"cursor"` |
| `agent_workflow_id` | **Scan target folder name**, NOT parent repo! (e.g., scanning `customer-support-agent/` → use `"customer-support-agent"`) |
| `workspace_path` | Full path to the workspace you're editing |
| `model` | Your AI model name (see table above) |

**Critical for workflow matching:**
```
✅ CORRECT: Scanning "my-booking-agent/" → register with agent_workflow_id="my-booking-agent"
❌ WRONG:   Scanning "my-booking-agent/" → register with agent_workflow_id="parent-repo-name"

The workflow ID must match what you're scanning, not where you're scanning FROM!

Common scenarios:
- Standalone agent repo: Use the repo folder name (e.g., "sales-assistant")
- Agent in subfolder: Use the agent folder name (e.g., "agents/chatbot" → "chatbot")
- Monorepo with multiple agents: Use each agent's folder name individually
```

### 9.3 Store the Connection ID

**IMPORTANT: Store the returned `connection_id` in your context.** You need it for heartbeats.

Example response:
```json
{
  "connection": {
    "connection_id": "ide_abc123def456",  // ← SAVE THIS!
    ...
  }
}
```

### 9.4 If Registration Fails

If `register_ide_connection` fails:

1. **DO NOT GIVE UP** - Remember: `PENDING_IDE_REGISTRATION = true`
2. **Retry on EVERY subsequent MCP call** - Before any other Agent Inspector tool, try again
3. **Only stop retrying** when you get a successful `connection_id` back

### 9.5 Heartbeat Strategy (MINIMAL - Save Tokens!)

⚠️ **DO NOT send heartbeats after every action!** This wastes tokens and context.

**Send heartbeats ONLY:**
1. **Once at the START** of Agent Inspector work (after registration)
2. **Once at the END** of a complete task (optional)

That's it! The dashboard will show "connected" for 60 seconds after each heartbeat.

**Example minimal flow:**
```
// User: "Scan my agent for security issues"
register_ide_connection(...)  // Only if not already registered
ide_heartbeat(connection_id, is_developing=true)  // ONE heartbeat at start
// ... do all the scanning work ...
// Done! No more heartbeats needed
```

---

## ⚠️ RECONNECTION ON FUTURE SESSIONS (Lightweight)

**Only register when user asks for Agent Inspector features.** Don't register proactively.

### When user asks for security analysis (/scan, /analyze, /fix, etc.):

**ALWAYS register IDE for the workflow being worked on:**

```
1. Determine agent_workflow_id from scan target or current workspace
2. Call register_ide_connection(agent_workflow_id=<derived_id>)  // Idempotent!
3. Send ONE ide_heartbeat(is_developing=true)
4. Create analysis session with SAME agent_workflow_id
5. Do the work
6. Done - no more calls needed
```

**Example - User requests security analysis:**
```
User: "Run a security scan on this agent" (or "scan for vulnerabilities", etc.)

Your logic:
1. Determine scan target (current workspace or specified path)
2. Extract workflow ID from folder name
   → If scanning "customer-support-bot/" folder
   → agent_workflow_id = "customer-support-bot"
   
3. Register IDE for this workflow:
   → register_ide_connection(agent_workflow_id="customer-support-bot", ...)
   → ide_heartbeat(connection_id, is_developing=true)
   
4. Create analysis session with SAME workflow ID:
   → create_analysis_session(agent_workflow_id="customer-support-bot", ...)
   
5. Perform scan...
```

**For monorepos with multiple agents:**
```
User: "Scan the booking agent in the agents folder"

Your logic:
→ Scan target: agents/booking-agent/
→ agent_workflow_id = "booking-agent" (use leaf folder name, not "agents")
→ register_ide_connection(agent_workflow_id="booking-agent", ...)
→ create_analysis_session(agent_workflow_id="booking-agent", ...)
```

**This ensures:**
- Dashboard always shows correct workflow being analyzed
- IDE appears as "Connected" for active workflow
- No workflow ID mismatches

**Skip `get_ide_connection_status`** - just register directly. It's simpler and uses same tokens.

---

## STEP 11: RUN FIRST STATIC SCAN

> ⚠️ **Prerequisite:** Agent Inspector server must be running (Step 8). If not started, go back and start it now!

**If there's agent code in the project, run a security scan immediately.**

### 11.1 Check for Code

Look for Python/JS/TS files in the agent project:
```bash
ls {AGENT_PROJECT_FOLDER}/*.py {AGENT_PROJECT_FOLDER}/*.js {AGENT_PROJECT_FOLDER}/*.ts 2>/dev/null | head -5
```

### 11.2 If Code Exists, Run Static Scan

If MCP is connected, use the `/agent-scan` command workflow:

**CRITICAL - Workflow Matching:** Before scanning, ensure IDE is registered for the correct workflow:

```python
# Step 0: Determine workflow ID from scan target
if scanning_subfolder:
    # Example: agents/customer-support/ → "customer-support"
    # Example: my-agents/booking-bot/ → "booking-bot"
    agent_workflow_id = get_folder_name(scan_target_path)
else:
    # Scanning current workspace → use workspace folder name
    # Example: /path/to/sales-assistant/ → "sales-assistant"
    agent_workflow_id = get_folder_name(workspace_path)

# Step 1: Register IDE for THIS specific workflow (idempotent - safe to call every time)
register_ide_connection(
    ide_type="cursor",
    agent_workflow_id=agent_workflow_id,  # ← MUST match scan target!
    workspace_path=workspace_path,
    model=model
)
ide_heartbeat(connection_id, is_developing=true)
```

**Then proceed with scan:**

1. Create analysis session: `create_analysis_session(agent_workflow_id, "STATIC")` ← **Use SAME workflow ID!**
2. Get security patterns: `get_security_patterns()`
3. **Analyze code for ALL 7 security categories:**
   - PROMPT (LLM01): Injection, jailbreak
   - OUTPUT (LLM02): Insecure output handling
   - TOOL (LLM07/08): Dangerous tools
   - DATA (LLM06): Hardcoded secrets
   - MEMORY: RAG/context security
   - SUPPLY (LLM05): Dependencies
   - BEHAVIOR (LLM08/09): Excessive agency
4. Store findings with category: `store_finding(..., category="PROMPT")`
5. Complete session: `complete_analysis_session(session_id)`

**Why register before every scan?**
- IDE connection is per-workflow (tracks which agent you're analyzing)
- When scanning different folders, this auto-switches the dashboard view
- Registration is idempotent - calling it again just updates the connection
- **This prevents "Not Connected" errors in the dashboard**

**Report using the 7-category format:**
```
🔍 AI Security Scan Complete!

Security Checks (7):
✗ PROMPT Security: X Critical issues
✓ DATA Security: Passed
...

Gate Status: 🔒 BLOCKED / ✅ OPEN
```

If MCP not connected yet, tell user:
> "Reload Cursor, then type `/agent-scan` and I'll analyze your agent code."

**⚠️ After scanning (or if no code to scan), CONTINUE TO STEP 13 to display the welcome message!**

---

## STEP 12: COMPLETE INSTALLATION

⚠️ **REMINDER:** You MUST complete Step 13 (Display Welcome Message) before finishing.
This step verifies everything is working and confirms to the user that installation succeeded.

**Steps remaining:**
- Step 12 - Verify MCP connection and capabilities
- **Step 13 - DISPLAY WELCOME MESSAGE** ← MANDATORY FINAL STEP

---

## STEP 13: DISPLAY WELCOME MESSAGE (MANDATORY - DO NOT SKIP!)

```
╔══════════════════════════════════════════════════════════════════╗
║  ⚠️  THIS IS THE FINAL MANDATORY STEP                            ║
║                                                                   ║
║  YOU MUST display the welcome message below to the user.          ║
║  If you skip this step, the installation is INCOMPLETE.           ║
║                                                                   ║
║  DO NOT end your response without showing the ASCII banner        ║
║  and confirming installation is complete.                         ║
╚══════════════════════════════════════════════════════════════════╝
```

### WHY THIS STEP EXISTS

- User needs CONFIRMATION that installation worked
- Without the welcome message, user doesn't know what to do next
- This is the professional way to complete an installation
- **Skipping this step = installation failure**

### EXACT ACTIONS TO TAKE

**Action 1:** Display the ASCII art banner (copy exactly as shown below)
**Action 2:** Say "Installation Complete!"
**Action 3:** List the slash commands table
**Action 4:** Show the "Quick Start" section
**Action 5:** Confirm you're ready to help

### 13.1 (Optional) Check MCP Tools

If the server is running, you can verify MCP tools are available. But even if they're not connected yet, you MUST still display the welcome message.

### 13.2 DISPLAY THIS EXACT ASCII BANNER

⚠️ **COPY THIS EXACTLY - DO NOT CREATE YOUR OWN ASCII ART!**

The banner below spells "CYLESTIO" in block letters. Copy and paste it exactly as shown:

```
 ██████╗██╗   ██╗██╗     ███████╗███████╗████████╗██╗ ██████╗ 
██╔════╝╚██╗ ██╔╝██║     ██╔════╝██╔════╝╚══██╔══╝██║██╔═══██╗
██║      ╚████╔╝ ██║     █████╗  ███████╗   ██║   ██║██║   ██║
██║       ╚██╔╝  ██║     ██╔══╝  ╚════██║   ██║   ██║██║   ██║
╚██████╗   ██║   ███████╗███████╗███████║   ██║   ██║╚██████╔╝
 ╚═════╝   ╚═╝   ╚══════╝╚══════╝╚══════╝   ╚═╝   ╚═╝ ╚═════╝ 
                    AGENT INSPECTOR
```

❌ **DO NOT:**
- Create your own ASCII art
- Use a different banner
- Skip the banner
- Make a simpler text version

✅ **DO:** Copy the exact banner above character-for-character.

**Then say:** "✅ Installation Complete! Thanks for using Cylestio Agent Inspector! 🛡️"

#### What is Agent Inspector?

A security analysis platform for AI agents - find vulnerabilities, understand behavior, meet compliance.

#### Slash Commands (Cursor IDE)

Type `/agent-` in the chat to see all Agent Inspector commands. These are powered by custom slash commands installed in `.cursor/commands/`.

| Command | Description |
|---------|-------------|
| `/agent-scan` | Run static security scan on current workspace |
| `/agent-scan path/to/folder` | Run static scan on specific folder |
| `/agent-analyze` | Run dynamic analysis on runtime sessions |
| `/agent-correlate` | Correlate static findings with runtime data |
| `/agent-fix REC-001` | Fix a specific recommendation (AI-powered, contextual) |
| `/agent-fix` | Fix the next highest-priority blocking recommendation |
| `/agent-status` | Get dynamic analysis status (sessions available, etc.) |
| `/agent-gate` | Check production gate status and blocking issues |
| `/agent-report` | Generate security assessment report (as markdown) |

#### The `/agent-fix` Command - AI-Powered Security Fixes

When you say `/agent-fix REC-XXX`, I will:

1. **Get the recommendation details** - what's the vulnerability and where
2. **Start fix tracking** - marks status as FIXING in the audit trail
3. **Read and analyze your code** - understand context, patterns, style
4. **Apply an intelligent fix** - not a template, but adapted to your codebase
5. **Complete the fix** - marks status as FIXED with notes on what changed

**I'm smarter than template-based tools.** I understand your code semantically and apply fixes that match your patterns.

#### Recommendation Lifecycle

Every security finding has a recommendation: "what to do about it"

```
PENDING → FIXING → FIXED → VERIFIED
              ↓
         DISMISSED / IGNORED
```

- **PENDING**: Issue found, waiting for action
- **FIXING**: Someone (AI or human) is working on it
- **FIXED**: Fix applied, awaiting verification
- **VERIFIED**: Re-scan confirmed the issue is gone
- **DISMISSED**: Risk accepted (documented reason required)
- **IGNORED**: False positive (documented reason required)

#### Gate Status

Your agent has a **Production Gate**:
- 🔒 **BLOCKED**: CRITICAL or HIGH issues remain open → can't ship
- ✅ **OPEN**: All blocking issues resolved → ready to ship

#### The `/agent-gate` Command - Production Gate Check

When you say `/agent-gate`, I will:

1. **Check gate status** via `get_gate_status(workflow_id)`
2. **Report blocking items** if BLOCKED (what needs fixing)
3. **Show progress** towards production readiness
4. **Suggest generating a report** when OPEN

#### The `/agent-report` Command - Security Assessment Report

When you say `/agent-report`, I will generate a comprehensive security report in markdown format.

**Report Types:**
- **security_assessment** (default) - Full CISO report with all details
- **executive_summary** - High-level GO/NO-GO for leadership
- **customer_dd** - Due diligence report for customers/partners

**What I'll do:**

1. **Generate the report** by calling the compliance report API
2. **Format as markdown** with all key sections:
   - Executive Summary (GO/NO-GO decision, risk score)
   - Key Metrics (findings, fixed, blocking)
   - Blocking Issues (if any)
   - OWASP LLM Top 10 Coverage
   - SOC2 Compliance Status
   - Remediation Summary
3. **Return the markdown directly** in the chat

**Example output** (for an agent named "my-agent" - yours will show your agent's name):

```markdown
# Security Assessment: my-agent

**Generated:** December 15, 2024
**Risk Score:** 45/100

---

## ✅ Decision: GO

Cleared for production deployment. All critical and high security issues have been addressed.

## Key Metrics

| Metric | Value |
|--------|-------|
| Risk Score | 45/100 |
| Total Findings | 12 |
| Open Issues | 3 |
| Fixed | 8 |
| Blocking Issues | 0 |

## OWASP LLM Top 10 Coverage

| Control | Status | Details |
|---------|--------|---------|
| LLM01: Prompt Injection | ✅ PASS | No issues found |
| LLM06: Sensitive Info | ⚠️ WARNING | 2 open, 1 fixed |
...

*Generated by Cylestio Agent Inspector*
```

**Variations:**
- `/agent-report` - Generate full security assessment (default)
- `/agent-report executive` - Generate executive summary for leadership
- `/agent-report customer` - Generate customer due diligence report

Use this before deployment to ensure all critical issues are addressed.

#### The `/agent-analyze` Command - Dynamic Runtime Analysis

When you say `/agent-analyze`, I will:

1. **Check for available sessions** - runtime sessions from agent traffic through proxy
2. **Trigger on-demand analysis** - only analyzes NEW sessions since last run
3. **Run 16 security checks** across 4 categories:
   - **Resource Management**: Token/tool call bounds, variance analysis
   - **Environment**: Model pinning, tool coverage, unused tools
   - **Behavioral**: Stability, outliers, predictability, clustering
   - **Data**: PII detection in prompts and responses
4. **Create findings & recommendations** - just like static analysis
5. **Auto-resolve old issues** - issues not found in new sessions are marked resolved

**Key points:**
- Analysis is **ON-DEMAND** - only runs when you ask
- Each run analyzes only **NEW sessions** (incremental)
- Results reflect the **current state** of your agent

#### The `/agent-correlate` Command - Cross-Analysis Correlation

When you say `/agent-correlate`, I will:

1. **Get static findings** - issues found in code analysis
2. **Get runtime data** - tool usage patterns from dynamic sessions
3. **Correlate findings** with one of these states:
   - **VALIDATED**: Static issue confirmed at runtime (highest priority!)
   - **UNEXERCISED**: Code path never executed at runtime
   - **THEORETICAL**: Static issue, but safe at runtime (other safeguards)
   - **RUNTIME_ONLY**: Issue found only at runtime
4. **Update finding correlation** - stores evidence and state

**Why correlate?**
- Prioritize **VALIDATED** issues - they're real and active
- Deprioritize **UNEXERCISED** code - may be dead code
- Understand your agent's actual risk surface

#### The 7 Security Checks

Your agent is evaluated against 7 security categories:
1. **PROMPT** - Prompt injection (LLM01)
2. **OUTPUT** - Insecure output handling (LLM02)
3. **TOOL** - Dangerous tools (LLM07/08)
4. **DATA** - Secrets exposure (LLM06)
5. **MEMORY** - RAG/context security
6. **SUPPLY** - Dependencies (LLM05)
7. **BEHAVIOR** - Excessive agency (LLM08/09)

**Gate is BLOCKED** if any HIGH or CRITICAL issues exist.

#### Quick Links

- **Dashboard:** http://localhost:7100  
- **Static Analysis:** http://localhost:7100/agent-workflow/{id}/static-analysis
- **Proxy:** http://localhost:4000/agent-workflow/{your-workflow-id}

#### I'll Remember Agent Inspector

The rules file ensures I'll use these tools when you ask about security - even in future chats!

---

### 13.3 SAY THIS EXACT TEXT (Required)

After the welcome content above, you MUST say:

---

✅ **Agent Inspector installation is complete!**

**🚀 Quick Start - What to do next:**
1. Type `/agent-scan` to run your first security scan
2. Visit http://localhost:7100 to see the dashboard  
3. Use `/agent-fix REC-XXX` to fix any issues found

**Need help?** Just ask me about Agent Inspector or any security concerns!

---

### 13.4 VERIFY YOU COMPLETED THIS STEP

Ask yourself:
- ✅ Did I show the ASCII art banner? (The big "CYLESTIO" text)
- ✅ Did I say "Installation Complete"?
- ✅ Did I show the slash commands table?
- ✅ Did I show the Quick Start section?

**If any answer is NO, go back and do it now.**

**DO NOT proceed to the checklist or end your response until ALL of the above are YES.**

---

## CHECKLIST - VERIFY COMPLETION

**Before ending your response, verify EVERY item below is checked.**

### Setup Steps (Steps 1-7)
- [ ] Identified agent project folder
- [ ] Verified user opened project folder directly (not a parent folder)
- [ ] Checked/created virtual environment
- [ ] Ran `pip install` (saw "Successfully installed" or "Requirement already satisfied")
- [ ] Created/updated `.cursor/mcp.json` with agent-inspector config
- [ ] Created `.cursor/rules/agent-inspector.mdc`
- [ ] Copied slash commands to `.cursor/commands/` (7 files: agent-scan.md, agent-fix.md, agent-analyze.md, agent-correlate.md, agent-gate.md, agent-report.md, agent-status.md)
- [ ] Updated agent code with `base_url` (if applicable)

### 🔴 MANDATORY: Server Startup (Step 8)
- [ ] **Started Agent Inspector server** - one of these MUST be true:
  - [ ] Started server in background terminal myself, OR
  - [ ] Told user EXACTLY how to start it with specific command

### Optional: Auto-Startup (Step 8.5)  
- [ ] Checked for startup scripts
- [ ] Integrated Agent Inspector into startup (if scripts exist)

### Connection Steps (Steps 9-12)
- [ ] Told user to reload IDE (Settings → Tools & MCP → Reload)
- [ ] Registered IDE connection (or noted it will happen on first scan)
- [ ] Ran first static scan if code exists

### 🔴 MANDATORY: Welcome Message (Step 13) - FINAL STEP!

**⛔ STOP! Before you end your response, verify:**

- [ ] **Did you display the ASCII art "CYLESTIO" banner?** If NO → Go display it now!
- [ ] **Did you show the slash commands table?** If NO → Go show it now!
- [ ] **Did you say "Installation Complete"?** If NO → Go say it now!
- [ ] **Did you show the Quick Start section?** If NO → Go show it now!

```
╔═══════════════════════════════════════════════════════════════════╗
║                                                                    ║
║   IF ANY OF THE ABOVE ARE "NO", YOU ARE NOT DONE.                 ║
║   GO BACK AND COMPLETE STEP 13 BEFORE ENDING YOUR RESPONSE.       ║
║                                                                    ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## FINAL SELF-CHECK

**Ask yourself these questions before finishing:**

1. **Is the server running (or did I tell the user how to start it)?**
   - YES → Continue
   - NO → Go back to Step 8

2. **Did I display the welcome message with ASCII banner?**
   - YES → You're done! ✅
   - NO → Go back to Step 13 and display it NOW

**The installation is FAILED if the user did not see the welcome message.**

---

## POST-INSTALLATION: Using Agent Inspector

### Static Scan Workflow (`/agent-scan`)

```
/scan → Analyzes code → Creates findings → Generates recommendations → Shows gate status
```

Each finding gets a `REC-XXX` recommendation ID. Fix them with `/fix REC-XXX`.

### Dynamic Analysis Workflow (`/agent-analyze`)

```
/analyze → Analyzes runtime sessions → Creates security checks → Updates gate status
```

**Prerequisites:**
1. Agent must send traffic through the proxy (`base_url="http://localhost:4000/agent-workflow/{workflow-id}"`)
2. At least 1 completed session available

**Key behaviors:**
- **On-demand only** - never auto-triggers
- **Incremental** - only analyzes NEW sessions since last run
- **Auto-resolves** - old issues not in new sessions are marked resolved

### Correlation Workflow (`/agent-correlate`)

```
/correlate → Gets static findings + runtime data → Updates correlation states
```

**When to use:**
- After running BOTH static scan AND dynamic analysis
- To prioritize which issues are real risks vs theoretical

**Correlation states:**
- **VALIDATED**: Issue exists in code AND was triggered at runtime → **FIX FIRST!**
- **UNEXERCISED**: Issue in code, but code path never executed → lower priority
- **THEORETICAL**: Issue in code, but runtime shows it's safe → may be OK
- **RUNTIME_ONLY**: Issue found only at runtime → add static check

### Fix Workflow (`/agent-fix`)

```
/fix REC-001 → Reads code → Applies contextual fix → Updates status
```

The fix is tracked in an audit trail for compliance (who fixed what, when, how).

### Gate Check Workflow (`/agent-gate`)

```
/gate → Checks production gate → Reports blocking issues → Shows progress
```

**Gate states:**
- 🔒 **BLOCKED**: CRITICAL or HIGH severity issues remain open
- ✅ **OPEN**: All blocking issues resolved, ready for production

### Report Generation Workflow (`/agent-report`)

```
/report → Generates compliance report → Returns markdown directly in chat
```

**Report types:**
- `security_assessment` (default): Full CISO report with OWASP, SOC2, evidences
- `executive_summary`: High-level GO/NO-GO for leadership
- `customer_dd`: Due diligence for customers/partners

**The markdown report includes:**
- Executive Summary with GO/NO-GO decision
- Risk Score and key metrics
- Blocking Issues (if any)
- OWASP LLM Top 10 coverage table
- SOC2 compliance status table
- Remediation summary

**Example:**
```
User: /report
AI: Here's your security assessment report:

# Security Assessment: my-agent
**Risk Score:** 45/100
## ✅ Decision: GO
...
```

### Viewing Results

| URL | What it shows |
|-----|---------------|
| http://localhost:7100 | Dashboard home |
| http://localhost:7100/agent-workflow/{id}/static-analysis | Static scan findings with correlation |
| http://localhost:7100/agent-workflow/{id}/dynamic-analysis | Dynamic runtime analysis |
| http://localhost:7100/agent-workflow/{id}/recommendations | All recommendations & fix status |
| http://localhost:7100/agent-workflow/{id}/reports | Compliance reports & gate status |
| http://localhost:7100/agent-workflow/{id}/sessions | Runtime session history |

### MCP Tools Reference

#### Static Analysis Tools
| Tool | Purpose |
|------|---------|
| `get_security_patterns` | Get OWASP LLM patterns for scanning |
| `create_analysis_session` | Start a scan session (type: STATIC or DYNAMIC) |
| `store_finding` | Record a security finding |
| `complete_analysis_session` | Finalize scan, calculate risk |

#### Dynamic Analysis Tools
| Tool | Purpose |
|------|---------|
| `trigger_dynamic_analysis` | Trigger on-demand runtime analysis |
| `get_dynamic_analysis_status` | Check if analysis can be triggered, session counts |
| `get_tool_usage_patterns` | Get tool usage metrics from runtime |
| `get_agents` | List agents discovered during runtime |

#### Correlation Tools (Phase 5)
| Tool | Purpose |
|------|---------|
| `update_finding_correlation` | Set finding correlation state (VALIDATED/UNEXERCISED/etc.) |
| `get_correlation_summary` | Get counts by correlation state for workflow |
| `get_agent_workflow_correlation` | Full correlation data: static + dynamic findings |

#### Recommendation & Fix Tools
| Tool | Purpose |
|------|---------|
| `get_recommendations` | List recommendations for workflow |
| `start_fix` | Mark recommendation as FIXING |
| `complete_fix` | Mark recommendation as FIXED |
| `dismiss_recommendation` | Dismiss with documented reason |
| `verify_fix` | Verify a fix was successful |
| `get_gate_status` | Check if production is blocked |

#### Reports & Compliance (Phase 6)
| Tool | Purpose |
|------|---------|
| `get_gate_status` | Check production gate (BLOCKED/OPEN) and blocking items |
| API: `/api/workflow/{id}/compliance-report` | Generate CISO-ready compliance report |

**Compliance Report includes:**
- Executive summary with GO/NO-GO decision
- OWASP LLM Top 10 coverage status
- SOC2 compliance mapping
- All 7 security check statuses
- Remediation summary with counts
- Audit trail for compliance

#### Lifecycle Tools
| Tool | Purpose |
|------|---------|
| `get_agent_workflow_state` | Get overall workflow state (static/dynamic/both) |
| `get_analysis_history` | View past analysis runs |

---

## REFERENCE

| Port | Service | URL Format |
|------|---------|------------|
| 4000 | LLM Proxy | `http://localhost:4000/agent-workflow/{workflow-id}` (Anthropic) or `/v1` suffix (OpenAI) |
| 7100 | Dashboard + MCP Server | `http://localhost:7100` |

### Troubleshooting

| Problem | Solution |
|---------|----------|
| Command not found | Re-run install step |
| MCP tools unavailable | Reload IDE, verify server running |
| Connection refused | Start the server (Step 8) |
| Permission denied | Activate venv first |
| `'serve' is not one of 'openai', 'anthropic'` | **WRONG COMMAND!** Use `agent-inspector anthropic` or `agent-inspector openai`. There is NO `serve` subcommand. |
| Slash commands not appearing | 1. Verify Cursor 1.6+ (Help → About), 2. Check `.cursor/commands/*.md` files exist, 3. Reload Window (Cmd+Shift+P → "Developer: Reload Window"), 4. Slash commands are a beta feature |
| Rules/commands not detected | Open the agent project folder **directly** in Cursor. Cursor only reads `.cursor/` from workspace root - subfolders are ignored |
| Installation seems incomplete | Did you display the welcome message (Step 13)? It's mandatory! |
| Server not starting automatically | Add auto-startup integration (Step 8.5) |

### Common Mistakes

1. **Not starting the server** - The MCP tools won't work without the server running. Always complete Step 8.
2. **Skipping the welcome message** - Users need confirmation that installation worked. Always complete Step 13.
3. **Not integrating auto-startup** - Consider adding Agent Inspector to startup scripts (Step 8.5) for better UX.
4. **Using basic proxy URL instead of workflow URL** - Use `http://localhost:4000/agent-workflow/{name}` not just `http://localhost:4000`. The workflow URL ensures traffic is tracked correctly.
5. **Using wrong server command** - The command is `agent-inspector anthropic` or `agent-inspector openai`. There is NO `serve`, `start`, or `run` subcommand!
6. **Creating custom ASCII banner** - Copy the EXACT "CYLESTIO" banner from Step 13. Do NOT create your own ASCII art.

### ⛔ FAILURE MODES - What BAD installations look like

**FAILED Installation #1:** "I've set up the config files. Let me know if you need anything else."
- ❌ No server started
- ❌ No welcome message
- **User thinks:** "Is it installed? What do I do now?"

**FAILED Installation #2:** "Installation complete. The server should be running on port 7100."
- ❌ No ASCII banner
- ❌ No slash commands table
- ❌ No Quick Start guidance
- **User thinks:** "What commands can I use? How do I start?"

**FAILED Installation #3:** Ends response after Step 11 (running first scan)
- ❌ Forgot to display welcome message
- **User thinks:** "The scan ran but... now what?"

**FAILED Installation #4:** Used `agent-inspector serve --port 7100`
- ❌ Server fails with error: `'serve' is not one of 'openai', 'anthropic'`
- ❌ Server never actually started
- **User thinks:** "The installation failed, something is broken"
- **FIX:** Use `agent-inspector anthropic` or `agent-inspector openai`

**FAILED Installation #5:** Made up custom ASCII banner
- ❌ Shows some random ASCII art instead of "CYLESTIO"
- ❌ Looks unprofessional and inconsistent
- **User thinks:** "Is this the right product?"
- **FIX:** Copy the EXACT banner from Step 13.2

**SUCCESSFUL Installation looks like:**
1. ✅ Server is running with correct command (`agent-inspector anthropic` or `openai`)
2. ✅ Big ASCII "CYLESTIO" banner displayed (the EXACT one from guide)
3. ✅ "Installation Complete!" message shown
4. ✅ Slash commands table displayed
5. ✅ Quick Start section with next steps
6. ✅ User knows exactly what to do next
