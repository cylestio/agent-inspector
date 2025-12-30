# Check Dynamic Analysis Status

Get the current status of dynamic analysis including available sessions, analysis state, and whether new analysis can be triggered.

## Instructions

### Step 0: Derive agent_workflow_id

**DO NOT ask the user.** Auto-derive from (priority order):
1. Git remote → repo name (e.g., `github.com/acme/my-agent.git` → `my-agent`)
2. Package name → from `pyproject.toml` or `package.json`
3. Folder name → last path segment

Use the **same `agent_workflow_id`** for ALL commands (scan, analyze, correlate, etc.) to ensure unified results.

### Step 1: Get Status

```
get_dynamic_analysis_status(agent_workflow_id)
```

### Step 2: Report Status

**If sessions available:**
```
📊 Dynamic Analysis Status: {agent_workflow_id}

Sessions Available: X unanalyzed sessions
Last Analysis: {date} or "Never"
Analysis State: READY / NOT_READY

{If READY}
Ready to analyze! Run /agent-analyze to process X new sessions.

{If NOT_READY}
No new sessions since last analysis.
To capture sessions, route agent traffic through proxy:
  base_url="http://localhost:4000/agent-workflow/{agent_workflow_id}"

View sessions: http://localhost:7100/agent-workflow/{agent_workflow_id}/sessions
```

**If no sessions:**
```
📊 Dynamic Analysis Status: {agent_workflow_id}

Sessions Available: 0
Analysis State: NO_DATA

To capture runtime sessions, configure your agent with the SAME agent_workflow_id:

# OpenAI
client = OpenAI(
    base_url=f"http://localhost:4000/agent-workflow/{AGENT_WORKFLOW_ID}"
)

# Anthropic
client = Anthropic(
    base_url=f"http://localhost:4000/agent-workflow/{AGENT_WORKFLOW_ID}"
)

Then run your agent to generate sessions, and use /agent-analyze.
```

## Additional Information

Also check:
- `get_agent_workflow_state(agent_workflow_id)` - Overall workflow state (STATIC_ONLY, DYNAMIC_ONLY, COMPLETE, NO_DATA)
- `get_analysis_history(agent_workflow_id)` - Past analysis runs

## Next Steps

- If sessions available: Run `/agent-analyze` to process them
- If no sessions: Configure agent to route through proxy, run agent, then `/agent-analyze`
- After analysis: Run `/agent-correlate` to cross-reference with static findings

