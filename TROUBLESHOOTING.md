# Troubleshooting Guide

## Problem: `kubert` doesn't switch my kubectl context

### Symptoms
- Running `kubert ue1-staging` completes without errors
- But `kubectl config current-context` still shows the old context
- `echo $KUBECONFIG` is empty or shows the old value

### Cause
You're missing the **shell integration** wrapper function.

### Solution

You need to add a shell wrapper function that uses `eval` to execute the export commands in your current shell.

#### Quick Fix (Test Immediately)

```bash
# Test with eval directly
eval "$(uv run kubert ue1-staging)"

# Verify it worked
echo $KUBECONFIG
kubectl config current-context
```

#### Permanent Fix (Recommended)

**Option 1: Automated Setup**

```bash
./setup_shell_integration.sh
source ~/.bashrc  # or ~/.zshrc
```

**Option 2: Manual Setup**

Add this to your `~/.bashrc` or `~/.zshrc`:

```bash
kubert() {
    eval "$(command kubert "$@")"
}

assume-role() {
    eval "$(command assume-role "$@")"
}
```

Then reload:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

### Why This Is Needed

When you run `kubert ue1-staging` directly:
1. ✅ Python script runs
2. ✅ Sets `KUBECONFIG` in the Python process
3. ✅ Prints `export KUBECONFIG=...`
4. ❌ Your shell **doesn't execute** those export commands

The environment variables only exist in the Python process, not your shell!

The wrapper function uses `eval` to execute the export commands in your current shell, making the environment variables persist.

---

## Problem: `fzf` not found or interactive selection doesn't work

### Symptoms
- Error: `fzf: command not found`
- Interactive selection doesn't appear
- Error about `iterfzf`

### Solution

Install `fzf`:

**macOS:**
```bash
brew install fzf
```

**Ubuntu/Debian:**
```bash
sudo apt-get install fzf
```

**Arch Linux:**
```bash
sudo pacman -S fzf
```

---

## Problem: Config file not found

### Symptoms
```
💩 Config file not found: /Users/mike/.config/kubert.yaml
Please create a config file. See example.kubert.yaml for reference
```

### Solution

Create your config file:

```bash
# Create config directory
mkdir -p ~/.config

# Copy example config
cp example.kubert.yaml ~/.config/kubert.yaml

# Edit with your contexts
vim ~/.config/kubert.yaml
```

Or specify a custom config file:

```bash
kubert -c /path/to/my-config.yaml dev
```

Or use environment variable:

```bash
export KUBERT_CONFIG_FILE=/path/to/my-config.yaml
kubert dev
```

---

## Problem: Invalid config file / Validation errors

### Symptoms
```
💩 Invalid config file: 1 validation error for Context
environment
  Field required
```

### Cause
Your YAML config is missing required fields or has invalid structure.

### Solution

Check your config file against the example:

**Required fields:**
- Each context MUST have an `environment` field
- At least one context must be defined

**Example valid config:**
```yaml
defaults:
  short_region: ue1
  region: us-east-1

contexts:
  dev:
    environment: dev
    # Optional: aws_profile, short_region, region, cluster
  
  staging:
    environment: staging
    region: us-west-2  # Override default
```

**Common mistakes:**
- Missing `environment` field
- Empty `contexts` section
- Invalid YAML syntax (tabs instead of spaces, etc.)

**Validate your config:**
```bash
uv run python -c "from kubert.models import KubertConfig; KubertConfig.from_yaml_file('~/.config/kubert.yaml'); print('✅ Config is valid')"
```

---

## Problem: `kubectl` not found

### Symptoms
```
kubectl: command not found
```

### Solution

Install kubectl:

**macOS:**
```bash
brew install kubectl
```

**Ubuntu/Debian:**
```bash
sudo apt-get install kubectl
```

**Or download directly:**
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

---

## Problem: `aws` CLI not found

### Symptoms
```
aws: command not found
```

### Solution

Install AWS CLI:

**macOS:**
```bash
brew install awscli
```

**Ubuntu/Debian:**
```bash
sudo apt-get install awscli
```

**Or use pip:**
```bash
pip install awscli
```

---

## Problem: AWS EKS update fails

### Symptoms
```
Error: An error occurred (ResourceNotFoundException) when calling the DescribeCluster operation
```

### Causes
1. Cluster name is incorrect
2. AWS profile doesn't have permissions
3. Region is incorrect
4. Cluster doesn't exist

### Solution

**Check cluster name:**
```bash
# List clusters in region
aws eks list-clusters --region us-east-1 --profile your-profile
```

**Check your config:**
```yaml
contexts:
  dev:
    environment: dev
    cluster: correct-cluster-name  # Make sure this matches
    region: us-east-1
    aws_profile: your-profile
```

**Test AWS access:**
```bash
aws sts get-caller-identity --profile your-profile
```

---

## Problem: kops export fails

### Symptoms
```
Error: chamber: command not found
```
or
```
Error: kops: command not found
```

### Solution

Install required tools:

**kops:**
```bash
brew install kops  # macOS
```

**chamber:**
```bash
brew install chamber  # macOS
```

---

## Problem: Context doesn't switch even with shell integration

### Symptoms
- Shell integration is installed
- `kubert` runs without errors
- But `kubectl config current-context` shows wrong context

### Debugging Steps

1. **Check KUBECONFIG is set:**
   ```bash
   kubert dev
   echo $KUBECONFIG
   # Should show: /Users/mike/.kube/dev.config.yaml
   ```

2. **Check the kubeconfig file exists:**
   ```bash
   ls -la ~/.kube/dev.config.yaml
   ```

3. **Check the kubeconfig file has content:**
   ```bash
   cat ~/.kube/dev.config.yaml
   ```

4. **Manually test kubectl with the file:**
   ```bash
   KUBECONFIG=~/.kube/dev.config.yaml kubectl config current-context
   ```

5. **Check if EKS update ran:**
   ```bash
   # Run with verbose output
   kubert dev
   # Should show: "aws eks update-kubeconfig ..."
   ```

### Possible Issues

**Issue: Kubeconfig file is empty**

The EKS update might have failed. Check:
```bash
# Run the aws command manually
aws eks update-kubeconfig \
  --name your-cluster-name \
  --region us-east-1 \
  --profile your-profile \
  --kubeconfig ~/.kube/dev.config.yaml
```

**Issue: Multiple KUBECONFIG files**

If you have `KUBECONFIG` set to multiple files:
```bash
# Check current KUBECONFIG
echo $KUBECONFIG

# Unset it and try again
unset KUBECONFIG
kubert dev
```

---

## Problem: Permission denied errors

### Symptoms
```
Permission denied: /Users/mike/.kube/dev.config.yaml
```

### Solution

Fix permissions:
```bash
chmod 600 ~/.kube/*.config.yaml
chmod 700 ~/.kube
```

---

## Getting Help

If you're still having issues:

1. **Check the logs:**
   ```bash
   kubert dev 2>&1 | tee kubert.log
   ```

2. **Test configuration:**
   ```bash
   uv run python test_config.py
   ```

3. **Test dry-run:**
   ```bash
   uv run python test_kubert_dry.py dev
   ```

4. **Check versions:**
   ```bash
   uv --version
   kubectl version --client
   aws --version
   fzf --version
   ```

5. **Open an issue** with:
   - Your shell (bash/zsh/fish)
   - Error messages
   - Output from test scripts
   - Your config file (sanitized)

