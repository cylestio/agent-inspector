# Debug Agent Workflow

Explore captured workflow data to debug issues, investigate behavioral patterns, and identify problems at the agent, session, and event level.

## Purpose

Use this command when:
- Investigating why an agent behaved unexpectedly
- Looking for errors or failures in agent sessions
- Checking for PII exposure in agent interactions
- Analyzing patterns across multiple sessions
- Debugging tool execution issues

## MCP Tools

| Tool | Purpose |
|------|---------|
| `get_workflow_agents` | List agents with system prompts, session counts |
| `get_workflow_sessions` | Query sessions with filters and pagination |
| `get_session_events` | Get events within a session |

## Instructions

### 1. Get Workflow Overview

```
get_workflow_agents(workflow_id, include_system_prompts=true)
```

Returns all agents and their last 10 sessions.

### 2. Query Sessions

```
get_workflow_sessions(workflow_id, agent_id?, status?, limit=20, offset=0)
```

Filter by:
- `agent_id`: Specific agent
- `status`: ACTIVE, INACTIVE, COMPLETED

### 3. Drill Into Events

```
get_session_events(session_id, limit=50, offset=0, event_types?)
```

Event types: `llm.call.start`, `llm.call.complete`, `tool.execution`, `tool.error`, `pii.detected`, etc.

### 4. Report Findings

```
Debug Summary: {workflow_id}

Investigation Scope:
- Agents examined: N
- Sessions reviewed: N
- Events analyzed: N

Findings:
ERRORS (N): [list errors with session/event references]
PII EXPOSURE (N): [list PII detections]
BEHAVIORAL CONCERNS (N): [list anomalies]

View in dashboard: http://localhost:7100/agent-workflow/{id}/sessions
```

## Common Scenarios

**Find errors:**
```
get_workflow_sessions(workflow_id, status="COMPLETED")
get_session_events(session_id, event_types=["error", "tool.error", "llm.call.error"])
```

**Check for PII:**
```
get_session_events(session_id, event_types=["pii.detected"])
```

**Analyze tool usage:**
```
get_session_events(session_id, event_types=["tool.execution"])
```

## Prerequisites

Your agent must route traffic through the proxy:
```python
# OpenAI
client = OpenAI(base_url=f"http://localhost:4000/agent-workflow/{WORKFLOW_ID}")

# Anthropic
client = Anthropic(base_url=f"http://localhost:4000/agent-workflow/{WORKFLOW_ID}")
```

Run your agent to generate sessions before debugging.
