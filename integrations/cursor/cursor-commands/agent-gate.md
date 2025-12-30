# Check Production Gate Status

Check if your agent is ready for production deployment. The gate is BLOCKED when there are unresolved CRITICAL or HIGH severity issues.

## Instructions

### Step 0: Derive agent_workflow_id

**DO NOT ask the user.** Auto-derive from (priority order):
1. Git remote → repo name (e.g., `github.com/acme/my-agent.git` → `my-agent`)
2. Package name → from `pyproject.toml` or `package.json`
3. Folder name → last path segment

Use the **same `agent_workflow_id`** for ALL commands (scan, analyze, correlate, etc.) to ensure unified results.

### Step 1: Get Gate Status

```
get_gate_status(agent_workflow_id)
```

### Step 2: Report Based on Status

**If BLOCKED:**
```
🔒 Production Gate: BLOCKED

Fix these issues to unlock production:

1. REC-XXX (CRITICAL): [Title]
   → /agent-fix REC-XXX

2. REC-YYY (HIGH): [Title]
   → /agent-fix REC-YYY

Progress: ●○○ 0 of N fixed

Once fixed, the gate will automatically unlock.

View: http://localhost:7100/agent-workflow/{agent_workflow_id}/recommendations
```

**If OPEN:**
```
✅ Production Gate: OPEN

All critical and high security issues have been addressed.
Your agent is ready for production deployment!

Security Summary:
- Total Recommendations: X
- Fixed: Y
- Verified: Z
- Dismissed: W

Generate a report: /agent-report

View: http://localhost:7100/agent-workflow/{agent_workflow_id}/reports
```

## Gate Logic

Gate is **BLOCKED** when ANY recommendations with severity CRITICAL or HIGH are:
- PENDING (not yet fixed)
- FIXING (in progress)

Gate is **OPEN** when all CRITICAL/HIGH recommendations are:
- FIXED (fix applied)
- VERIFIED (fix confirmed)
- DISMISSED (risk accepted with documented reason)
- IGNORED (marked as false positive with reason)

## Next Steps

- If BLOCKED: Use `/agent-fix` to address blocking issues
- If OPEN: Use `/agent-report` to generate a compliance report for stakeholders

