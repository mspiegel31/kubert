#!/bin/bash
# Setup shell integration for kubert

set -e

echo "======================================================================"
echo "Kubert Shell Integration Setup"
echo "======================================================================"
echo ""

# Detect shell
SHELL_NAME=$(basename "$SHELL")
echo "Detected shell: $SHELL_NAME"
echo ""

# Shell integration code
BASH_ZSH_CODE='
# Kubert shell integration
kubert() {
    eval "$(command kubert "$@")"
}

assume-role() {
    eval "$(command assume-role "$@")"
}
'

FISH_CODE='
# Kubert shell integration
function kubert
    command kubert $argv | source
end

function assume-role
    command assume-role $argv | source
end
'

# Determine config file
case "$SHELL_NAME" in
    bash)
        CONFIG_FILE="$HOME/.bashrc"
        INTEGRATION_CODE="$BASH_ZSH_CODE"
        ;;
    zsh)
        CONFIG_FILE="$HOME/.zshrc"
        INTEGRATION_CODE="$BASH_ZSH_CODE"
        ;;
    fish)
        CONFIG_FILE="$HOME/.config/fish/config.fish"
        INTEGRATION_CODE="$FISH_CODE"
        mkdir -p "$(dirname "$CONFIG_FILE")"
        ;;
    *)
        echo "❌ Unsupported shell: $SHELL_NAME"
        echo ""
        echo "Please manually add the shell integration to your shell config file."
        echo "See README.md for instructions."
        exit 1
        ;;
esac

echo "Config file: $CONFIG_FILE"
echo ""

# Check if already installed
if [ -f "$CONFIG_FILE" ] && grep -q "kubert shell integration" "$CONFIG_FILE"; then
    echo "✅ Shell integration already installed in $CONFIG_FILE"
    echo ""
    echo "To reload your shell configuration, run:"
    echo "  source $CONFIG_FILE"
    exit 0
fi

# Ask for confirmation
echo "This will add the following to $CONFIG_FILE:"
echo "----------------------------------------------------------------------"
echo "$INTEGRATION_CODE"
echo "----------------------------------------------------------------------"
echo ""
read -p "Continue? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    echo ""
    echo "To manually add shell integration, see README.md"
    exit 1
fi

# Backup existing config
if [ -f "$CONFIG_FILE" ]; then
    BACKUP_FILE="${CONFIG_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$CONFIG_FILE" "$BACKUP_FILE"
    echo "✅ Backed up existing config to: $BACKUP_FILE"
fi

# Add integration
echo "$INTEGRATION_CODE" >> "$CONFIG_FILE"
echo "✅ Added shell integration to $CONFIG_FILE"
echo ""

# Instructions
echo "======================================================================"
echo "Setup Complete!"
echo "======================================================================"
echo ""
echo "To activate the changes, run:"
echo "  source $CONFIG_FILE"
echo ""
echo "Or restart your terminal."
echo ""
echo "Then test with:"
echo "  kubert --help"
echo "  assume-role --help"
echo ""
echo "======================================================================"

