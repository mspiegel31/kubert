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
from typing import Optional, Dict, Any
import yaml
from iterfzf import iterfzf


class KubertConfig:
    """Handles loading and parsing of kubert configuration."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize KubertConfig.
        
        Args:
            config_file: Path to kubert config file. Defaults to ~/.config/kubert.yaml
        """
        if config_file:
            self.config_file = Path(config_file)
        else:
            self.config_file = Path.home() / ".config" / "kubert.yaml"
        
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_file.exists():
            print(f"💩 Config file not found: {self.config_file}", file=sys.stderr)
            print(f"Please create a config file at {self.config_file}", file=sys.stderr)
            print("See example.kubert.yaml for reference", file=sys.stderr)
            sys.exit(1)
        
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def get_defaults(self) -> Dict[str, str]:
        """Get default configuration values."""
        return self.config.get('defaults', {})
    
    def get_contexts(self) -> Dict[str, Dict[str, Any]]:
        """Get all available contexts."""
        return self.config.get('contexts', {})
    
    def get_context(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific context configuration."""
        contexts = self.get_contexts()
        return contexts.get(name)


def kubert_context_prompt(config: KubertConfig) -> Optional[str]:
    """
    Interactive context selection using fzf.
    
    Args:
        config: KubertConfig instance
        
    Returns:
        Selected context name or None if cancelled
    """
    contexts = sorted(config.get_contexts().keys())
    
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
    
    return selected


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


def kubert(context: Optional[str] = None, config_file: Optional[str] = None) -> int:
    """
    Main kubert function to switch Kubernetes contexts.
    
    Args:
        context: Context name. If None, prompts for selection.
        config_file: Path to config file. If None, uses default.
        
    Returns:
        0 on success, 1 on failure
    """
    # Load configuration
    config = KubertConfig(config_file)
    
    # Get context from user if not provided
    if not context:
        context = kubert_context_prompt(config)
    
    if not context:
        return 1
    
    # Get context configuration
    context_config = config.get_context(context)
    if not context_config:
        print(f"💩 Context {context} not found.", file=sys.stderr)
        return 1
    
    # Get defaults
    defaults = config.get_defaults()
    default_short_region = defaults.get('short_region', 'ue1')
    default_region = defaults.get('region', 'us-east-1')
    
    # Extract context settings
    environment = context_config.get('environment')
    aws_profile = context_config.get('aws_profile', '')
    short_region = context_config.get('short_region', default_short_region)
    region = context_config.get('region', default_region)
    cluster = context_config.get('cluster', '')
    
    # Switch kubeconfig
    kubeswitch(context)
    
    # Build cluster name if not specified
    if not cluster:
        cluster = f"spoton-{short_region}-{environment}-eks-cluster"
    
    # Build AWS profile if not specified
    if not aws_profile:
        aws_profile = f"spoton-gbl-{environment}-admin"
    
    # Handle kops vs EKS clusters
    if context.startswith('kops-'):
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

