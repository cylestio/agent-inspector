# Agent Inspector

Debug, trace, and evaluate agent risk and behavior in real-time.

Agent Inspector gives you instant visibility into your AI agents with ready-to-run profiles for OpenAI and Anthropic. Start a local proxy and live tracing dashboard with a single command.

Ideal for development-time evaluation and for running alongside your test suite (including CI).

## IDE Setup

IDE integration provides MCP query tools for inspecting sessions, risk metrics, and security findings directly in your editor. It also enables static analysis to scan your agent code for vulnerabilities before runtime.

### Claude Code

Register the Cylestio marketplace:

```
/plugin marketplace add cylestio/agent-inspector
```

Then install the plugin:

```
/plugin install agent-inspector@cylestio
```

After installation, restart Claude Code for the MCP connection to activate.

### Cursor

Copy this command to Cursor and it will set everything up for you:

```
Fetch and follow instructions from https://raw.githubusercontent.com/cylestio/agent-inspector/refs/heads/main/integrations/AGENT_INSPECTOR_SETUP.md
```

After setup, restart Cursor and approve the MCP server when prompted.

## Install without IDE Integration

Install via `pipx` (recommended):

```bash
pipx install agent-inspector
agent-inspector openai   # or: anthropic
```

Or run directly with `uvx`:

```bash
uvx agent-inspector openai   # or: anthropic
```

This starts:
- A proxy server on port 4000 (configurable)
- A live trace dashboard on port 7100 (configurable)

### CLI Options

| Flag | Description |
|------|-------------|
| `--port`, `-p` | Override the proxy server port (default: 4000) |
| `--ui-port` | Override the dashboard port (default: 7100) |
| `--base-url` | Override the LLM provider base URL |
| `--use-local-storage` | Enable persistent SQLite storage for traces |
| `--local-storage-path` | Custom database path (requires `--use-local-storage`) |
| `--log-level` | Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `--no-presidio` | Disable Presidio PII detection (enabled by default) |

Point your agent to the proxy:

```python
# OpenAI
client = OpenAI(base_url=f"http://localhost:4000/agent-workflow/{AGENT_WORKFLOW_ID}")

# Anthropic
client = Anthropic(base_url=f"http://localhost:4000/agent-workflow/{AGENT_WORKFLOW_ID}")
```

Replace `AGENT_WORKFLOW_ID` with your project identifier (e.g., derived from your git repo name, package name, or folder name).

Open http://localhost:7100 to view the live dashboard.

## Features

### Security Scanning & Fixes
- Scan your agent code for OWASP LLM Top 10 vulnerabilities
- Get AI-powered, context-aware fixes for security issues
- Track remediation progress with recommendation lifecycle
- Check production deployment readiness with gate status

### Live Tracing & Debugging
- Stream live traces of sessions, tool executions, and messages
- Real-time token usage and duration tracking
- Debug agent sessions with full event replay and timeline
- Health badges and status indicators

### Risk Analytics
Evaluate agent risk across four categories:
- **Resource Management**: Token usage, session duration, and tool call patterns
- **Environment & Supply Chain**: Model versions and tool adoption
- **Behavioral Stability**: Consistency and predictability scoring
- **Privacy & PII**: Automated detection of sensitive data exposure

### PII Detection (Microsoft Presidio)
- Scan prompts, messages, and tool inputs for sensitive data
- Confidence scoring on each finding
- Session-level and aggregate reporting

### Dynamic Runtime Analysis
- Analyze runtime behavior and detect anomalies
- Cross-reference static findings with runtime evidence
- Identify validated issues vs theoretical risks
- Track behavioral patterns and outliers

### Compliance & Reporting
- Generate compliance reports for stakeholders (CISO, executive, customer DD)
- OWASP LLM Top 10 coverage tracking
- SOC2 compliance mapping
- Audit trail for all security fixes

## Dependencies

Agent Inspector is built on:
- [cylestio-perimeter](https://pypi.org/project/cylestio-perimeter/) - Agent monitoring infrastructure
- [Microsoft Presidio](https://microsoft.github.io/presidio/) - PII detection and analysis

## License

Apache License - see [LICENSE](LICENSE) for details
