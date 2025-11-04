# Homebrew Distribution Guide

This document explains how to distribute kubert via Homebrew.

## Overview

Homebrew can fully automate the installation, but **shell integration still requires manual setup** (this is standard for tools like direnv, pyenv, etc.).

## Distribution Options

### Option 1: Homebrew Tap (Recommended for Personal/Org Use)

Create a custom tap for easy distribution within your organization.

#### Steps:

1. **Create a tap repository:**
   ```bash
   # Create a new repo: homebrew-kubert
   # GitHub URL: https://github.com/mspiegel31/homebrew-kubert
   ```

2. **Add the formula:**
   ```bash
   # In homebrew-kubert repo, create:
   # Formula/kubert.rb
   ```

3. **Users install with:**
   ```bash
   brew tap mspiegel31/kubert
   brew install kubert
   ```

4. **Homebrew automatically shows the caveats** (shell integration instructions)

### Option 2: Homebrew Core (For Public Distribution)

Submit to the main Homebrew repository for wider distribution.

#### Requirements:
- ✅ Stable release (tagged version)
- ✅ 75+ stars on GitHub OR 30+ forks OR known repository
- ✅ Actively maintained
- ✅ No dependencies on other taps

#### Steps:
1. Create a GitHub release with version tag (e.g., `v0.1.0`)
2. Submit PR to [homebrew-core](https://github.com/Homebrew/homebrew-core)
3. Homebrew maintainers review and merge

### Option 3: Direct Formula URL

Users can install directly from a formula URL:

```bash
brew install https://raw.githubusercontent.com/mspiegel31/kubert/main/Formula/kubert.rb
```

## What Homebrew Automates

✅ **Automated:**
- Python virtual environment creation
- Dependency installation (click, pydantic, boto3, etc.)
- Binary installation to `/usr/local/bin/kubert`
- Example config file installation
- Post-install instructions (caveats)

❌ **Cannot Automate:**
- Shell function injection (security/safety reasons)
- Modifying user's shell config files

## Shell Integration: Why Manual?

Homebrew **intentionally does not** modify shell config files because:

1. **Security**: Automated shell modification is a security risk
2. **User Control**: Users should control their shell environment
3. **Multiple Shells**: Users might use different shells
4. **Conflicts**: Might conflict with existing functions

**This is standard practice** - see how other tools handle it:

### direnv
```bash
$ brew install direnv
==> Caveats
To enable direnv, add the following to your shell config:
  eval "$(direnv hook bash)"
```

### pyenv
```bash
$ brew install pyenv
==> Caveats
To enable pyenv, add the following to your shell config:
  eval "$(pyenv init -)"
```

### rbenv
```bash
$ brew install rbenv
==> Caveats
To enable rbenv, add the following to your shell config:
  eval "$(rbenv init -)"
```

## Alternative: Automatic Shell Integration

If you **really** want automatic setup, you can:

### Option A: Post-Install Script (Not Recommended)

Homebrew discourages this, but you could add a post-install script:

```ruby
def post_install
  system "#{bin}/kubert-setup-shell"
end
```

**Problems:**
- Homebrew maintainers will reject this for homebrew-core
- Users might not want automatic modification
- Hard to handle multiple shells

### Option B: Separate Setup Command

Add a setup command that users run once:

```bash
brew install kubert
kubert setup-shell  # Interactive setup
```

This is better because:
- ✅ User explicitly opts in
- ✅ Can be interactive
- ✅ Can detect shell automatically
- ✅ Can backup existing config

Let me create this:

## Creating the Setup Command

Add a `setup-shell` subcommand to kubert:

```python
@click.group()
def cli():
    """Kubert - Kubernetes context switcher"""
    pass

@cli.command()
def setup_shell():
    """Setup shell integration"""
    # Interactive setup that modifies shell config
    pass

@cli.command()
@click.argument('context', required=False)
def switch(context):
    """Switch to a Kubernetes context"""
    # Existing kubert logic
    pass
```

Then users do:
```bash
brew install kubert
kubert setup-shell  # One-time setup
kubert dev          # Use normally
```

## Recommended Approach

**For your use case (internal tool), I recommend:**

1. **Create a Homebrew tap** (`mspiegel31/homebrew-kubert`)
2. **Use caveats** to show shell integration instructions
3. **Optionally add** `kubert setup-shell` command for convenience

This gives you:
- ✅ Easy installation: `brew tap mspiegel31/kubert && brew install kubert`
- ✅ Automatic updates: `brew upgrade kubert`
- ✅ Clear instructions in caveats
- ✅ Optional automated setup with `kubert setup-shell`

## Example: Complete Homebrew Workflow

```bash
# User installs
$ brew tap mspiegel31/kubert
$ brew install kubert

==> Installing kubert from mspiegel31/kubert
🍺  /usr/local/Cellar/kubert/0.1.0: 50 files, 1.2MB
==> Caveats
To enable kubert shell integration, run:
  kubert setup-shell

Or manually add to your ~/.bashrc or ~/.zshrc:
  kubert() {
      eval "$(command kubert "$@")"
  }

# User runs setup
$ kubert setup-shell
Detected shell: zsh
Add shell integration to ~/.zshrc? (y/N) y
✅ Shell integration added
Reload your shell: source ~/.zshrc

# User reloads and uses
$ source ~/.zshrc
$ kubert dev
✅ Switched to dev context
```

## Next Steps

Would you like me to:

1. ✅ **Create the Homebrew formula** (Formula/kubert.rb) - DONE
2. **Add `kubert setup-shell` command** to automate shell integration?
3. **Create a homebrew-kubert tap repository** structure?
4. **Update README** with Homebrew installation instructions?

Let me know which direction you'd prefer!

