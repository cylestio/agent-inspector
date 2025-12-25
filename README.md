# Agent Inspector

Debug, trace, and evaluate agent risk and behavior in real-time.

Agent Inspector gives you instant visibility into your AI agents with ready-to-run profiles for OpenAI and Anthropic. Start a local proxy and live tracing dashboard with a single command.

Ideal for development-time evaluation and for running alongside your test suite (including CI).

## Installation

Install via `pipx` (recommended):

```bash
pipx install agent-inspector
```

Or via `pip`:

```bash
pip install agent-inspector
```

Or run directly with `uvx`:

```bash
uvx agent-inspector
```

## IDE Setup

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

### Manual (Dynamic Analysis Only)

If you just want runtime tracing without the full IDE integration:

```bash
# Start the server
agent-inspector anthropic   # or: openai
```

Point your agent to the proxy:

```python
# OpenAI
client = OpenAI(base_url="http://localhost:4000/v1")

# Anthropic
client = Anthropic(base_url="http://localhost:4000")
```

Open http://localhost:7100 to view the live dashboard.

## Quick Start

Launch Agent Inspector for your provider:

```bash
# For OpenAI
agent-inspector openai

# For Anthropic
agent-inspector anthropic
```

This starts:
- A proxy server on port 4000 (configurable)
- A live trace dashboard on port 7100 (configurable)

Point your AI application to `http://localhost:4000` and start monitoring immediately.

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
