"""
Kubert - Kubernetes Context Switcher

Simple tool to allow logging into multiple Kubernetes clusters simultaneously
in separate terminal windows/tabs.
"""

__version__ = "0.1.0"

from .kubert import kubert, kubeswitch
from .assume_role import aws_sdk_assume_role, aws_choose_role
from .models import KubertConfig, Context, Defaults

__all__ = [
    'kubert',
    'kubeswitch',
    'aws_sdk_assume_role',
    'aws_choose_role',
    'KubertConfig',
    'Context',
    'Defaults',
]
