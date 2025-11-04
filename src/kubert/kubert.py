#!/usr/bin/env python3
"""
Kubert - Kubernetes Context Switcher

This module provides functionality to switch between Kubernetes contexts
and configure kubectl for different EKS and kops clusters.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional
import click
from iterfzf import iterfzf

from .models import KubertConfig


def kubert_context_prompt(config: KubertConfig) -> Optional[str]:
    """
    Interactive context selection using fzf.

    Args:
        config: KubertConfig instance

    Returns:
        Selected context name or None if cancelled
    """
    contexts = config.get_context_names()

    if not contexts:
        print("💩 No contexts found in config file", file=sys.stderr)
        return None

    selected = iterfzf(
        contexts,
        prompt='-> ',
        __extra__=[
            '--height', '50%',
            '--reverse',
            '--select-1',
            '--tiebreak=begin,index',
            '--header', 'Select Kubernetes context'
        ]
    )

    # iterfzf returns str or None
    return str(selected) if selected else None


def kubeswitch(context: str) -> str:
    """
    Switch to a different kubeconfig file.
    
    Args:
        context: Context name
        
    Returns:
        Path to the kubeconfig file
    """
    kube_dir = Path.home() / ".kube"
    kubeconfig_file = kube_dir / f"{context}.config.yaml"
    
    # Create .kube directory if it doesn't exist
    if not kube_dir.exists():
        print(f"~/.kube directory not found. Creating it.")
        kube_dir.mkdir(mode=0o700, exist_ok=True)
    
    # Create kubeconfig file if it doesn't exist
    if not kubeconfig_file.exists():
        print(f"{kubeconfig_file} not found. Creating it.")
        kubeconfig_file.touch(mode=0o600)
    
    print(f"$KUBECONFIG is now {kubeconfig_file}")
    os.environ['KUBECONFIG'] = str(kubeconfig_file)
    
    return str(kubeconfig_file)


def check_current_context() -> bool:
    """
    Check if kubectl has a current context configured.
    
    Returns:
        True if context exists, False otherwise
    """
    try:
        result = subprocess.run(
            ['kubectl', 'config', 'current-context'],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except FileNotFoundError:
        print("💩 kubectl is not installed or not in PATH", file=sys.stderr)
        return False


def update_eks_kubeconfig(cluster: str, region: str, profile: str) -> bool:
    """
    Update kubeconfig for an EKS cluster.
    
    Args:
        cluster: EKS cluster name
        region: AWS region
        profile: AWS profile name
        
    Returns:
        True on success, False on failure
    """
    try:
        cmd = [
            'aws', 'eks', 'update-kubeconfig',
            '--name', cluster,
            '--region', region,
            '--profile', profile
        ]
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout, end='')
        return True
    except subprocess.CalledProcessError as e:
        print(f"💩 Failed to update EKS kubeconfig: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("💩 aws CLI is not installed or not in PATH", file=sys.stderr)
        return False


def update_kops_kubeconfig(profile: str) -> bool:
    """
    Update kubeconfig for a kops cluster.
    
    Args:
        profile: AWS profile name
        
    Returns:
        True on success, False on failure
    """
    try:
        # Set AWS_PROFILE for kops
        os.environ['AWS_PROFILE'] = profile
        
        # Run kops export kubecfg with chamber
        cmd = ['chamber', 'exec', 'kops', '--', 'kops', 'export', 'kubecfg', '--admin=87600h']
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout, end='')
        return True
    except subprocess.CalledProcessError as e:
        print(f"💩 Failed to export kops kubeconfig: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("💩 kops or chamber is not installed or not in PATH", file=sys.stderr)
        return False


def kubert(context: Optional[str] = None, config_file: Optional[Path] = None) -> int:
    """
    Main kubert function to switch Kubernetes contexts.

    Args:
        context: Context name. If None, prompts for selection.
        config_file: Path to config file. If None, uses default.

    Returns:
        0 on success, 1 on failure
    """
    # Load configuration
    try:
        if config_file:
            config = KubertConfig.from_yaml_file(config_file)
        else:
            config = KubertConfig.from_default_location()
    except FileNotFoundError as e:
        click.echo(f"💩 {e}", err=True)
        click.echo("Please create a config file. See example.kubert.yaml for reference", err=True)
        return 1
    except ValueError as e:
        click.echo(f"💩 Invalid config file: {e}", err=True)
        return 1

    # Get context from user if not provided
    if not context:
        context = kubert_context_prompt(config)

    if not context:
        return 1

    # Resolve context values using Pydantic model
    try:
        values = config.resolve_context_values(context)
    except KeyError as e:
        click.echo(f"💩 {e}", err=True)
        return 1

    environment = values["environment"]
    short_region = values["short_region"]
    region = values["region"]
    cluster = values["cluster"]
    aws_profile = values["aws_profile"]
    is_kops = values["is_kops"]

    # Switch kubeconfig
    kubeswitch(context)

    # Handle kops vs EKS clusters
    if is_kops:
        # kops cluster
        success = update_kops_kubeconfig(aws_profile)
    else:
        # EKS cluster - only update if no current context
        if not check_current_context():
            success = update_eks_kubeconfig(cluster, region, aws_profile)
        else:
            success = True

    if not success:
        return 1

    # Export environment variables
    os.environ['AWS_REGION'] = region
    os.environ['AWS_SHORT_REGION'] = short_region
    os.environ['CLUSTER'] = cluster

    # Print export commands for shell integration
    print(f"export AWS_REGION={region}")
    print(f"export AWS_SHORT_REGION={short_region}")
    print(f"export CLUSTER={cluster}")
    print(f"export KUBECONFIG={os.environ['KUBECONFIG']}")

    return 0

