# Agent Inspector - Claude Code Plugin

AI Agent Security Analysis plugin for Claude Code. Scan, fix, analyze, and report on AI agent vulnerabilities using OWASP LLM Top 10.

## Installation

### Quick Install

1. Clone or copy this plugin folder to your project:
   ```bash
   cp -r claude-code-plugin /path/to/your/project/.claude-plugin
   ```

2. That's it! The plugin will auto-install dependencies and start the server when you open Claude Code.

### Manual Install

If you prefer manual setup:

```bash
# Install agent-inspector
pip install agent-inspector

# Start the server
agent-inspector anthropic
```

## Available Commands

| Command | Description |
|---------|-------------|
| `/setup` | Install, configure, and ensure Agent Inspector is running |
| `/scan` | Run static security scan on your agent code |
| `/fix REC-XXX` | Fix a specific security recommendation |
| `/analyze` | Run dynamic runtime analysis on captured sessions |
| `/correlate` | Cross-reference static findings with runtime data |
| `/gate` | Check production deployment readiness |
| `/report` | Generate security compliance report |
| `/status` | Check dynamic analysis session availability |
| `/debug` | Debug workflow - explore agents, sessions, events |

## Workflow

### 1. Static Analysis
```
/scan
```
Scans your agent code for security issues across 7 OWASP categories.

### 2. Fix Issues
```
/fix REC-001
```
Get AI-assisted fixes for each recommendation.

### 3. Dynamic Analysis (Optional)

Configure your agent to use the proxy:
```python
# OpenAI
client = OpenAI(base_url="http://localhost:4000/agent-workflow/my-agent")

# Anthropic
client = Anthropic(base_url="http://localhost:4000/agent-workflow/my-agent")
```

Run your agent through test scenarios, then:
```
/analyze
```

### 4. Correlate Findings
```
/correlate
```
See which static findings are confirmed at runtime.

### 5. Check Gate
```
/gate
```
Verify all blocking issues are resolved.

### 6. Generate Report
```
/report
```
Get a CISO-ready compliance report.

## Security Categories (OWASP LLM Top 10)

| Category | OWASP Mapping |
|----------|---------------|
| PROMPT | LLM01: Prompt Injection |
| OUTPUT | LLM02: Insecure Output Handling |
| TOOL | LLM05: Improper Plugin Design |
| DATA | LLM06: Sensitive Information Disclosure |
| MEMORY | LLM08: Excessive Agency |
| SUPPLY | LLM03: Training Data Poisoning |
| BEHAVIOR | LLM07: Insecure Plugin Design |

## Web Dashboard

Access the full UI at: http://localhost:7100

## Requirements

- Python 3.8+
- Claude Code CLI
- pip (for installing agent-inspector)

## Troubleshooting

### Server not starting?
```bash
# Check if port 7100 is in use
lsof -i :7100

# Manually start server
agent-inspector anthropic

# Check logs
cat /tmp/agent-inspector.log
```

### No MCP tools available?
1. Ensure server is running: `curl http://localhost:7100/health`
2. Check `.mcp.json` is at project root
3. Restart Claude Code

### Dynamic analysis not capturing sessions?
1. Verify proxy URL in your client configuration
2. Ensure agent-workflow-id matches
3. Check http://localhost:7100/agent-workflow/{id}/sessions

## License

MIT

## Author

[Cylestio](https://github.com/cylestio)
