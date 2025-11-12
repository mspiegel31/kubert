#!/usr/bin/env python3
"""
Shell Integration Setup

Automatically configure shell integration for kubert.
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Optional
import click


BASH_ZSH_INTEGRATION = """
# Kubert shell integration
kubert() {
    eval "$(command kubert "$@")"
}

assume-role() {
    eval "$(command assume-role "$@")"
}
"""

FISH_INTEGRATION = """
# Kubert shell integration
function kubert
    command kubert $argv | source
end

function assume-role
    command assume-role $argv | source
end
"""


def detect_shell() -> str:
    """
    Detect the user's shell.
    
    Returns:
        Shell name (bash, zsh, fish) or empty string if unknown
    """
    shell_path = os.environ.get('SHELL', '')
    shell_name = Path(shell_path).name
    
    if shell_name in ('bash', 'zsh', 'fish'):
        return shell_name
    
    return ''


def get_shell_config_file(shell: str) -> Path:
    """
    Get the config file path for a shell.
    
    Args:
        shell: Shell name (bash, zsh, fish)
        
    Returns:
        Path to shell config file
    """
    home = Path.home()
    
    if shell == 'bash':
        return home / '.bashrc'
    elif shell == 'zsh':
        return home / '.zshrc'
    elif shell == 'fish':
        config_dir = home / '.config' / 'fish'
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / 'config.fish'
    else:
        raise ValueError(f"Unsupported shell: {shell}")


def get_integration_code(shell: str) -> str:
    """
    Get the shell integration code for a shell.
    
    Args:
        shell: Shell name (bash, zsh, fish)
        
    Returns:
        Shell integration code
    """
    if shell in ('bash', 'zsh'):
        return BASH_ZSH_INTEGRATION
    elif shell == 'fish':
        return FISH_INTEGRATION
    else:
        raise ValueError(f"Unsupported shell: {shell}")


def is_already_installed(config_file: Path) -> bool:
    """
    Check if shell integration is already installed.
    
    Args:
        config_file: Path to shell config file
        
    Returns:
        True if already installed, False otherwise
    """
    if not config_file.exists():
        return False
    
    content = config_file.read_text()
    return 'Kubert shell integration' in content or 'kubert shell integration' in content


def backup_config(config_file: Path) -> Path:
    """
    Create a backup of the shell config file.
    
    Args:
        config_file: Path to shell config file
        
    Returns:
        Path to backup file
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = config_file.parent / f"{config_file.name}.backup.{timestamp}"
    
    if config_file.exists():
        backup_file.write_text(config_file.read_text())
        click.echo(f"✅ Backed up existing config to: {backup_file}", err=True)
    
    return backup_file


def add_integration(config_file: Path, integration_code: str) -> None:
    """
    Add shell integration to config file.
    
    Args:
        config_file: Path to shell config file
        integration_code: Shell integration code to add
    """
    # Ensure file exists
    if not config_file.exists():
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.touch()
    
    # Append integration code
    with open(config_file, 'a') as f:
        f.write('\n')
        f.write(integration_code)
    
    click.echo(f"✅ Added shell integration to {config_file}", err=True)


def setup_shell_integration(shell: Optional[str] = None, skip_confirm: bool = False) -> int:
    """
    Setup shell integration for kubert.
    
    Args:
        shell: Shell type (bash, zsh, fish) or None to auto-detect
        skip_confirm: Skip confirmation prompts
        
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    click.echo("=" * 70, err=True)
    click.echo("Kubert Shell Integration Setup", err=True)
    click.echo("=" * 70, err=True)
    click.echo("", err=True)
    
    # Detect or validate shell
    if shell is None:
        shell = detect_shell()
        if not shell:
            click.echo("❌ Could not detect shell", err=True)
            click.echo("", err=True)
            click.echo("Please specify shell type:", err=True)
            click.echo("  kubert setup-shell --shell bash", err=True)
            click.echo("  kubert setup-shell --shell zsh", err=True)
            click.echo("  kubert setup-shell --shell fish", err=True)
            return 1
        
        click.echo(f"Detected shell: {shell}", err=True)
    else:
        click.echo(f"Using shell: {shell}", err=True)
    
    click.echo("", err=True)
    
    # Get config file
    try:
        config_file = get_shell_config_file(shell)
    except ValueError as e:
        click.echo(f"❌ {e}", err=True)
        return 1
    
    click.echo(f"Config file: {config_file}", err=True)
    click.echo("", err=True)
    
    # Check if already installed
    if is_already_installed(config_file):
        click.echo("✅ Shell integration already installed!", err=True)
        click.echo("", err=True)
        click.echo("To reload your shell configuration, run:", err=True)
        click.echo(f"  source {config_file}", err=True)
        return 0
    
    # Get integration code
    integration_code = get_integration_code(shell)
    
    # Show what will be added
    click.echo("This will add the following to your shell config:", err=True)
    click.echo("-" * 70, err=True)
    click.echo(integration_code, err=True)
    click.echo("-" * 70, err=True)
    click.echo("", err=True)
    
    # Confirm
    if not skip_confirm:
        if not click.confirm("Continue?", default=True, err=True):
            click.echo("❌ Cancelled", err=True)
            return 1
        click.echo("", err=True)
    
    # Backup existing config
    backup_config(config_file)
    
    # Add integration
    add_integration(config_file, integration_code)
    
    # Success message
    click.echo("", err=True)
    click.echo("=" * 70, err=True)
    click.echo("Setup Complete! 🎉", err=True)
    click.echo("=" * 70, err=True)
    click.echo("", err=True)
    click.echo("To activate the changes, run:", err=True)
    click.echo(f"  source {config_file}", err=True)
    click.echo("", err=True)
    click.echo("Or restart your terminal.", err=True)
    click.echo("", err=True)
    click.echo("Then test with:", err=True)
    click.echo("  kubert --help", err=True)
    click.echo("  assume-role --help", err=True)
    click.echo("", err=True)
    
    return 0

