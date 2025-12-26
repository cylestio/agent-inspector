---
description: Debug AI agent workflows by exploring agents, sessions, and events. Investigate behavioral issues and unexpected patterns. Use when user asks to debug, explore sessions, investigate issues, or examine agent behavior at runtime.
---

# Debug Agent Workflow

Explore captured workflow data to debug issues, investigate behavioral patterns, and identify problems at the agent, session, and event level.

## Prerequisites

**You MUST run `/agent-inspector:setup` BEFORE proceeding.**

This is NOT optional. The setup command will:
1. Check if agent-inspector is already running
2. Auto-detect your LLM provider (OpenAI/Anthropic)
3. Start the server in background if needed
4. Verify MCP connection is working

**DO NOT skip this step.** If you proceed without running setup, MCP tools will fail.

## When to Use This Command

Use `/debug` when:
- Investigating why an agent behaved unexpectedly
- Analyzing patterns across multiple sessions
- Debugging tool execution issues
- Tracing through a specific session

## Workflow Query Tools

| Tool | Purpose |
|------|---------|
| `get_workflow_agents` | List all agents with their system prompts, session counts, and last activity |
| `get_workflow_sessions` | Query sessions with filters (agent, status) and pagination |
| `get_session_events` | Get detailed events within a session with type filtering |
| `get_event` | Get complete details for a single event by ID |

## Debug Workflow

### 1. Derive workflow_id

Auto-derive from (priority order):
1. Git remote: `github.com/acme/my-agent.git` -> `my-agent`
2. Package name: `pyproject.toml` or `package.json`
3. Folder name: `/projects/my-bot` -> `my-bot`

**Do NOT ask the user for workflow_id - derive it automatically.**

### 2. Get Workflow Overview

```
get_workflow_agents(workflow_id, include_system_prompts=true)
```

Returns:
- All agents in the workflow with:
  - Agent ID and display name
  - System prompt (if `include_system_prompts=true`)
  - Total session count
  - Last seen timestamp
- Last 10 sessions across all agents (quick overview)

**Report to user:**
```
Workflow Agents: {workflow_id}

Found {N} agents:

1. {agent_name} (ID: {agent_id})
   Sessions: {count} | Last active: {timestamp}
   System prompt: "{first 100 chars}..."

2. {agent_name} (ID: {agent_id})
   Sessions: {count} | Last active: {timestamp}
   ...

Recent Sessions (last 10):
| Session ID | Agent | Status | Started | Events |
|------------|-------|--------|---------|--------|
| sess_abc... | Agent 1 | COMPLETED | 2 hours ago | 47 |
| sess_def... | Agent 2 | ACTIVE | 5 mins ago | 12 |
...

To drill down: "show me sessions for {agent_name}"
```

### 3. Query Sessions

```
get_workflow_sessions(
  workflow_id,
  agent_id="{optional}",
  status="{optional}",
  limit=20,
  offset=0
)
```

**Session Statuses:**
| Status | Meaning |
|--------|---------|
| ACTIVE | Currently running, receiving events |
| INACTIVE | Paused or idle, may resume |
| COMPLETED | Finished, no more events expected |

**Report to user:**
```
Sessions for {agent_name or workflow_id}:

Showing {N} sessions (page {page}):

| Session ID | Status | Started | Duration | Events |
|------------|--------|---------|----------|--------|
| sess_abc123 | COMPLETED | Dec 15, 2:30pm | 45s | 47 |
| sess_def456 | COMPLETED | Dec 15, 2:15pm | 2m 30s | 128 |
| sess_ghi789 | ACTIVE | Dec 15, 3:00pm | ongoing | 23 |

Sessions currently active: 1

To investigate a session: "show events for sess_def456"
To see more: "next page" or "show sessions offset 20"
```

### 4. Drill Into Session Events

```
get_session_events(
  session_id,
  limit=50,
  offset=0,
  event_types=["llm.call.start", "tool.execution"]
)
```

**Event Types:**
| Type | Description |
|------|-------------|
| `llm.call.start` | LLM API call initiated |
| `llm.call.finish` | LLM response received |
| `tool.execution` | Tool/function called |
| `tool.result` | Tool returned result |

**Report to user:**
```
Session Events: sess_def456

Agent: Customer Support Bot
Status: COMPLETED
Duration: 2m 30s
Total Events: 128

Timeline:
| # | Time | Type | Summary |
|---|------|------|---------|
| 1 | 0.1s | llm.call.start | gpt-4 (tokens: 1.2k) |
| 2 | 1.2s | llm.call.finish | Response received |
| 3 | 1.3s | tool.execution | lookup_booking(user_id="123") |
| 4 | 1.5s | tool.result | Found booking #456 |
...
| 47 | 45s | llm.call.finish | Final response

To filter: "show only tool events"
To see more: "next 50 events"
To get full details: "show event {event_id}"
```

### 5. Get Full Event Details

```
get_event(
  session_id,
  event_id
)
```

Use after identifying an interesting event in `get_session_events` to retrieve complete event data including all attributes.

**Report to user:**
```
Event Details: {event_id}

Session: {session_id}
Type: {event_type}
Time: {timestamp}

Attributes:
- model: gpt-4
- tokens_in: 1234
- tokens_out: 567
- duration_ms: 1250
- ...

Request:
{full request payload}

Response:
{full response payload}

Navigate: "back to session events" or "next event"
```

### 6. Report Debug Summary

After investigation, summarize findings:

```
Debug Summary: {workflow_id}

Investigation Scope:
- Agents examined: 2
- Sessions reviewed: 5
- Events analyzed: 320

Findings:

BEHAVIORAL CONCERNS (1):
1. sess_xyz789: 47 tool calls in single session (unusually high)

Recommendations:
- Add tool call limits per session

Related Commands:
- Run full scan: /agent-inspector:scan
- View in dashboard: http://localhost:7100/agent-workflow/{id}/sessions
```

## Common Debug Scenarios

### Scenario 1: Session Overview

User: "show me recent agent sessions"

```
// 1. Get overview
get_workflow_agents(workflow_id)

// 2. List recent sessions
get_workflow_sessions(workflow_id, status="COMPLETED", limit=20)

// 3. Drill into a session
get_session_events(session_id)
```

### Scenario 2: Behavioral Analysis

User: "why is my agent making so many tool calls"

```
// 1. Get agents and recent sessions
get_workflow_agents(workflow_id)

// 2. Find high-activity sessions
get_workflow_sessions(workflow_id, limit=50)

// 3. Analyze tool patterns in suspicious sessions
get_session_events(session_id, event_types=["tool.execution"])
```

### Scenario 3: Specific Session Deep-Dive

User: "show me what happened in session sess_abc123"

```
// Direct event retrieval
get_session_events("sess_abc123", limit=100)

// Then filter as needed
get_session_events("sess_abc123", event_types=["llm.call.start", "llm.call.finish"])

// Get full details for a specific event
get_event("sess_abc123", "evt_xyz789")
```

## Pagination

The listing tools (`get_workflow_sessions`, `get_session_events`) support pagination:

```
// First page
get_workflow_sessions(workflow_id, limit=20, offset=0)

// Second page
get_workflow_sessions(workflow_id, limit=20, offset=20)

// Third page
get_workflow_sessions(workflow_id, limit=20, offset=40)
```

## Dashboard Integration

After debugging, direct users to the web UI for visual exploration:

| View | URL |
|------|-----|
| All Sessions | http://localhost:7100/agent-workflow/{id}/sessions |
| Specific Session | http://localhost:7100/agent-workflow/{id}/session/{session_id} |
| Agent Details | http://localhost:7100/agent-workflow/{id}/agents |

## Troubleshooting

**No agents found?**
- Ensure dynamic analysis is configured
- Check that agent traffic routes through proxy
- Verify workflow_id matches the base_url used

**No sessions?**
- Run your agent to generate sessions
- Check http://localhost:7100/agent-workflow/{id}/sessions

**Events missing?**
- Events are captured in real-time; wait for session to complete
- Check session status - ACTIVE sessions may still be receiving events
