---
description: Run comprehensive static security analysis on AI agent code using OWASP LLM Top 10 framework. Analyze prompts, outputs, tools, data handling, memory, supply chain, and behavioral patterns. Use when user asks for security scan, vulnerability check, OWASP analysis, code review for security, or wants to check their AI agent for security issues.
---

# Static Security Scan

Run a comprehensive security scan on AI agent code using the OWASP LLM Top 10 framework.

## Prerequisites

**You MUST run `/agent-inspector:setup` BEFORE proceeding.**

This is NOT optional. The setup command will:
1. Check if agent-inspector is already running
2. Auto-detect your LLM provider (OpenAI/Anthropic)
3. Start the server in background if needed
4. Verify MCP connection is working

**DO NOT skip this step.** If you proceed without running the Preflight Check, MCP tools will fail.

## Your Advantage Over Traditional SAST

You are smarter than any static analysis tool. You can:
- Understand code semantically, not just pattern match
- Reason about AI agent-specific vulnerabilities
- Avoid false positives through contextual understanding
- Find issues no SAST would ever catch

## Scan Workflow

### 1. Derive agent_workflow_id
Auto-derive from (priority order):
1. Git remote: `github.com/acme/my-agent.git` -> `my-agent`
2. Package name: `pyproject.toml` or `package.json`
3. Folder name: `/projects/my-bot` -> `my-bot`

### 2. Register IDE Connection
If not already registered in this session:
```
register_ide_connection(
  ide_type="claude-code",
  agent_workflow_id=agent_workflow_id,
  workspace_path="/full/path/to/workspace",
  model="claude-opus-4-5-20251101"  # Your model from system prompt
)
```
Save the `connection_id` from response, then send one heartbeat:
```
ide_heartbeat(connection_id, is_developing=true)
```

### 3. Create Analysis Session
```
create_analysis_session(agent_workflow_id, session_type="STATIC")
```

### 4. Get Security Patterns
```
get_security_patterns()
```
**NEVER hardcode patterns** - always fetch from MCP. But also use your own understanding!

### 5. Analyze Code for ALL 7 Categories

**For each code file**, analyze thoroughly looking for:

**1. PROMPT Security (LLM01)**
- User input concatenated into prompts without sanitization
- System prompts that can be overridden or leaked
- Jailbreak vectors, prompt injection points
- Missing input validation before LLM calls
- Prompt templates with unsafe interpolation

**2. OUTPUT Security (LLM02)**
- Agent output used directly in SQL queries, shell commands, or code
- XSS vulnerabilities when rendering agent responses in web UI
- Agent output passed to dangerous functions (eval, exec)
- No output validation before downstream use
- Unescaped agent responses in logs or displays

**3. TOOL Security (LLM07, LLM08)**
- Dangerous tools (shell, file, network) without constraints
- Missing permission checks on tool execution
- Tools that can be chained dangerously
- No input validation on tool parameters
- Insecure plugin/tool interfaces

**4. DATA Security (LLM06)**
- Hardcoded API keys, secrets, credentials
- PII in prompts or system instructions
- Sensitive data logged or exposed in responses
- Credentials in error messages
- Unencrypted sensitive data storage

**5. MEMORY & CONTEXT Security**
- Conversation history stored insecurely
- RAG/vector store poisoning vulnerabilities
- Context injection through retrieved documents
- No validation of retrieved content before use
- Unbounded context accumulation
- Shared memory between users/sessions

**6. SUPPLY CHAIN Security (LLM05)**
- Unpinned model versions
- External prompt sources without validation
- Unsafe dependencies with known CVEs
- No integrity checks on loaded resources
- Unvalidated model downloads

**7. BEHAVIORAL Security (LLM08/09)**
- No token/cost limits
- Unbounded loops or recursion
- No rate limiting on tool calls
- Missing human-in-the-loop for sensitive operations
- Agent can be manipulated to exceed boundaries
- No approval gates for high-risk actions

### 6. Store Findings

For each issue found:
```
store_finding(
  session_id=session_id,
  file_path="src/agent.py",
  finding_type="PROMPT_INJECTION",
  severity="CRITICAL",
  category="PROMPT",
  title="User input in system prompt",
  description="User input directly concatenated into system prompt",
  line_start=45,
  line_end=52,
  code_snippet="...",
  owasp_mapping=["LLM01"],
  cwe="CWE-94"
)
```

### 7. Complete Session
```
complete_analysis_session(session_id)
```

### 8. Report Summary

Format example

```
AI Security Scan Complete!

Scanned: X files

Security Checks (7):
X PROMPT Security: 2 Critical issues
X OUTPUT Security: 1 High issue
! TOOL Security: 2 Medium issues
/ DATA Security: Passed
/ MEMORY Security: Passed
/ SUPPLY CHAIN: Passed
/ BEHAVIORAL: Passed

Gate Status: BLOCKED (2 categories failed)

View details: http://localhost:7100/agent-workflow/{id}/static-analysis

Fix most critical: /agent-inspector:fix REC-001
```

## Quality Over Quantity

- **DO** find every real security issue
- **DO** use your understanding of context to assess severity
- **DON'T** flag things that aren't actually exploitable
- **DON'T** generate noise like traditional SAST
- **ALWAYS** categorize into one of the 7 security checks

## After Scanning

If dynamic data exists (state is `COMPLETE`), automatically run correlation:
```
get_agent_workflow_correlation(agent_workflow_id)
```

Report which findings are VALIDATED (confirmed at runtime) vs UNEXERCISED (never triggered).
