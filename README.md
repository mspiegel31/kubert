# kubert

Simple tool to allow logging into multiple clusters simultaneously in separate terminal windows/tabs.

## Installation

### Prerequisites

- Python 3.12 or higher
- [UV package manager](https://github.com/astral-sh/uv)
- kubectl
- AWS CLI
- Optional: kops (for kops clusters)
- Optional: chamber (for kops clusters with secrets)

### Install UV

**macOS/Linux:**
```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Or with Homebrew:**
```shell
brew install uv
```

### Install Kubert

**From source:**
```shell
git clone https://github.com/mspiegel31/kubert.git
cd kubert
uv sync
uv pip install -e .
```

**Or install directly with UV:**
```shell
uv tool install kubert
```

### Setup

1. Create your config file at `~/.config/kubert.yaml` (see `example.kubert.yaml`):
   ```shell
   cp example.kubert.yaml ~/.config/kubert.yaml
   # Edit the file with your contexts
   ```

2. **IMPORTANT: Add shell integration** to your shell config file:

   **For Bash** (`~/.bashrc`):
   ```bash
   kubert() {
       eval "$(command kubert "$@")"
   }

   assume-role() {
       eval "$(command assume-role "$@")"
   }
   ```

   **For Zsh** (`~/.zshrc`):
   ```zsh
   kubert() {
       eval "$(command kubert "$@")"
   }

   assume-role() {
       eval "$(command assume-role "$@")"
   }
   ```

   **For Fish** (`~/.config/fish/config.fish`):
   ```fish
   function kubert
       command kubert $argv | source
   end

   function assume-role
       command assume-role $argv | source
   end
   ```

   Then reload your shell:
   ```shell
   source ~/.bashrc  # or ~/.zshrc or restart your terminal
   ```

   > **Why is this needed?** The kubert command prints `export` statements that need to be executed in your current shell. The wrapper function uses `eval` to execute these commands, allowing environment variables like `KUBECONFIG` to persist in your shell session.

3. Ensure kubectl and AWS CLI are installed and configured

## Usage

> **⚠️ IMPORTANT:** Make sure you've completed the [shell integration setup](#setup) above! Without it, `kubert` won't switch your context. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) if you have issues.

### Basic Usage

Switch to a specific context:
```shell
kubert dev
```

```shell
kubert staging
```

Interactive context selection (if no context specified):
```shell
kubert
```

### Assume AWS Role

Select and assume an AWS profile:
```shell
assume-role
```

Or specify a profile directly:
```shell
assume-role my-aws-profile
```

### Shell Integration

For the environment variables to persist in your shell, you need to evaluate the output:

**Bash/Zsh:**
Add to your `~/.bashrc` or `~/.zshrc`:
```shell
kubert() {
    eval "$(command kubert "$@")"
}

assume-role() {
    eval "$(command assume-role "$@")"
}
```

**Fish:**
Add to your `~/.config/fish/config.fish`:
```fish
function kubert
    command kubert $argv | source
end

function assume-role
    command assume-role $argv | source
end
```

### Configuration

The config file at `~/.config/kubert.yaml` defines your contexts. See `example.kubert.yaml` for the format.

You can also set a custom config file location:
```shell
export KUBERT_CONFIG_FILE=/path/to/your/kubert.yaml
```

Or use the `-c` flag:
```shell
kubert -c /path/to/your/kubert.yaml dev
```

## Dependencies

Python packages (automatically installed with UV):
- pyyaml - YAML configuration parsing
- boto3 - AWS SDK for Python
- iterfzf - Python wrapper for fzf (interactive fuzzy finder)

External tools:
- kubectl - Kubernetes command-line tool
- AWS CLI - Amazon Web Services command-line interface
- kops (optional) - Kubernetes Operations tool for kops clusters
- chamber (optional) - Secret management for kops clusters

## Tips

- Use with iTerm profiles (or another terminal) to make opening new K8s tabs even easier
- The tool creates separate kubeconfig files for each context in `~/.kube/<context>.config.yaml`
- Environment variables (AWS_REGION, AWS_SHORT_REGION, CLUSTER, KUBECONFIG) are exported for each context
