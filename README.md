# Agent Inspector

Agent Inspector is a thin CLI wrapper around [cylestio-perimeter](https://pypi.org/project/cylestio-perimeter/) that ships with ready-to-run configurations for OpenAI and Anthropic providers. It is designed for installation via `pipx` or `uvx` and aims to make spinning up the perimeter server a single command away.

## Usage

```bash
agent-inspector openai
# or
agent-inspector anthropic
```

Use `--help` to view all available options including the server and live trace port overrides.

To inspect the bundled configurations without launching the server, run:

```bash
agent-inspector --show-configs
```

Review the latest live trace analytics without launching the server:

```bash
agent-inspector --show-report
```

## Live Trace Test Coverage

The bundled configs enable the `live_trace` interceptor from `cylestio-perimeter`. Its test suite (`src/interceptors/live_trace/test_pii_analysis.py`) exercises the PII analysis pipeline end-to-end:
- Validates how user messages, system prompts, and tool inputs are extracted from session events before inspection.
- Confirms PII detection aggregates findings per session and per entity type using Presidio’s analyzer (mocked in tests).
- Classifies findings into high, medium, and low confidence buckets and ensures summary counters stay accurate.
- Tracks the most common entities encountered and correctly handles edge cases such as empty sessions or filtered results.

These checks help ensure the live trace dashboard surfaces consistent, actionable signals when you run Agent Inspector’s OpenAI or Anthropic profiles.

## Live Trace Overview

For the full feature list see `live_trace.md`, but at a glance the Live Trace dashboard delivers:
- **Real-time dashboards**: Auto-refreshing agent and session views with health badges, duration/token stats, and tool usage tracking.
- **Risk analytics**: Four security categories (Resource Management, Environment & Supply Chain, Behavioral Stability, Privacy & PII) with pass/warn/fail status, evidence, and remediation tips.
- **Behavior insights**: MinHash-based clustering, outlier detection, and stability/predictability scoring so you can spot drifting or risky sessions quickly.
- **PII safeguards**: Microsoft Presidio–powered scanning that logs entity findings (with confidence levels) across user messages, prompts, and tool inputs.
- **Session drill-downs**: Timeline replay of LLM calls, tool executions, errors, and metrics, plus cluster/outlier context for faster triage.
- **Readiness checks**: Clear indicators when the minimum data thresholds (5 sessions for full risk analysis) have not yet been met.
