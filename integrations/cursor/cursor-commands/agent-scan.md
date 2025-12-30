# Run AI Agent Security Scan

Run a comprehensive security scan on the current workspace or specified path using Agent Inspector MCP tools.

## Instructions

### Step 0: Derive agent_workflow_id

**DO NOT ask the user.** Auto-derive from (priority order):
1. Git remote → repo name (e.g., `github.com/acme/my-agent.git` → `my-agent`)
2. Package name → from `pyproject.toml` or `package.json`
3. Folder name → last path segment

Use the **same `agent_workflow_id`** for ALL commands (scan, analyze, correlate, etc.) to ensure unified results.

### Step 1: Register IDE Connection

Call `register_ide_connection` with:
- `ide_type`: "cursor"
- `agent_workflow_id`: the value derived in Step 0
- `workspace_path`: full workspace path
- `model`: your AI model name (check system prompt for "powered by X")

Save the `connection_id` from response. Send ONE `ide_heartbeat(connection_id, is_developing=true)`.

### Step 2: Create Analysis Session

Call `create_analysis_session(agent_workflow_id, session_type="STATIC")` and save the `session_id`.

### Step 3: Get Security Patterns

Call `get_security_patterns()` to get OWASP LLM Top 10 patterns. NEVER hardcode patterns.

### Step 4: Analyze Code

Analyze ALL code files for 7 security categories:

- **PROMPT (LLM01)**: User input in prompts, prompt injection, jailbreak vectors
- **OUTPUT (LLM02)**: Agent output in SQL/shell/code, XSS, eval/exec
- **TOOL (LLM07/08)**: Dangerous tools without constraints, missing permissions
- **DATA (LLM06)**: Hardcoded secrets, PII exposure, credentials in logs
- **MEMORY**: RAG poisoning, context injection, unbounded context
- **SUPPLY (LLM05)**: Unpinned dependencies, unvalidated sources
- **BEHAVIOR (LLM08/09)**: No rate limits, unbounded loops, missing approvals

### Step 5: Store Findings

For each finding, call:
```
store_finding(session_id, file_path, finding_type, severity, title,
              category, description, code_snippet, owasp_mapping, cwe, ...)
```

### Step 6: Complete Session

Call `complete_analysis_session(session_id)`.

### Step 7: Report Summary

Use this format:
```
🔍 AI Security Scan Complete!

Scanned: X files

Security Checks (7):
✗ PROMPT Security: X Critical issues
✓ DATA Security: Passed
...

Gate Status: 🔒 BLOCKED / ✅ OPEN

View: http://localhost:7100/agent-workflow/{agent_workflow_id}/static-analysis
Fix most critical: /agent-fix REC-001
```

## Parameters

You can optionally specify a path after the command: `/scan path/to/folder`

If no path specified, scan the current workspace.

## Quality Guidelines

- **DO** find every real security issue
- **DO** use semantic understanding to assess severity
- **DON'T** flag things that aren't exploitable (avoid false positives)
- **DON'T** generate noise like traditional SAST
- **ALWAYS** categorize into one of the 7 security checks

