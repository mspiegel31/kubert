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


class KubertGroup(click.Group):
    """Custom Click group that allows both subcommands and direct context switching."""

    def get_help(self, ctx):
        """Override to send help to stderr instead of stdout (for shell eval compatibility)."""
        help_text = super().get_help(ctx)
        # Print to stderr so it doesn't get eval'd by the shell wrapper
        click.echo(help_text, err=True)
        return ""  # Return empty string so nothing goes to stdout

    def invoke(self, ctx):
        # Check if help was requested - if so, print help to stderr and exit
        # This prevents help text from being sent to stdout where it would be eval'd
        if '--help' in sys.argv or '-h' in sys.argv:
            self.get_help(ctx)
            ctx.exit(0)

        # Get remaining arguments (Click 8.2+: args contains unparsed tokens)
        args = ctx.args

        # If first arg is a known subcommand, use normal group behavior
        if args and args[0] in self.commands:
            return super().invoke(ctx)

        # Otherwise, treat it as a context name and run kubert
        context = args[0] if args else None
        config = ctx.params.get('config')
        sys.exit(kubert(context, config))


@click.group(cls=KubertGroup, invoke_without_command=True)
@click.option(
    '-c', '--config',
    type=click.Path(exists=True, path_type=Path),
    envvar='KUBERT_CONFIG_FILE',
    help='Path to kubert config file (default: ~/.config/kubert.yaml)'
)
@click.pass_context
def main(ctx, config: Optional[Path]):
    """
    Simple tool to switch between Kubernetes clusters.

    Examples:

        kubert dev              # Switch to dev context

        kubert staging          # Switch to staging context

        kubert                  # Interactive context selection

        kubert setup-shell      # Setup shell integration
    """
    # Store config in context for subcommands
    ctx.ensure_object(dict)
    ctx.obj['config'] = config


@main.command('setup-shell')
@click.option('--shell', type=click.Choice(['bash', 'zsh', 'fish']), help='Shell type (auto-detected if not specified)')
@click.option('--yes', '-y', is_flag=True, help='Skip confirmation prompts')
def setup_shell_cmd(shell: Optional[str], yes: bool):
    """Setup shell integration for kubert."""
    from .setup_shell import setup_shell_integration
    sys.exit(setup_shell_integration(shell, yes))


if __name__ == "__main__":
    main()

