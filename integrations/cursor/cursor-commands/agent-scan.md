# Run AI Agent Security Scan

Run a comprehensive security scan on the current workspace or specified path using Agent Inspector MCP tools.

## Instructions

1. **Register IDE Connection** (if not already registered):
   - Call `register_ide_connection` with:
     - `ide_type`: "cursor"
     - `agent_workflow_id`: derived from the folder name being scanned
     - `workspace_path`: full workspace path
     - `model`: your AI model name (check system prompt for "powered by X")
   - Save the `connection_id` from response
   - Send ONE `ide_heartbeat(connection_id, is_developing=true)`

2. **Create analysis session**:
   - Call `create_analysis_session(agent_workflow_id, session_type="STATIC")`
   - Save the `session_id`

3. **Get security patterns**:
   - Call `get_security_patterns()` to get OWASP LLM Top 10 patterns
   - NEVER hardcode patterns

4. **Analyze ALL code files** for 7 security categories:

   **PROMPT (LLM01)**: User input in prompts, prompt injection, jailbreak vectors
   **OUTPUT (LLM02)**: Agent output in SQL/shell/code, XSS, eval/exec
   **TOOL (LLM07/08)**: Dangerous tools without constraints, missing permissions
   **DATA (LLM06)**: Hardcoded secrets, PII exposure, credentials in logs
   **MEMORY**: RAG poisoning, context injection, unbounded context
   **SUPPLY (LLM05)**: Unpinned dependencies, unvalidated sources
   **BEHAVIOR (LLM08/09)**: No rate limits, unbounded loops, missing approvals

5. **For each finding**, call:
   ```
   store_finding(session_id, file_path, finding_type, severity, title, 
                 category, description, code_snippet, owasp_mapping, cwe, ...)
   ```

6. **Complete session**:
   - Call `complete_analysis_session(session_id)`

7. **Report summary** using format:
   ```
   🔍 AI Security Scan Complete!
   
   Scanned: X files
   
   Security Checks (7):
   ✗ PROMPT Security: X Critical issues
   ✓ DATA Security: Passed
   ...
   
   Gate Status: 🔒 BLOCKED / ✅ OPEN
   
   View: http://localhost:7100/agent-workflow/{id}/static-analysis
   Fix most critical: /fix REC-001
   ```

## Parameters

You can optionally specify a path after the command: `/scan path/to/folder`

If no path specified, scan the current workspace.

## Quality Guidelines

- **DO** find every real security issue
- **DO** use semantic understanding to assess severity
- **DON'T** flag things that aren't exploitable (avoid false positives)
- **DON'T** generate noise like traditional SAST
- **ALWAYS** categorize into one of the 7 security checks

