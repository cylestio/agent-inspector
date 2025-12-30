"""Agent Inspector CLI entry point."""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional

import typer
import yaml

BANNER = r"""
    _                    _     ___                           _             
   / \   __ _  ___ _ __ | |_  |_ _|_ __  ___ _ __   ___  ___| |_ ___  _ __ 
  / _ \ / _` |/ _ \ '_ \| __|  | || '_ \/ __| '_ \ / _ \/ __| __/ _ \| '__|
 / ___ \ (_| |  __/ | | | |_   | || | | \__ \ |_) |  __/ (__| || (_) | |   
/_/   \_\__, |\___|_| |_|\__| |___|_| |_|___/ .__/ \___|\___|\__\___/|_|   
        |___/                               |_|                            
"""

CONFIG_DIR = Path(__file__).resolve().parent / "configs"


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


def _launch_perimeter(config_path: Path) -> None:
    """Launch cylestio-perimeter using Python module execution.

    Uses sys.executable to ensure we run with the same Python interpreter,
    which is critical for pipx installations where the cylestio-perimeter
    CLI is not on the system PATH but is installed in the same venv.
    """
    import sys

    try:
        subprocess.run(
            [sys.executable, "-m", "src.main", "run", "--config", str(config_path)],
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        typer.secho(
            f"Perimeter exited with error code {exc.returncode}",
            err=True,
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=exc.returncode) from exc
    except FileNotFoundError as exc:
        typer.secho(
            "Unable to launch cylestio-perimeter. Ensure it is installed and available.",
            err=True,
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1) from exc


def _cleanup_temp_dir(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)


app = typer.Typer()


@app.command()
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
        help="Override the perimeter server listening port (defaults to 4000).",
    ),
    live_trace_port: Optional[int] = typer.Option(
        None,
        "--trace-port",
        min=1,
        max=65535,
        help="Override the Live Trace web server port (defaults to 7100).",
    ),
    use_local_storage: bool = typer.Option(
        False,
        "--use-local-storage",
        help="Enable local SQLite storage for live trace (default path: ./agent-inspector-trace.db).",
    ),
    storage_db_path: Optional[str] = typer.Option(
        None,
        "--local-storage-path",
        help="Custom database path for local storage (requires --use-local-storage).",
    ),
    show_configs: bool = typer.Option(
        False,
        "--show-configs",
        help="Display the bundled configurations and exit.",
    ),
) -> None:
    """Agent Inspector by Cylestio lets you debug, inspect, and evaluate agent behaviour and risk."""

    if show_configs:
        _show_configs()
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

    if use_local_storage:
        db_path = storage_db_path if storage_db_path else "./agent-inspector-trace.db"
        interceptors = config.setdefault("interceptors", [])
        for interceptor in interceptors:
            if interceptor.get("type") == "live_trace":
                interceptor.setdefault("config", {})["storage_mode"] = "sqlite"
                interceptor["config"]["db_path"] = db_path
                break
        else:
            typer.secho(
                "Live Trace interceptor not found in config; cannot set local storage.",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(code=1)

    _print_banner()
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
    app()


if __name__ == "__main__":
    main()
