---
description: Check production deployment readiness for AI agents. Verify all CRITICAL and HIGH severity issues are resolved. Use when user asks about deployment readiness, gate status, blocking issues, or whether their agent is ready for production.
---

# Production Gate Check

Check if the agent workflow is ready for production deployment. The gate is BLOCKED when there are unresolved CRITICAL or HIGH severity issues.

## Prerequisites

**You MUST run `/agent-inspector:setup` BEFORE proceeding.**

This is NOT optional. The setup command will:
1. Check if agent-inspector is already running
2. Auto-detect your LLM provider (OpenAI/Anthropic)
3. Start the server in background if needed
4. Verify MCP connection is working

**DO NOT skip this step.** If you proceed without running the Preflight Check, MCP tools will fail.

## Gate Workflow

### 1. Get Gate Status
```
get_gate_status(workflow_id)
```

### 2. Report Based on Status

**If BLOCKED:**
```
Production Gate: BLOCKED

Fix these issues to unlock production:

1. REC-001 (CRITICAL): [Title]
   -> /agent-inspector:fix REC-001

2. REC-003 (HIGH): [Title]
   -> /agent-inspector:fix REC-003

Progress: 0/2 blocking issues resolved

Once fixed, the gate will automatically unlock.

View in UI: http://localhost:7100/agent-workflow/{workflow_id}/recommendations
```

**If OPEN:**
```
Production Gate: OPEN

All critical and high security issues have been addressed.
Your agent is ready for production deployment!

Security Summary:
- Total Recommendations: X
- Fixed: Y
- Verified: Z
- Dismissed: W

Generate a compliance report: /agent-inspector:report
http://localhost:7100/agent-workflow/{workflow_id}/reports
```

## Gate Logic

**Gate is BLOCKED** when ANY recommendations with severity CRITICAL or HIGH are:
- PENDING (not yet fixed)
- FIXING (in progress)

**Gate is OPEN** when all CRITICAL/HIGH recommendations are:
- FIXED (fix applied)
- VERIFIED (fix confirmed)
- DISMISSED (risk accepted with reason)
- IGNORED (marked as false positive)

## Example Scenarios

**Scenario: Gate Blocked**
```
User: /agent-inspector:gate

AI:
Production Gate: BLOCKED

Fix these 2 issues to unlock production:

1. REC-001 (CRITICAL): Prompt Injection in agent.py:42
   User input concatenated into system prompt
   -> /agent-inspector:fix REC-001

2. REC-003 (HIGH): Hardcoded API Key in config.py:15
   Secret exposed in source code
   -> /agent-inspector:fix REC-003

Progress: 0 of 2 fixed

To fix the most critical: /agent-inspector:fix REC-001
```

**Scenario: Gate Open**
```
User: /agent-inspector:gate

AI:
Production Gate: OPEN

Your agent is ready for production deployment!

Security Summary:
- Recommendations: 5 total
- Fixed: 3
- Verified: 1
- Dismissed: 1 (risk accepted)

All critical and high severity issues have been addressed.

To generate a report directly, type /agent-inspector:report
```

## After Gate Check

Based on gate status, suggest:
- **BLOCKED**: Start fixing with `/agent-inspector:fix REC-XXX`
- **OPEN**: Generate report with `/agent-inspector:report`
