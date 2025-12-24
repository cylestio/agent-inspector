# Run Dynamic Analysis

Trigger on-demand runtime analysis of agent sessions captured through the proxy.

## Purpose

Analyze runtime behavior of your agent across captured sessions to detect:
- Resource management issues (token/tool bounds, variance)
- Environment issues (model pinning, tool coverage)
- Behavioral issues (stability, predictability, outliers)
- Data issues (PII detection at runtime)

## Instructions

1. **Check if analysis can be triggered**:
   ```
   get_dynamic_analysis_status(workflow_id)
   ```
   Verify there are unanalyzed sessions available.

2. **Trigger the analysis**:
   ```
   trigger_dynamic_analysis(workflow_id)
   ```

3. **Wait for completion** - analysis processes only NEW sessions since last run

4. **Report results**:
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

View: http://localhost:7100/agent-workflow/{id}/dynamic-analysis

Next: Run /correlate to cross-reference with static findings
```

## Prerequisites

Your agent must be configured to route traffic through the proxy:

```python
# OpenAI
client = OpenAI(
    api_key="...",
    base_url=f"http://localhost:4000/agent-workflow/{WORKFLOW_ID}"
)

# Anthropic
client = Anthropic(
    api_key="...",
    base_url=f"http://localhost:4000/agent-workflow/{WORKFLOW_ID}"
)
```

Run your agent normally - all LLM calls will be captured as sessions.

## Key Behaviors

- **On-demand only**: Analysis only runs when you trigger it
- **Incremental**: Only processes NEW sessions since last analysis
- **Auto-resolves**: Issues not found in new sessions are auto-resolved
- **Findings persist**: Creates findings and recommendations like static analysis

## Next Steps

- After analysis: Run `/correlate` to cross-reference with static findings
- If issues found: Run `/fix REC-XXX` to address them
- Check gate: Run `/gate` to see production readiness

