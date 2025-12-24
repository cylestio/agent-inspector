---
description: Apply intelligent, contextual security fixes to AI agent vulnerabilities. Fix prompt injection, output handling, tool security, data leaks, memory issues, supply chain, and behavioral risks. Use when user says fix, asks to remediate a recommendation (REC-XXX), apply security patches, or resolve vulnerabilities.
---

# Security Fix

Apply intelligent, contextual fixes to security vulnerabilities in AI agent code.

## Prerequisites

**You MUST run `/agent-inspector:setup` BEFORE proceeding.**

This is NOT optional. The setup command will:
1. Check if agent-inspector is already running
2. Auto-detect your LLM provider (OpenAI/Anthropic)
3. Start the server in background if needed
4. Verify MCP connection is working

**DO NOT skip this step.** If you proceed without running the Preflight Check, MCP tools will fail.

## Your Advantage Over Traditional Tools

You're not a template-based fixer. You can:
- Understand the specific vulnerability in context
- Read the codebase and follow its patterns
- Apply intelligent, contextual fixes
- Explain what you changed and why

## Fix Workflow

### With Specific ID: `/agent-inspector:fix REC-XXX`

1. **Get recommendation details**:
   ```
   get_recommendation_detail("REC-XXX")
   ```

2. **Start fix tracking**:
   ```
   start_fix("REC-XXX")
   ```

3. **Understand the vulnerability deeply**:
   - What's the security category? (PROMPT, OUTPUT, TOOL, DATA, MEMORY, SUPPLY, BEHAVIOR)
   - What's the specific risk? How could it be exploited?
   - What's the affected code doing? What's its purpose?

4. **Read and analyze the codebase**:
   - Read the affected file(s) completely
   - Look for similar patterns elsewhere
   - Identify existing validation, sanitization, or security patterns
   - Understand imports, dependencies, and coding style

5. **Design the fix** based on category:

   **For PROMPT issues**:
   - Add input validation (use existing patterns if any)
   - Sanitize/escape user input before prompt interpolation
   - Consider structured inputs (pydantic, dataclasses)
   - Add length limits to prevent context overflow

   **For OUTPUT issues**:
   - Add output encoding appropriate to context (HTML, SQL, shell)
   - Validate agent output before using in dangerous contexts
   - Add escaping when rendering in UI

   **For TOOL issues**:
   - Add permission checks before tool execution
   - Validate tool inputs against allowlist
   - Add constraints (file paths, network hosts, etc.)
   - Implement least-privilege patterns

   **For DATA issues**:
   - Move secrets to environment variables
   - Use secret manager patterns if codebase has them
   - Redact sensitive data from logs
   - Remove hardcoded credentials

   **For MEMORY issues**:
   - Validate retrieved content before use
   - Sanitize context from RAG/vector stores
   - Add bounds on context size
   - Isolate user sessions

   **For SUPPLY CHAIN issues**:
   - Pin dependency versions
   - Add integrity checks for downloads
   - Validate external sources

   **For BEHAVIORAL issues**:
   - Add token/cost limits
   - Implement timeouts
   - Add rate limiting
   - Require human approval for sensitive operations

6. **Apply the fix**:
   - Follow the codebase's existing patterns and style
   - Make minimal changes - fix the vulnerability, don't refactor
   - Preserve existing functionality
   - Add, don't remove (add validation, don't remove features)

7. **Complete the fix**:
   ```
   complete_fix("REC-XXX",
     notes="Clear description of what was fixed and how",
     files_modified=["list", "of", "files.py"])
   ```

8. **Report to user**:
   ```
   Fixed REC-001: Prompt Injection Vulnerability

   **What was the risk?**
   User input was being concatenated directly into the system prompt,
   allowing attackers to inject malicious instructions.

   **What I changed:**
   - Added BookingRequest pydantic model for input validation (agent.py:15-30)
   - Replaced string concatenation with validated, bounded input (agent.py:42)
   - Added sanitization for the preferences field

   **Why this approach?**
   Your codebase already uses pydantic elsewhere, so I followed that pattern.

   **Files modified:** agent.py

   **Next step:** Run /agent-inspector:scan to verify the fix resolved the issue.
   ```

### Without ID: `/agent-inspector:fix`

1. Get open recommendations:
   ```
   get_recommendations(workflow_id, status="PENDING", blocking_only=true)
   ```
2. Pick highest priority (CRITICAL > HIGH)
3. Follow fix flow above

## Fix Quality Checklist

Before completing a fix, verify:
- [ ] Fix follows codebase's existing patterns and style
- [ ] Fix is minimal - only changes what's necessary
- [ ] Fix doesn't break existing functionality
- [ ] Fix handles edge cases (null, empty, unicode, etc.)
- [ ] Explanation is clear to the user

## Recommendation Lifecycle

```
PENDING -> FIXING -> FIXED -> VERIFIED
              |
         DISMISSED/IGNORED
```

## Dismissing a Recommendation

If user wants to dismiss (accept risk):
```
dismiss_recommendation("REC-XXX",
  reason="Explain why this is being dismissed",
  dismiss_type="DISMISSED" or "IGNORED")
```

- **DISMISSED**: Risk accepted - understood but won't fix
- **IGNORED**: False positive - not actually a security issue

## Prioritization Matrix

| Severity | Correlation | Priority | Action |
|----------|-------------|----------|--------|
| CRITICAL | VALIDATED | Immediate | Fix NOW - actively exploitable |
| CRITICAL | UNEXERCISED | High | Fix soon - potential risk |
| HIGH | VALIDATED | High | Fix soon - confirmed at runtime |
| HIGH | UNEXERCISED | Medium | Schedule fix |
| MEDIUM/LOW | Any | Normal | Fix when convenient |
