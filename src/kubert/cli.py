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
    """
    Custom Click group that allows both subcommands and direct context switching.

    This class solves two problems:
    1. Allows `kubert dev` (direct context switch) and `kubert setup-shell` (subcommand) syntax
    2. Redirects all help output to stderr to prevent shell eval issues
    """

    def main(self, *args, **kwargs):
        """
        Override main() to redirect help output to stderr.

        This is the cleanest way to ensure ALL help output (including from subcommands,
        exceptions, etc.) goes to stderr instead of stdout, preventing the shell wrapper
        from trying to eval it.
        """
        # Temporarily redirect stdout to stderr for help output
        # We detect help by checking if --help is in sys.argv
        if '--help' in sys.argv or '-h' in sys.argv:
            original_stdout = sys.stdout
            try:
                # Redirect stdout to stderr for help output
                sys.stdout = sys.stderr
                return super().main(*args, **kwargs)
            finally:
                # Restore original stdout
                sys.stdout = original_stdout
        else:
            return super().main(*args, **kwargs)

    def invoke(self, ctx):
        """
        Custom invoke to support both subcommands and direct context switching.

        If the first argument is a known subcommand, use normal group behavior.
        Otherwise, treat it as a context name for direct switching.
        """
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

