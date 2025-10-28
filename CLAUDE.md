# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Agent Inspector is a thin CLI wrapper around cylestio-perimeter that provides ready-to-run configurations for OpenAI and Anthropic LLM providers. It's designed for installation via `pipx` or `uvx` to make spinning up the perimeter server a single command.

## Architecture

### Core Components

- **CLI Entry Point** (`agent_inspector/cli.py`): Main Typer-based CLI that handles command parsing, configuration loading, and server launch orchestration
- **Provider Configurations** (`agent_inspector/configs/`): YAML configs for OpenAI and Anthropic providers, each specifying:
  - Server settings (port 3000, host 0.0.0.0, workers)
  - LLM provider base URLs and types
  - Live trace interceptor configuration (port 8080, retention, refresh intervals)
  - Logging configuration

### CLI Workflow

1. User invokes `agent-inspector <provider>` (openai or anthropic)
2. CLI loads the corresponding YAML config from `agent_inspector/configs/`
3. Port overrides are applied if specified via `--port` or `--trace-port`
4. Config is written to a temporary directory
5. The perimeter server is launched by importing and calling `src.main.run()` from cylestio-perimeter
6. Temporary directory is cleaned up on exit

### Key Design Decisions

- **Temporary Config Files**: The CLI writes bundled configs to temp directories before launching perimeter to allow runtime overrides without modifying bundled assets
- **Import-Based Launch**: Instead of subprocess, the CLI imports cylestio-perimeter's `src.main.run()` function directly at cli.py:176
- **Provider Enum**: Uses Python Enum for type-safe provider selection (cli.py:100-108)

## Development Commands

### Installation
```bash
# Install in editable mode
pip install -e .

# Install via pipx (recommended for users)
pipx install .
```

### Running the CLI
```bash
# Launch with OpenAI config (default)
agent-inspector openai

# Launch with Anthropic config
agent-inspector anthropic

# Override ports
agent-inspector openai --port 8000 --trace-port 9090

# View bundled configs
agent-inspector --show-configs

# View sample report
agent-inspector --show-report
```

### Code Quality
This project does not currently have test files, linting configuration, or formatter setup in the repository. Testing is handled upstream in cylestio-perimeter's test suite (specifically `src/interceptors/live_trace/test_pii_analysis.py`).

## Live Trace Interceptor

The bundled configs enable the `live_trace` interceptor which provides:
- Real-time agent/session dashboards with health badges and metrics
- Risk analytics across 4 categories (Resource Management, Environment & Supply Chain, Behavioral Stability, Privacy & PII)
- Microsoft Presidio-powered PII detection
- MinHash-based behavioral clustering and outlier detection
- Session drill-downs with timeline replay

Default ports:
- Perimeter server: 3000
- Live trace dashboard: 8080

## Dependencies

- `typer[all]>=0.12.3`: CLI framework
- `pyyaml>=6.0.1`: YAML config parsing
- `cylestio-perimeter>=1.2.0`: The actual perimeter server implementation

The CLI is a thin launcher; the heavy lifting happens in cylestio-perimeter.
