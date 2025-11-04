# kubert

Simple tool to allow logging into multiple clusters simultaneously in separate terminal windows/tabs.

## Installation

### Dependencies

Install the required dependencies:

**macOS (Homebrew):**
```shell
brew install fzf yq
pip install crudini
# Optional: for kops clusters
brew install kops
```

**Linux (Debian/Ubuntu):**
```shell
sudo apt install fzf
# Install yq (https://github.com/mikefarah/yq)
sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
sudo chmod +x /usr/local/bin/yq
# Install crudini
sudo apt install crudini
# Optional: for kops clusters
# See https://kops.sigs.k8s.io/getting_started/install/
```

**Linux (Fedora/RHEL):**
```shell
sudo dnf install fzf crudini
# Install yq (https://github.com/mikefarah/yq)
sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
sudo chmod +x /usr/local/bin/yq
# Optional: for kops clusters
# See https://kops.sigs.k8s.io/getting_started/install/
```

### Setup

1. Source the scripts in your shell profile (`~/.bashrc` or `~/.zshrc`):
   ```shell
   source /path/to/kubert/assume-role.bash
   source /path/to/kubert/kubert.bash
   ```

2. Create your config file at `~/.config/kubert.yaml` (see `example.kubert.yaml`)

## Example usage

```shell
kubert dev
```

```shell
kubert staging
```

## Dependencies

- crudini
- fzf
- kops (if you want to connect to kops clusters)

## Tips

Use with iTerm profiles (or another terminal) to make opening new K8s tab even easier.
