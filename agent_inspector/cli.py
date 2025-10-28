"""Agent Inspector CLI entry point."""
from __future__ import annotations

import shutil
import tempfile
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional

import typer
import yaml

BANNER = r"""
    ___                 _                _____                     _             
   /   |  ____  _______(_)___  ____ _   / ___/____  ____ ___  ____(_)___  ____ _ 
  / /| | / __ \/ ___/ / / __ \/ __ `/   \__ \/ __ \/ __ `__ \/ __/ / __ \/ __ `/ 
 / ___ |/ /_/ / /  / / / / / / /_/ /   ___/ / /_/ / / / / / / /_/ / / / / /_/ /  
/_/  |_|\____/_/  /_/_/_/ /_/\__, /   /____/\____/_/ /_/ /_/\__/_/_/ /_/\__, /   
                           /____/                                  /____/        
"""

CONFIG_DIR = Path(__file__).resolve().parent / "configs"

STATUS_COLORS = {
    "OK": typer.colors.GREEN,
    "WARN": typer.colors.YELLOW,
    "FAIL": typer.colors.RED,
}

REPORT_DATA = [
    {
        "title": "Resource Management",
        "description": "Summarizes how the agent uses tokens, time, and tools against policy.",
        "metrics": [
            ("Avg. Tokens", "7K"),
            ("Avg. Session Duration", "0.1 min"),
        ],
        "checks": [
            ("Session Duration Consistency", "OK", "CV: 0.22"),
            ("Tool Consistency Across Sessions", "OK", "CV: 0.46"),
            ("Token Consistency Across Sessions", "OK", "CV: 0.23"),
            ("Token Budget Usage", "OK", "8,433 max tokens"),
            ("Tool Call Volume", "OK", "4 max calls"),
        ],
    },
    {
        "title": "Environment & Supply Chain",
        "description": "Examines model version pinning and tool adoption health.",
        "metrics": [
            ("Model", "claude-3-haiku-20240307"),
            ("Avg. Tools Coverage", "0.43"),
            ("Avg. Tool Calls", "2.7"),
            ("Tools", "divide ×8, add ×7, subtract ×4, multiply unused, power unused"),
        ],
        "checks": [
            ("Pinned Model Usage", "OK", "1 pinned model"),
            ("Session Tool Coverage", "WARN", "0.43 coverage"),
            ("Unused Tools Inventory", "WARN", "2 unused tools"),
        ],
    },
    {
        "title": "Behavioral Stability",
        "description": "Summarizes behavioral consistency, predictability, and remaining variance.",
        "checks": [
            ("Behavior Cluster Formation", "OK", "1 cluster"),
            ("Behavior Stability Score", "FAIL", "0.57 score"),
            ("Behavior Outlier Rate", "FAIL", "42% outliers"),
            ("Behavior Predictability", "WARN", "0.57 score"),
            ("Behavioral Uncertainty Level", "WARN", "0.43 uncertainty"),
        ],
    },
    {
        "title": "Privacy & PII Compliance",
        "description": "Microsoft Presidio powered detection of PII exposure in agent streams.",
        "checks": [
            ("PII Detection", "FAIL", "24 findings (16 high-confidence)"),
            ("PII in System Prompts", "OK", "No PII in system prompts"),
            ("PII Exposure Rate", "WARN", "100% sessions with PII"),
        ],
    },
    {
        "title": "Behavioral Insights",
        "description": "Behavioral pattern analysis using MinHash clustering and outlier detection.",
        "metrics": [
            ("Stability Score", "57%"),
            ("Predictability Score", "57%"),
            ("Summary", "Unstable agent with unpredictable behavior - single dominant pattern"),
            ("Outlier Sessions", "3 (IDs: 435a71b8…, 7a4049e2…, 76597661…)"),
            ("Cluster", "cluster_1 (4 sessions, 57.1%) featuring add/divide usage"),
        ],
    },
]

CRITICAL_MESSAGES = [
    "Behavior stability score is 0.57 with 42% outliers.",
    "PII detection flagged 24 findings (16 high-confidence).",
]


class Provider(str, Enum):
    """Supported provider configurations."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"

    def __str__(self) -> str:  # pragma: no cover - improves Typer help output
        return self.value


def _load_config(provider: Provider) -> Dict[str, Any]:
    config_path = CONFIG_DIR / f"{provider.value}.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Missing bundled config: {config_path}")
    with config_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _dump_config(config: Dict[str, Any], destination: Path) -> None:
    with destination.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(config, handle, sort_keys=False)


def _print_banner() -> None:
    typer.echo(typer.style(BANNER, fg=typer.colors.CYAN))
    typer.secho(
        "Agent Inspector helps you debug, inspect, and evaluate agent behaviour and risk.",
        fg=typer.colors.MAGENTA,
    )


def _show_configs() -> None:
    typer.echo(typer.style("Available configurations:\n", fg=typer.colors.GREEN, bold=True))
    for provider in Provider:
        typer.echo(typer.style(f"[{provider.value}]", fg=typer.colors.BRIGHT_BLUE, bold=True))
        config_path = CONFIG_DIR / f"{provider.value}.yaml"
        contents = config_path.read_text(encoding="utf-8")
        typer.echo(contents.rstrip())
        typer.echo("")


def _render_status(label: str, status: str, detail: str) -> str:
    color = STATUS_COLORS.get(status.upper(), typer.colors.WHITE)
    status_text = typer.style(status.upper(), fg=color, bold=True)
    detail_text = f" ({detail})" if detail else ""
    return f"- {label}: {status_text}{detail_text}"


def _show_report() -> None:
    typer.secho("Agent Inspector Report", fg=typer.colors.CYAN, bold=True)
    typer.echo("")
    for section in REPORT_DATA:
        typer.secho(section["title"], fg=typer.colors.BRIGHT_BLUE, bold=True)
        typer.echo(section["description"])
        for metric in section.get("metrics", []):
            typer.secho(f"  • {metric[0]}: {metric[1]}", fg=typer.colors.BRIGHT_BLACK)
        for check in section.get("checks", []):
            typer.echo(_render_status(check[0], check[1], check[2]))
        typer.echo("")
    typer.secho(
        "Use the Live Trace dashboard for deeper drill-down into outliers and PII findings.",
        fg=typer.colors.MAGENTA,
    )


def _print_known_issues() -> None:
    if not CRITICAL_MESSAGES:
        return
    typer.secho("Known issues detected:", fg=typer.colors.RED, bold=True)
    for message in CRITICAL_MESSAGES:
        typer.secho(f"- {message}", fg=typer.colors.RED)
    typer.secho("Run with --show-report for full details.\n", fg=typer.colors.BRIGHT_BLACK)


def _launch_perimeter(config_path: Path) -> None:
    try:
        from src.main import run as perimeter_run
    except ImportError as exc:  # pragma: no cover - fallback if import fails
        typer.secho(
            "Unable to import cylestio-perimeter. Ensure it is installed and available.",
            err=True,
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1) from exc

    perimeter_run(config=str(config_path))


def _cleanup_temp_dir(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)


def _entrypoint(
    provider: Provider = typer.Argument(
        Provider.OPENAI,
        metavar="PROVIDER",
        help="Configuration to load: openai or anthropic",
        show_default=True,
    ),
    port: Optional[int] = typer.Option(
        None,
        "--port",
        "-p",
        min=1,
        max=65535,
        help="Override the perimeter server listening port (defaults to 3000).",
    ),
    live_trace_port: Optional[int] = typer.Option(
        None,
        "--trace-port",
        min=1,
        max=65535,
        help="Override the Live Trace web server port (defaults to 8080).",
    ),
    show_configs: bool = typer.Option(
        False,
        "--show-configs",
        help="Display the bundled configurations and exit.",
    ),
    show_report: bool = typer.Option(
        False,
        "--show-report",
        help="Display the latest behavior, resource, and PII report, then exit.",
    ),
) -> None:
    """Agent Inspector by Cylestio lets you debug, inspect, and evaluate agent behaviour and risk."""

    if show_configs:
        _show_configs()
        raise typer.Exit()

    if show_report:
        _show_report()
        raise typer.Exit()

    config = _load_config(provider)

    if port is not None:
        config.setdefault("server", {})["port"] = port

    if live_trace_port is not None:
        interceptors = config.setdefault("interceptors", [])
        for interceptor in interceptors:
            if interceptor.get("type") == "live_trace":
                interceptor.setdefault("config", {})["server_port"] = live_trace_port
                break
        else:
            typer.secho(
                "Live Trace interceptor not found in config; cannot override trace port.",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(code=1)

    _print_banner()
    _print_known_issues()
    typer.secho(f"Agent Inspector loading the {provider.value} perimeter profile...", fg=typer.colors.GREEN)

    temp_dir = Path(tempfile.mkdtemp(prefix="agent-inspector-"))
    config_path = temp_dir / f"{provider.value}.yaml"

    try:
        _dump_config(config, config_path)
        typer.secho(f"Using config: {config_path}", fg=typer.colors.BRIGHT_BLACK)
        _launch_perimeter(config_path)
    except KeyboardInterrupt:
        typer.echo("")
        typer.secho("Interrupted. Shutting down…", fg=typer.colors.YELLOW)
    finally:
        _cleanup_temp_dir(temp_dir)


def main() -> None:
    """Entry point used by the console script."""
    typer.run(_entrypoint)


if __name__ == "__main__":
    main()
