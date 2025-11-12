#!/usr/bin/env python3
"""
Pydantic models for kubert configuration.

These models provide type-safe validation and parsing of the kubert.yaml
configuration file.
"""

from pathlib import Path
from typing import Dict, Optional
from pydantic import BaseModel, Field, field_validator
import yaml


class Defaults(BaseModel):
    """Default configuration values."""
    
    short_region: str = Field(
        default="ue1",
        description="Default short region code (e.g., ue1, uw2)"
    )
    region: str = Field(
        default="us-east-1",
        description="Default AWS region (e.g., us-east-1, us-west-2)"
    )


class Context(BaseModel):
    """Configuration for a single Kubernetes context."""
    
    environment: str = Field(
        description="Environment name (e.g., dev, staging, prod)"
    )
    aws_profile: Optional[str] = Field(
        default=None,
        description="AWS profile to use for this context"
    )
    short_region: Optional[str] = Field(
        default=None,
        description="Short region code override"
    )
    region: Optional[str] = Field(
        default=None,
        description="AWS region override"
    )
    cluster: Optional[str] = Field(
        default=None,
        description="Cluster name override"
    )
    
    @field_validator('environment')
    @classmethod
    def environment_not_empty(cls, v: str) -> str:
        """Validate that environment is not empty."""
        if not v or not v.strip():
            raise ValueError("environment cannot be empty")
        return v.strip()


class KubertConfig(BaseModel):
    """Root configuration model for kubert.yaml."""
    
    defaults: Defaults = Field(
        default_factory=Defaults,
        description="Default configuration values"
    )
    contexts: Dict[str, Context] = Field(
        default_factory=dict,
        description="Map of context names to context configurations"
    )
    
    @field_validator('contexts')
    @classmethod
    def contexts_not_empty(cls, v: Dict[str, Context]) -> Dict[str, Context]:
        """Validate that at least one context is defined."""
        if not v:
            raise ValueError("At least one context must be defined")
        return v
    
    @classmethod
    def from_yaml_file(cls, path: Path | str) -> "KubertConfig":
        """
        Load configuration from a YAML file.

        Args:
            path: Path to the YAML configuration file

        Returns:
            Parsed and validated KubertConfig instance

        Raises:
            FileNotFoundError: If the config file doesn't exist
            ValueError: If the YAML is invalid or validation fails
        """
        path = Path(path) if isinstance(path, str) else path

        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        with open(path, 'r') as f:
            data = yaml.safe_load(f)

        if not data:
            raise ValueError(f"Config file is empty: {path}")

        return cls.model_validate(data)
    
    @classmethod
    def from_default_location(cls) -> "KubertConfig":
        """
        Load configuration from the default location (~/.config/kubert.yaml).
        
        Returns:
            Parsed and validated KubertConfig instance
            
        Raises:
            FileNotFoundError: If the config file doesn't exist
            ValueError: If the YAML is invalid or validation fails
        """
        default_path = Path.home() / ".config" / "kubert.yaml"
        return cls.from_yaml_file(default_path)
    
    def get_context(self, name: str) -> Optional[Context]:
        """
        Get a specific context by name.
        
        Args:
            name: Context name
            
        Returns:
            Context configuration or None if not found
        """
        return self.contexts.get(name)
    
    def get_context_names(self) -> list[str]:
        """
        Get all context names.
        
        Returns:
            Sorted list of context names
        """
        return sorted(self.contexts.keys())
    
    def resolve_context_values(self, context_name: str) -> Dict[str, str]:
        """
        Resolve all values for a context, applying defaults where needed.
        
        Args:
            context_name: Name of the context
            
        Returns:
            Dictionary with resolved values
            
        Raises:
            KeyError: If context doesn't exist
        """
        context = self.contexts.get(context_name)
        if not context:
            raise KeyError(f"Context '{context_name}' not found")
        
        # Apply defaults
        short_region = context.short_region or self.defaults.short_region
        region = context.region or self.defaults.region
        environment = context.environment
        
        # Build cluster name if not specified
        cluster = context.cluster
        if not cluster:
            cluster = f"spoton-{short_region}-{environment}-eks-cluster"
        
        # Build AWS profile if not specified
        aws_profile = context.aws_profile
        if not aws_profile:
            aws_profile = f"spoton-gbl-{environment}-admin"
        
        return {
            "environment": environment,
            "short_region": short_region,
            "region": region,
            "cluster": cluster,
            "aws_profile": aws_profile,
            "is_kops": context_name.startswith("kops-"),
        }

