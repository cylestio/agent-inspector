---
description: Cross-reference static code findings with dynamic runtime observations. Identify VALIDATED (confirmed at runtime) vs UNEXERCISED (never triggered) issues. Use when user asks to correlate, cross-reference static and dynamic findings, or prioritize issues based on runtime evidence.
---

# Correlate Static + Dynamic Findings

Connect static code findings with dynamic runtime observations to prioritize which issues are real vs theoretical.

## Prerequisites

**You MUST run `/agent-inspector:setup` BEFORE proceeding.**

This is NOT optional. The setup command will:
1. Check if agent-inspector is already running
2. Auto-detect your LLM provider (OpenAI/Anthropic)
3. Start the server in background if needed
4. Verify MCP connection is working

**DO NOT skip this step.** If you proceed without running the Preflight Check, MCP tools will fail.

## Correlation States

| State | Meaning | Priority |
|-------|---------|----------|
| **VALIDATED** | Static finding + runtime evidence match | Highest - actively exploitable |
| **UNEXERCISED** | Static finding, never triggered | Test gap, needs coverage |
| **RUNTIME_ONLY** | Dynamic issue, no static counterpart | Different fix approach |
| **THEORETICAL** | Static finding, safe at runtime | Lower priority |

## Correlation Workflow

### 1. Get Workflow State
```
get_agent_workflow_state(agent_workflow_id)
```

Verify both static AND dynamic data exist:
- If `STATIC_ONLY`: Inform user to run dynamic tests first
- If `DYNAMIC_ONLY`: Run /agent-inspector:scan first
- If `COMPLETE`: Proceed with correlation

### 2. Get Static Findings
```
get_findings(agent_workflow_id, status="OPEN")
```

### 3. Get Tool Usage from Runtime
```
get_tool_usage_summary(agent_workflow_id)
```

### 4. Get Correlation Data
```
get_agent_workflow_correlation(agent_workflow_id)
```

### 5. Determine Correlation for Each Finding

**Tool-related findings**: Check if tool was called at runtime
- Tool called -> VALIDATED
- Tool never called -> UNEXERCISED

**Prompt findings**: Check if code path was exercised
- Function/route called at runtime -> VALIDATED
- Never executed -> UNEXERCISED

**Secret/Data findings**: Check if file was loaded at runtime
- File accessed but safe in practice -> THEORETICAL
- Actively used -> VALIDATED

### 6. Update Each Finding
```
update_finding_correlation(finding_id, correlation_state="VALIDATED", correlation_evidence={
  "tool_calls": 47,
  "session_count": 15,
  "runtime_observations": "Tool called 47 times across 15 sessions"
})
```

### 7. Report to User

```
Correlation Complete!

Cross-referenced 5 static findings with 25 runtime sessions.

VALIDATED (2) - Active risks confirmed at runtime:
- Tool without constraints: Called 47 times across 15 sessions
- Hardcoded secret: Used in all sessions

UNEXERCISED (3) - Static risks, never triggered:
- Prompt injection in handle_request(): Code path never executed
- Missing validation in process_input(): Function never called
- Shell command in admin_action(): Admin route never accessed

Prioritize fixing VALIDATED issues first - they're actively exploitable.

To fix the most critical: /agent-inspector:fix REC-001

View correlation in UI: http://localhost:7100/agent-workflow/{id}/static-analysis
```

## Example Scenarios

**Scenario 1: VALIDATED**
```
Static Finding: TOOL_DANGEROUS_UNRESTRICTED in tools.py
- Function: execute_shell()

Runtime Data: execute_shell called 47 times across 15 sessions

Result: VALIDATED
Evidence: "Tool called 47 times in 15 sessions - active risk!"
```

**Scenario 2: UNEXERCISED**
```
Static Finding: PROMPT_INJECT_DIRECT in agent.py
- Function: handle_request()

Runtime Data: No calls to handle_request observed

Result: UNEXERCISED
Evidence: "Code path never executed in 25 sessions - add test coverage"
```

**Scenario 3: THEORETICAL**
```
Static Finding: SECRET_API_KEY in config.py

Runtime Data:
- config.py loaded at runtime
- But environment variable overrides hardcoded value

Result: THEORETICAL
Evidence: "File loaded but value safely overridden by env var"
```

## After Correlation

Suggest next actions based on results:
- VALIDATED issues -> `/agent-inspector:fix REC-XXX`
- UNEXERCISED code -> Add test coverage
- Check gate status -> `/agent-inspector:gate`
