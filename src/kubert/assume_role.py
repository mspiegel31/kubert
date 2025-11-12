#!/usr/bin/env python3
"""
AWS Profile Assumption Module

This module provides functionality to select and assume AWS profiles
using interactive fuzzy finding (fzf replacement).
"""

import os
import sys
from pathlib import Path
from configparser import ConfigParser
from typing import Optional, List
import click
from iterfzf import iterfzf


def get_aws_profiles() -> List[str]:
    """
    Read AWS profiles from both credentials and config files.
    
    Returns:
        List of profile names
    """
    profiles = set()
    
    # Read credentials file
    credentials_file = Path.home() / ".aws" / "credentials"
    if credentials_file.exists():
        config = ConfigParser()
        config.read(credentials_file)
        profiles.update(config.sections())
    
    # Read config file
    config_file = Path.home() / ".aws" / "config"
    if config_file.exists():
        config = ConfigParser()
        config.read(config_file)
        for section in config.sections():
            # Remove 'profile ' prefix if present
            profile_name = section.replace('profile ', '')
            profiles.add(profile_name)
    
    return sorted(list(profiles))
    
def aws_choose_role(namespace: Optional[str] = "spoton", stage: Optional[str] = None) -> Optional[str]:
    """
    Interactive AWS profile selection using fzf.
    
    Args:
        namespace: Default namespace for query filtering
        stage: Optional stage for query filtering
        
    Returns:
        Selected profile name or None if cancelled
    """
    profiles = get_aws_profiles()
    
    if not profiles:
        print("No AWS profiles found in ~/.aws/credentials or ~/.aws/config", file=sys.stderr)
        return None
    
    # Build query string for filtering
    query_parts = []
    if namespace:
        query_parts.append(namespace)
    if stage:
        query_parts.append(stage)
    query = "-".join(query_parts) if query_parts else ""
    
    # Use iterfzf for interactive selection
    selected = iterfzf(
        profiles,
        prompt='-> ',
        query=query,
        __extra__=[
            '--height', '30%',
            '--reverse',
            '--select-1',
            '--tiebreak=begin,index',
            '--header', 'Select AWS profile'
        ]
    )

    # iterfzf returns str or None
    return str(selected) if selected else None


def aws_sdk_assume_role(role: Optional[str] = None) -> int:
    """
    Assume an AWS role by setting the AWS_PROFILE environment variable.
    
    Args:
        role: Profile name to assume. If None, prompts for selection.
        
    Returns:
        0 on success, 1 on failure
    """
    if not role:
        role = aws_choose_role()
    
    if not role:
        print("Usage: assume-role <role>", file=sys.stderr)
        return 1
    
    # Set AWS_PROFILE environment variable
    os.environ['AWS_PROFILE'] = role
    
    # Print export command for shell integration
    print(f"export AWS_PROFILE={role}")
    
    return 0


@click.command()
@click.argument('role', required=False)
@click.option(
    '--namespace',
    envvar='NAMESPACE',
    default='spoton',
    help='Namespace for filtering profiles'
)
@click.option(
    '--stage',
    envvar='STAGE',
    help='Stage for filtering profiles'
)
def main(role: Optional[str], namespace: str, stage: Optional[str]):
    """
    Assume an AWS role by setting AWS_PROFILE.

    ROLE is the AWS profile name. If not provided, shows interactive selection.

    Examples:

        assume-role                    # Interactive profile selection

        assume-role my-profile         # Assume specific profile
    """
    sys.exit(aws_sdk_assume_role(role))


if __name__ == "__main__":
    main()

