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

## Usage

### Basic Commands

```bash
# Launch with default settings
agent-inspector openai

# Override ports
agent-inspector openai --port 8000 --trace-port 9090

# View bundled configurations
agent-inspector --show-configs

# Get help
agent-inspector --help
```

### Configuration

Agent Inspector comes with preconfigured profiles for OpenAI and Anthropic. Each profile includes:
- Local proxy settings
- Streaming trace interceptor for real-time analytics
- Sensible logging defaults

## Features

### Live Tracing & Debugging
- Streaming live trace of sessions, tool executions, and messages for instant debugging
- Real-time token usage and duration tracking
- Tool usage monitoring
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

### Session Intelligence
- Step-by-step timeline of model calls and tool executions
- Behavioral pattern analysis and outlier detection
- Deep drill-downs for rapid debugging and triage

## Dependencies

Agent Inspector is built on:
- [cylestio-perimeter](https://pypi.org/project/cylestio-perimeter/) - Agent monitoring infrastructure
- [Microsoft Presidio](https://microsoft.github.io/presidio/) - PII detection and analysis

## License

Apache License - see [LICENSE](LICENSE) for details
