# Run Dynamic Analysis

Trigger on-demand runtime analysis of agent sessions captured through the proxy.

## Purpose

Analyze runtime behavior of your agent across captured sessions to detect:
- Resource management issues (token/tool bounds, variance)
- Environment issues (model pinning, tool coverage)
- Behavioral issues (stability, predictability, outliers)
- Data issues (PII detection at runtime)

## Instructions

### Step 0: Derive agent_workflow_id

**DO NOT ask the user.** Auto-derive from (priority order):
1. Git remote → repo name (e.g., `github.com/acme/my-agent.git` → `my-agent`)
2. Package name → from `pyproject.toml` or `package.json`
3. Folder name → last path segment

Use the **same `agent_workflow_id`** for ALL commands (scan, analyze, correlate, etc.) to ensure unified results.

### Step 1: Check Analysis Status

```
get_dynamic_analysis_status(agent_workflow_id)
```
Verify there are unanalyzed sessions available.

### Step 2: Trigger Analysis

```
trigger_dynamic_analysis(agent_workflow_id)
```

### Step 3: Wait for Completion

Analysis processes only NEW sessions since last run.

### Step 4: Report Results
```
🔬 Dynamic Analysis Complete!

Analyzed: X new sessions
Previous issues auto-resolved: Y

Security Checks (4 categories):

📦 Resource Management:
✓ Token Bounds: Within limits
✗ Tool Call Variance: HIGH - inconsistent behavior detected

🔧 Environment:
✓ Model Pinning: Consistent model usage
⚠ Tool Coverage: 2 tools never called

📈 Behavioral:
✓ Stability: Consistent across sessions
✗ Outliers: 3 anomalous sessions detected

🔐 Data:
✓ PII Detection: No PII found in prompts/responses

New Findings: N
Gate Status: 🔒 BLOCKED / ✅ OPEN

View: http://localhost:7100/agent-workflow/{agent_workflow_id}/dynamic-analysis

Next: Run /agent-correlate to cross-reference with static findings
```

## Prerequisites

Your agent must route traffic through the proxy using the **same `agent_workflow_id`** derived in Step 0:

```python
# Use the SAME agent_workflow_id from Step 0

# OpenAI
client = OpenAI(
    api_key="...",
    base_url=f"http://localhost:4000/agent-workflow/{AGENT_WORKFLOW_ID}"
)

# Anthropic
client = Anthropic(
    api_key="...",
    base_url=f"http://localhost:4000/agent-workflow/{AGENT_WORKFLOW_ID}"
)
```

Run your agent normally - all LLM calls will be captured as sessions.

## Key Behaviors

- **On-demand only**: Analysis only runs when you trigger it
- **Incremental**: Only processes NEW sessions since last analysis
- **Auto-resolves**: Issues not found in new sessions are auto-resolved
- **Findings persist**: Creates findings and recommendations like static analysis

## Next Steps

- After analysis: Run `/agent-correlate` to cross-reference with static findings
- If issues found: Run `/agent-fix REC-XXX` to address them
- Check gate: Run `/agent-gate` to see production readiness

