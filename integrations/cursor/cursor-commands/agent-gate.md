# Check Production Gate Status

Check if your agent is ready for production deployment. The gate is BLOCKED when there are unresolved CRITICAL or HIGH severity issues.

## Instructions

1. **Get gate status**:
   ```
   get_gate_status(workflow_id)
   ```

2. **Report based on status**:

### If BLOCKED:
```
🔒 Production Gate: BLOCKED

Fix these issues to unlock production:

1. REC-XXX (CRITICAL): [Title]
   → /fix REC-XXX

2. REC-YYY (HIGH): [Title]
   → /fix REC-YYY

Progress: ●○○ 0 of N fixed

Once fixed, the gate will automatically unlock.

View: http://localhost:7100/agent-workflow/{id}/recommendations
```

### If OPEN:
```
✅ Production Gate: OPEN

All critical and high security issues have been addressed.
Your agent is ready for production deployment!

Security Summary:
- Total Recommendations: X
- Fixed: Y
- Verified: Z
- Dismissed: W

Generate a report: /report

View: http://localhost:7100/agent-workflow/{id}/reports
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

- If BLOCKED: Use `/fix` to address blocking issues
- If OPEN: Use `/report` to generate a compliance report for stakeholders

