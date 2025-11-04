#!/usr/bin/env python3
"""
Kubert CLI Entry Point

Command-line interface for the kubert Kubernetes context switcher.
"""

import sys
import argparse
from pathlib import Path
from .kubert import kubert


def main():
    """Main entry point for the kubert CLI command."""
    parser = argparse.ArgumentParser(
        description='Simple tool to switch between Kubernetes clusters',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  kubert dev              # Switch to dev context
  kubert staging          # Switch to staging context
  kubert                  # Interactive context selection

Environment Variables:
  KUBERT_CONFIG_FILE      Path to kubert config file (default: ~/.config/kubert.yaml)
        """
    )
    
    parser.add_argument(
        'context',
        nargs='?',
        help='Kubernetes context name (if not provided, shows interactive selection)'
    )
    
    parser.add_argument(
        '-c', '--config',
        help='Path to kubert config file',
        default=None
    )
    
    args = parser.parse_args()
    
    # Use config from args, environment, or default
    config_file = args.config or sys.environ.get('KUBERT_CONFIG_FILE')
    
    # Run kubert
    sys.exit(kubert(args.context, config_file))


if __name__ == "__main__":
    main()

