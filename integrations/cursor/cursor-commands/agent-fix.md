# Fix Security Recommendation

Fix a specific security recommendation using AI-powered contextual fixes, or fix the highest priority blocking issue.

## Instructions

### Step 0: Derive agent_workflow_id

**DO NOT ask the user.** Auto-derive from (priority order):
1. Git remote → repo name (e.g., `github.com/acme/my-agent.git` → `my-agent`)
2. Package name → from `pyproject.toml` or `package.json`
3. Folder name → last path segment

Use the **same `agent_workflow_id`** for ALL commands (scan, analyze, correlate, etc.) to ensure unified results.

### With specific ID: `/agent-fix REC-XXX`

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
   - What's the specific risk and how could it be exploited?
   - What is the affected code doing?

4. **Read and analyze the codebase**:
   - Read the affected file(s) completely
   - Look for similar patterns - how are similar things handled?
   - Identify existing validation, sanitization, or security patterns
   - Understand coding style and conventions

5. **Design the fix by category**:

   **PROMPT**: Add input validation, sanitize before interpolation, use structured inputs
   **OUTPUT**: Add output encoding, validate before dangerous contexts, escape in UI
   **TOOL**: Add permission checks, validate inputs, implement allowlists
   **DATA**: Move secrets to env vars, redact from logs, remove hardcoded creds
   **MEMORY**: Validate retrieved content, sanitize RAG sources, bound context size
   **SUPPLY**: Pin versions, add integrity checks, validate external sources
   **BEHAVIOR**: Add token/cost limits, timeouts, rate limiting, approval gates

6. **Apply the fix**:
   - Follow codebase's existing patterns and style
   - Make minimal changes - fix the vulnerability, don't refactor
   - Preserve existing functionality
   - Add validation, don't remove features

7. **Complete the fix**:
   ```
   complete_fix("REC-XXX", 
     notes="Description of what was fixed and how", 
     files_modified=["list", "of", "files.py"])
   ```

8. **Report to user**:
   ```
   ✅ Fixed REC-XXX: [Title]
   
   **What was the risk?**
   [Explain the vulnerability]
   
   **What I changed:**
   - [List of changes with file:line references]
   
   **Why this approach?**
   [Explain why this fix was chosen]
   
   **Files modified:** [list]
   
   **Next step:** Run /agent-scan to verify
   ```

### Without ID: `/agent-fix`

1. Get open recommendations:
   ```
   get_recommendations(agent_workflow_id, status="PENDING", blocking_only=true)
   ```

2. Pick highest priority (CRITICAL > HIGH > MEDIUM > LOW)

3. Follow the fix flow above

## Dismissing a Recommendation

If the issue should be dismissed (accepted risk or false positive):
```
dismiss_recommendation("REC-XXX", 
  reason="Explain why this is being dismissed",
  dismiss_type="DISMISSED" or "IGNORED")
```

- **DISMISSED**: Risk accepted - understood but won't fix
- **IGNORED**: False positive - not actually a security issue

## Fix Quality Checklist

Before completing, verify:
- [ ] Fix follows codebase's existing patterns and style
- [ ] Fix is minimal - only changes what's necessary  
- [ ] Fix doesn't break existing functionality
- [ ] Fix handles edge cases (null, empty, unicode, etc.)
- [ ] Explanation is clear to the user

