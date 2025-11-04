#!/usr/bin/env python3
"""
Kubert CLI Entry Point

Command-line interface for the kubert Kubernetes context switcher.
"""

import sys
from pathlib import Path
from typing import Optional
import click
from .kubert import kubert


@click.command()
@click.argument('context', required=False)
@click.option(
    '-c', '--config',
    type=click.Path(exists=True, path_type=Path),
    envvar='KUBERT_CONFIG_FILE',
    help='Path to kubert config file (default: ~/.config/kubert.yaml)'
)
def main(context: Optional[str], config: Optional[Path]):
    """
    Simple tool to switch between Kubernetes clusters.

    CONTEXT is the Kubernetes context name. If not provided, shows interactive selection.

    Examples:

        kubert dev              # Switch to dev context

        kubert staging          # Switch to staging context

        kubert                  # Interactive context selection
    """
    # Run kubert
    sys.exit(kubert(context, config))


if __name__ == "__main__":
    main()

