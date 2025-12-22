# Correlate Static and Dynamic Findings

Cross-reference static code findings with runtime observations to prioritize which issues are real vs theoretical.

## Purpose

Connect static analysis findings with dynamic runtime data to understand:
- Which code paths are actually exercised
- Which tools are being called
- Whether static findings represent real runtime risks

## Correlation States

- **VALIDATED** 🔴: Static finding confirmed at runtime → **FIX FIRST!**
- **UNEXERCISED** 📋: Static finding, never triggered at runtime → Test gap
- **RUNTIME_ONLY** 🔵: Dynamic issue, no static counterpart → Different fix needed
- **THEORETICAL** 📚: Static finding, but safe at runtime → Lower priority

## Instructions

1. **Get workflow state**:
   ```
   get_agent_workflow_state(agent_workflow_id)
   ```
   Verify BOTH static AND dynamic data exist. If not, inform user what's missing.

2. **Get static findings**:
   ```
   get_findings(agent_workflow_id, status="OPEN")
   ```

3. **Get tool usage from runtime**:
   ```
   get_tool_usage_summary(agent_workflow_id)
   ```

4. **Get correlation data**:
   ```
   get_agent_workflow_correlation(agent_workflow_id)
   ```

5. **For each finding, determine correlation**:
   
   **Tool-related findings**: Check if tool was called at runtime
   - Tool called → VALIDATED
   - Tool never called → UNEXERCISED
   
   **Prompt findings**: Check if code path was exercised
   - Function/route called at runtime → VALIDATED
   - Never executed → UNEXERCISED
   
   **Secret/Data findings**: Check file usage at runtime
   - File accessed but safe in practice → THEORETICAL
   - Actively used → VALIDATED

6. **Update each finding**:
   ```
   update_finding_correlation(finding_id, correlation_state="VALIDATED", 
     correlation_evidence={
       "tool_calls": 47,
       "session_count": 15,
       "runtime_observations": "Tool called 47 times across 15 sessions"
     })
   ```

7. **Report to user**:
   ```
   🔗 Correlation Complete!
   
   Cross-referenced X static findings with Y runtime sessions.
   
   🔴 VALIDATED (N) - Active risks confirmed at runtime:
   - [Title]: [Evidence]
   
   📋 UNEXERCISED (N) - Static risks, never triggered:
   - [Title]: [Evidence]
   
   💡 Prioritize fixing VALIDATED issues first - they're actively exploitable.
   
   To fix most critical: /fix REC-XXX
   
   View: http://localhost:7100/agent-workflow/{id}/static-analysis
   ```

## Prerequisites

- Run `/scan` to get static analysis results
- Route agent traffic through proxy to capture dynamic data:
  ```python
  # OpenAI
  client = OpenAI(base_url=f"http://localhost:4000/agent-workflow/{WORKFLOW_ID}")
  # Anthropic  
  client = Anthropic(base_url=f"http://localhost:4000/agent-workflow/{WORKFLOW_ID}")
  ```

