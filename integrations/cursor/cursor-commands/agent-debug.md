# Debug Agent Workflow

Explore captured workflow data to debug issues, investigate behavioral patterns, and identify problems at the agent, session, and event level.

## Purpose

Use this command when:
- Investigating why an agent behaved unexpectedly
- Analyzing patterns across multiple sessions
- Debugging tool execution issues
- Tracing through a specific session

## MCP Tools

| Tool | Purpose |
|------|---------|
| `get_workflow_agents` | List agents with system prompts, session counts |
| `get_workflow_sessions` | Query sessions with filters and pagination |
| `get_session_events` | Get events within a session |
| `get_event` | Get complete details for a single event by ID |

## Instructions

### Step 0: Derive agent_workflow_id

**DO NOT ask the user.** Auto-derive from (priority order):
1. Git remote → repo name (e.g., `github.com/acme/my-agent.git` → `my-agent`)
2. Package name → from `pyproject.toml` or `package.json`
3. Folder name → last path segment

Use the **same `agent_workflow_id`** for ALL commands (scan, analyze, correlate, etc.) to ensure unified results.

### Step 1: Get Workflow Overview

```
get_workflow_agents(agent_workflow_id, include_system_prompts=true)
```

Returns all agents and their last 10 sessions.

### Step 2: Query Sessions

```
get_workflow_sessions(agent_workflow_id, agent_id?, status?, limit=20, offset=0)
```

Filter by:
- `agent_id`: Specific agent
- `status`: ACTIVE, INACTIVE, COMPLETED

### Step 3: Drill Into Events

```
get_session_events(session_id, limit=50, offset=0, event_types?)
```

Event types: `llm.call.start`, `llm.call.finish`, `tool.execution`, `tool.result`

### Step 4: Get Full Event Details

```
get_event(session_id, event_id)
```

Use after identifying an interesting event to retrieve complete data including all attributes, full request/response payloads, and detailed metadata.

### Step 5: Report Findings

```
Debug Summary: {agent_workflow_id}

Investigation Scope:
- Agents examined: N
- Sessions reviewed: N
- Events analyzed: N

Findings:
BEHAVIORAL CONCERNS (N): [list anomalies]

View in dashboard: http://localhost:7100/agent-workflow/{agent_workflow_id}/sessions
```

## Common Scenarios

**List recent sessions:**
```
get_workflow_sessions(agent_workflow_id, status="COMPLETED")
get_session_events(session_id)
```

**Analyze tool usage:**
```
get_session_events(session_id, event_types=["tool.execution", "tool.result"])
```

**Filter LLM calls:**
```
get_session_events(session_id, event_types=["llm.call.start", "llm.call.finish"])
```

## Prerequisites

Your agent must route traffic through the proxy using the **same `agent_workflow_id`**:
```python
# OpenAI
client = OpenAI(base_url=f"http://localhost:4000/agent-workflow/{AGENT_WORKFLOW_ID}")

# Anthropic
client = Anthropic(base_url=f"http://localhost:4000/agent-workflow/{AGENT_WORKFLOW_ID}")
```

Run your agent to generate sessions before debugging.
