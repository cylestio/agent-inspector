---
description: Check dynamic analysis status and session availability for AI agent security testing. Report session counts, analysis history, and readiness. Use when user asks about status, session availability, analysis readiness, or when dynamic analysis was last run.
---

# Dynamic Analysis Status

Quick check of dynamic analysis availability and session counts.

## Prerequisites

**You MUST run `/agent-inspector:setup` BEFORE proceeding.**

This is NOT optional. The setup command will:
1. Check if agent-inspector is already running
2. Auto-detect your LLM provider (OpenAI/Anthropic)
3. Start the server in background if needed
4. Verify MCP connection is working

**DO NOT skip this step.** If you proceed without running the Preflight Check, MCP tools will fail.

## Status Workflow

### 1. Get Status
```
get_dynamic_analysis_status(workflow_id)
```

### 2. Report Status

```
Dynamic Analysis Status: {workflow_id}

Sessions Available: 25 total
- Analyzed: 20
- Pending: 5

Last Analysis: 2 hours ago
Next Available: Ready (5 new sessions)

To run analysis: /agent-inspector:analyze
```

## Status Fields

| Field | Description |
|-------|-------------|
| **Sessions Available** | Total sessions captured through proxy |
| **Analyzed** | Sessions already processed |
| **Pending** | New sessions awaiting analysis |
| **Last Analysis** | When analysis was last run |
| **Next Available** | Whether new sessions are ready |

## Example Responses

**Sessions Ready:**
```
Dynamic Analysis Status: my-agent

Sessions Available: 25 total
- Analyzed: 20
- Pending: 5

Last Analysis: 2 hours ago
Next Available: Ready (5 new sessions)

To run analysis: /agent-inspector:analyze
```

**No New Sessions:**
```
Dynamic Analysis Status: my-agent

Sessions Available: 20 total
- Analyzed: 20
- Pending: 0

Last Analysis: 30 minutes ago
Next Available: No new sessions

Run your agent to capture more sessions, then try again.
```

**No Sessions Yet:**
```
Dynamic Analysis Status: my-agent

Sessions Available: 0

No sessions have been captured yet.

To capture sessions, configure your agent:

# OpenAI
client = OpenAI(base_url="http://localhost:4000/agent-workflow/my-agent")

# Anthropic
client = Anthropic(base_url="http://localhost:4000/agent-workflow/my-agent")

Then run your agent through test scenarios.
```

## After Status Check

Based on status, suggest next actions:
- **Pending > 0**: Run `/agent-inspector:analyze`
- **Pending = 0**: Run more test scenarios
- **No sessions**: Configure agent base_url
