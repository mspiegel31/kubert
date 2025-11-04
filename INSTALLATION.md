# Installation Guide

Multiple installation methods are available for kubert.

## Quick Install (Recommended)

### Option 1: Automated Install Script

```bash
# Clone the repository
git clone https://github.com/mspiegel31/kubert.git
cd kubert

# Run the install script
./install.sh
```

This will:
1. Install the Python package with uv
2. Automatically add shell integration to your shell config
3. Create a backup of your existing config

Then reload your shell:
```bash
source ~/.bashrc  # or ~/.zshrc
```

### Option 2: Using `setup-shell` Command

```bash
# Install with uv
git clone https://github.com/mspiegel31/kubert.git
cd kubert
uv sync

# Run the setup command
uv run kubert setup-shell
```

This provides an interactive setup that:
- Auto-detects your shell (bash/zsh/fish)
- Shows you what will be added
- Asks for confirmation
- Backs up your existing config
- Adds shell integration

Then reload your shell:
```bash
source ~/.bashrc  # or ~/.zshrc
```

---

## Manual Installation

### Step 1: Install Python Package

```bash
# Clone the repository
git clone https://github.com/mspiegel31/kubert.git
cd kubert

# Install with uv
uv sync
```

### Step 2: Add Shell Integration

**For Bash (~/.bashrc):**
```bash
# Kubert shell integration
kubert() {
    eval "$(command kubert "$@")"
}

assume-role() {
    eval "$(command assume-role "$@")"
}
```

**For Zsh (~/.zshrc):**
```bash
# Kubert shell integration
kubert() {
    eval "$(command kubert "$@")"
}

assume-role() {
    eval "$(command assume-role "$@")"
}
```

**For Fish (~/.config/fish/config.fish):**
```fish
# Kubert shell integration
function kubert
    command kubert $argv | source
end

function assume-role
    command assume-role $argv | source
end
```

### Step 3: Reload Shell

```bash
source ~/.bashrc  # or ~/.zshrc
```

---

## Homebrew Installation (Coming Soon)

Once published to Homebrew:

```bash
# Install from tap
brew tap mspiegel31/kubert
brew install kubert

# Setup shell integration
kubert setup-shell

# Reload shell
source ~/.bashrc  # or ~/.zshrc
```

See [HOMEBREW.md](HOMEBREW.md) for details on Homebrew distribution.

---

## Configuration

After installation, create your config file:

```bash
# Create config directory
mkdir -p ~/.config

# Copy example config
cp example.kubert.yaml ~/.config/kubert.yaml

# Edit with your contexts
vim ~/.config/kubert.yaml
```

Example config:
```yaml
defaults:
  short_region: ue1
  region: us-east-1

contexts:
  dev:
    environment: dev
  
  staging:
    environment: staging
    region: us-west-2
  
  prod:
    environment: prod
    aws_profile: my-prod-profile
```

---

## Verification

Test that everything is working:

```bash
# Check help
kubert --help

# Test context switching
kubert dev

# Verify environment variables
echo $KUBECONFIG
echo $AWS_REGION
echo $CLUSTER

# Check kubectl context
kubectl config current-context
```

---

## Troubleshooting

### Shell Integration Not Working

**Symptom:** Running `kubert dev` doesn't switch context

**Solution:** Make sure you've added the shell integration and reloaded your shell:

```bash
# Check if shell integration is installed
grep -A 5 "kubert shell integration" ~/.bashrc  # or ~/.zshrc

# If not found, run:
kubert setup-shell

# Then reload:
source ~/.bashrc  # or ~/.zshrc
```

### Command Not Found

**Symptom:** `kubert: command not found`

**Solution:** Make sure uv is in your PATH and the package is installed:

```bash
# Check uv is installed
uv --version

# Reinstall if needed
cd /path/to/kubert
uv sync

# Try running with uv directly
uv run kubert --help
```

### Config File Not Found

**Symptom:** `💩 Config file not found`

**Solution:** Create your config file:

```bash
mkdir -p ~/.config
cp example.kubert.yaml ~/.config/kubert.yaml
```

Or specify a custom config location:

```bash
kubert -c /path/to/config.yaml dev
```

Or set environment variable:

```bash
export KUBERT_CONFIG_FILE=/path/to/config.yaml
```

---

## Uninstallation

To remove kubert:

1. **Remove shell integration:**
   ```bash
   # Edit your shell config and remove the kubert section
   vim ~/.bashrc  # or ~/.zshrc
   ```

2. **Remove Python package:**
   ```bash
   cd /path/to/kubert
   rm -rf .venv
   ```

3. **Remove config:**
   ```bash
   rm ~/.config/kubert.yaml
   ```

4. **If installed via Homebrew:**
   ```bash
   brew uninstall kubert
   brew untap mspiegel31/kubert
   ```

---

## Next Steps

- Read [README.md](README.md) for usage examples
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- Check [HOMEBREW.md](HOMEBREW.md) for Homebrew distribution details

