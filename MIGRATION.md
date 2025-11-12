# Migration from Bash to Python

This document describes the migration of kubert from Bash scripts to Python.

## Overview

The kubert project has been completely rewritten in Python using the UV package manager. The functionality remains the same, but with improved maintainability, better error handling, and cross-platform compatibility.

## Changes

### Project Structure

**Before (Bash):**
```
kubert/
├── assume-role.bash
├── kubert.bash
├── example.kubert.yaml
└── README.md
```

**After (Python):**
```
kubert/
├── src/
│   └── kubert/
│       ├── __init__.py
│       ├── assume_role.py
│       ├── kubert.py
│       └── cli.py
├── pyproject.toml
├── example.kubert.yaml
├── README.md
└── .gitignore
```

### Dependency Replacements

| Bash Tool | Python Package | Purpose |
|-----------|---------------|---------|
| fzf | iterfzf | Interactive fuzzy finder |
| yq | pyyaml | YAML parsing |
| crudini | configparser (built-in) | INI file parsing |
| aws-cli | boto3 | AWS SDK |

### Command Changes

The commands remain the same, but now they're Python scripts:

**Before:**
```bash
# Source in shell profile
source /path/to/kubert/assume-role.bash
source /path/to/kubert/kubert.bash
```

**After:**
```bash
# Install with UV
uv tool install kubert

# Or add shell functions for environment variable persistence
kubert() {
    eval "$(command kubert "$@")"
}

assume-role() {
    eval "$(command assume-role "$@")"
}
```

### Features

All original features are preserved:

1. ✅ Interactive context selection with fuzzy finding
2. ✅ AWS profile selection and assumption
3. ✅ EKS cluster configuration
4. ✅ kops cluster support
5. ✅ Separate kubeconfig files per context
6. ✅ Environment variable exports (AWS_REGION, CLUSTER, etc.)
7. ✅ YAML configuration file support

### New Features

1. **Better CLI**: Proper argument parsing with `--help` support
2. **Error Handling**: More informative error messages
3. **Cross-Platform**: Works on macOS, Linux, and Windows
4. **Type Safety**: Python type hints for better code quality
5. **Package Management**: Proper dependency management with UV
6. **Installable**: Can be installed as a Python package

## Installation

### Prerequisites

1. Install UV:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Install kubert:
   ```bash
   cd /path/to/kubert
   uv sync
   uv pip install -e .
   ```

### Shell Integration

For environment variables to persist, add to your shell profile:

**Bash/Zsh (~/.bashrc or ~/.zshrc):**
```bash
kubert() {
    eval "$(command kubert "$@")"
}

assume-role() {
    eval "$(command assume-role "$@")"
}
```

**Fish (~/.config/fish/config.fish):**
```fish
function kubert
    command kubert $argv | source
end

function assume-role
    command assume-role $argv | source
end
```

## Configuration

The configuration file format remains unchanged. Your existing `~/.config/kubert.yaml` will work as-is.

## Testing

Test the installation:

```bash
# Test kubert
uv run kubert --help

# Test assume-role
uv run assume-role --help

# Test with your config (if you have one)
uv run kubert dev
```

## Backward Compatibility

The old Bash scripts (`assume-role.bash` and `kubert.bash`) are still in the repository but are no longer maintained. They can be removed once you've migrated to the Python version.

## Troubleshooting

### fzf not found

If you get an error about fzf not being found, make sure fzf is installed on your system:

```bash
# macOS
brew install fzf

# Linux (Debian/Ubuntu)
sudo apt install fzf

# Linux (Fedora/RHEL)
sudo dnf install fzf
```

The `iterfzf` Python package requires the `fzf` binary to be available in your PATH.

### AWS credentials not found

Make sure you have AWS credentials configured:

```bash
aws configure
```

Or ensure `~/.aws/credentials` and `~/.aws/config` exist.

### kubectl not found

Install kubectl:

```bash
# macOS
brew install kubectl

# Linux
# See https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
```

## Benefits of Python Version

1. **Easier to maintain**: Python is more readable and maintainable than Bash
2. **Better error handling**: Proper exception handling and error messages
3. **Cross-platform**: Works on Windows, macOS, and Linux
4. **Testable**: Can write unit tests for the code
5. **Type safety**: Type hints help catch bugs early
6. **Package management**: UV handles dependencies automatically
7. **IDE support**: Better autocomplete and refactoring support

