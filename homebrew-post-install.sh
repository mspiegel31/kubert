#!/bin/bash
# Post-install script for Homebrew
# This is shown to users after `brew install kubert`

cat << 'EOF'

🎉 kubert installed successfully!

⚠️  IMPORTANT: Shell Integration Required

To use kubert, add this to your shell config:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For Bash (~/.bashrc):

    kubert() {
        eval "$(command kubert "$@")"
    }

    assume-role() {
        eval "$(command assume-role "$@")"
    }

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For Zsh (~/.zshrc):

    kubert() {
        eval "$(command kubert "$@")"
    }

    assume-role() {
        eval "$(command assume-role "$@")"
    }

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For Fish (~/.config/fish/config.fish):

    function kubert
        command kubert $argv | source
    end

    function assume-role
        command assume-role $argv | source
    end

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Then reload your shell:
    source ~/.bashrc  # or ~/.zshrc

Next steps:
    1. Create config: mkdir -p ~/.config && cp $(brew --prefix)/share/kubert/example.kubert.yaml ~/.config/kubert.yaml
    2. Edit config: vim ~/.config/kubert.yaml
    3. Test: kubert --help

EOF

