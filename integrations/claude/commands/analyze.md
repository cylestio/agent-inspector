---
description: Run dynamic runtime analysis on captured AI agent sessions. Analyze token usage, tool calls, behavioral patterns, PII detection, and model pinning. Use when user asks for runtime analysis, dynamic testing, behavioral analysis, or wants to analyze captured agent sessions through the proxy.
---

# Dynamic Runtime Analysis

Analyze runtime sessions captured through the proxy to detect behavioral issues, resource usage patterns, and runtime-only vulnerabilities.

## Prerequisites

**You MUST run `/agent-inspector:setup` BEFORE proceeding.**

This is NOT optional. The setup command will:
1. Check if agent-inspector is already running
2. Auto-detect your LLM provider (OpenAI/Anthropic)
3. Start the server in background if needed
4. Verify MCP connection is working

**DO NOT skip this step.** If you proceed without running the Preflight Check, MCP tools will fail.

## Additional Requirements

1. Agent must send traffic through the proxy:
   ```python
   client = OpenAI(base_url=f"http://localhost:4000/agent-workflow/{AGENT_WORKFLOW_ID}")
   # or
   client = Anthropic(base_url=f"http://localhost:4000/agent-workflow/{AGENT_WORKFLOW_ID}")
   ```
2. At least 1 completed session available

## Analyze Workflow

### 1. Check for Available Sessions
```
get_dynamic_analysis_status(workflow_id)
```

If no sessions available, inform user how to capture them.

### 2. Trigger On-Demand Analysis
```
trigger_dynamic_analysis(workflow_id)
```

This analyzes NEW sessions since last run.

### 3. 16 Security Checks Across 4 Categories

**Resource Management:**
- Token usage bounds and variance
- Tool call frequency limits
- Cost monitoring

**Environment:**
- Model pinning verification
- Tool coverage analysis
- Unused tools inventory

**Behavioral:**
- Response stability
- Outlier detection
- Predictability analysis
- Behavior clustering

**Data:**
- PII detection in prompts
- PII detection in responses
- Sensitive data exposure

### 4. Create Findings & Recommendations

Just like static analysis, dynamic findings generate recommendations with:
- Severity (CRITICAL, HIGH, MEDIUM, LOW)
- Category mapping
- Specific evidence from runtime

### 5. Auto-Resolve Old Issues

Issues not found in new sessions are automatically marked as resolved.

## Report to User

```
Dynamic Analysis Complete!

Analyzed: 25 sessions (15 new since last run)

Resource Checks:
/ Token Usage: Within bounds (avg 2.3k, max 4.1k)
X Tool Calls: Exceeded limit (max 47, limit 20)

Environment Checks:
/ Model Pinning: Using pinned model gpt-4-0613
X Tool Coverage: 3 tools never used

Behavioral Checks:
! Stability: High variance in response patterns
/ Predictability: Consistent behavior across sessions

Data Checks:
/ PII Detection: No PII found in prompts/responses

New Issues: 2
Resolved: 1

View details: http://localhost:7100/agent-workflow/{id}/dynamic-analysis
```

## Key Points

- Analysis is **ON-DEMAND** - only runs when you ask
- Each run analyzes only **NEW sessions** (incremental)
- Results reflect the **current state** of your agent
- Use same agent_workflow_id as static analysis for unified results

## After Analysis

If static data also exists, suggest running correlation:
```
/agent-inspector:correlate
```

This will show which static findings are VALIDATED (confirmed at runtime) vs UNEXERCISED (never triggered).

## Troubleshooting

**No sessions available?**
- Ensure agent uses the proxy base_url
- Run your agent through some test scenarios
- Check http://localhost:7100/agent-workflow/{id}/sessions

**Analysis not finding issues?**
- Run more diverse test scenarios
- Include edge cases and error conditions
- Test with various input types
