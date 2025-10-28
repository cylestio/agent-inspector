# Agent Inspector

Debug, inspect, and evaluate AI agent behavior and risk in real-time.

Agent Inspector provides instant visibility into your AI agents with ready-to-run configurations for OpenAI and Anthropic. Launch a comprehensive monitoring dashboard with a single command.

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

## Quick Start

Launch Agent Inspector for your provider:

```bash
# For OpenAI
agent-inspector openai

# For Anthropic
agent-inspector anthropic
```

This starts:
- A proxy server on port 3000 (configurable)
- A live trace dashboard on port 8080 (configurable)

Point your AI application to `http://localhost:3000` and start monitoring immediately.

## Usage

### Basic Commands

```bash
# Launch with default settings
agent-inspector openai

# Override ports
agent-inspector openai --port 8000 --trace-port 9090

# View bundled configurations
agent-inspector --show-configs

# View sample analytics report
agent-inspector --show-report

# Get help
agent-inspector --help
```

### Configuration

Agent Inspector comes with pre-configured profiles for OpenAI and Anthropic. Each profile includes:
- Proxy server settings
- Live trace interceptor with real-time analytics
- Optimal logging configuration

## Features

### Real-Time Monitoring
- Auto-refreshing dashboards with agent and session views
- Health badges and status indicators
- Token usage and duration tracking
- Tool usage monitoring

### Risk Analytics
Comprehensive analysis across four categories:
- **Resource Management**: Token usage, session duration, and tool call patterns
- **Environment & Supply Chain**: Model version tracking and tool adoption
- **Behavioral Stability**: Consistency and predictability scoring
- **Privacy & PII**: Automated detection of sensitive data exposure

### PII Detection
- Automatic scanning of user messages, prompts, and tool inputs
- Confidence-level scoring for findings
- Session-level and aggregate reporting

### Session Intelligence
- Timeline replay of LLM calls and tool executions
- Behavioral pattern analysis and outlier detection
- Detailed drill-downs for debugging and triage

## Dependencies

Agent Inspector is built on:
- [cylestio-perimeter](https://pypi.org/project/cylestio-perimeter/) - Agent monitoring infrastructure
- [Microsoft Presidio](https://microsoft.github.io/presidio/) - PII detection and analysis

## License

MIT License - see [LICENSE](LICENSE) for details
