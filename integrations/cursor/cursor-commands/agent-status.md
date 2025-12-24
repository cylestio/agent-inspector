# Check Dynamic Analysis Status

Get the current status of dynamic analysis including available sessions, analysis state, and whether new analysis can be triggered.

## Instructions

1. **Get dynamic analysis status**:
   ```
   get_dynamic_analysis_status(workflow_id)
   ```

2. **Report the status**:

### If sessions available:
```
📊 Dynamic Analysis Status: {workflow_id}

Sessions Available: X unanalyzed sessions
Last Analysis: {date} or "Never"
Analysis State: READY / NOT_READY

{If READY}
Ready to analyze! Run /analyze to process X new sessions.

{If NOT_READY}
No new sessions since last analysis.
To capture sessions, route agent traffic through proxy:
  base_url="http://localhost:4000/agent-workflow/{workflow_id}"

View sessions: http://localhost:7100/agent-workflow/{id}/sessions
```

### If no sessions:
```
📊 Dynamic Analysis Status: {workflow_id}

Sessions Available: 0
Analysis State: NO_DATA

To capture runtime sessions, configure your agent:

# OpenAI
client = OpenAI(
    base_url=f"http://localhost:4000/agent-workflow/{workflow_id}"
)

# Anthropic
client = Anthropic(
    base_url=f"http://localhost:4000/agent-workflow/{workflow_id}"
)

Then run your agent to generate sessions, and use /analyze.
```

## Additional Information

Also check:
- `get_agent_workflow_state(workflow_id)` - Overall workflow state (STATIC_ONLY, DYNAMIC_ONLY, COMPLETE, NO_DATA)
- `get_analysis_history(workflow_id)` - Past analysis runs

## Next Steps

- If sessions available: Run `/analyze` to process them
- If no sessions: Configure agent to route through proxy, run agent, then `/analyze`
- After analysis: Run `/correlate` to cross-reference with static findings

