#!/bin/bash
# Install kubert with automatic shell integration

set -e

echo "======================================================================"
echo "Kubert Installation"
echo "======================================================================"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed"
    echo ""
    echo "Install uv first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Install Python package
echo "Installing kubert Python package..."
uv sync
echo "✅ Python package installed"
echo ""

# Detect shell
SHELL_NAME=$(basename "$SHELL")
echo "Detected shell: $SHELL_NAME"

# Determine config file
case "$SHELL_NAME" in
    bash)
        CONFIG_FILE="$HOME/.bashrc"
        ;;
    zsh)
        CONFIG_FILE="$HOME/.zshrc"
        ;;
    fish)
        CONFIG_FILE="$HOME/.config/fish/config.fish"
        mkdir -p "$(dirname "$CONFIG_FILE")"
        ;;
    *)
        echo "⚠️  Unsupported shell: $SHELL_NAME"
        echo "Please manually add shell integration (see README.md)"
        exit 0
        ;;
esac

# Check if already installed
if [ -f "$CONFIG_FILE" ] && grep -q "kubert shell integration" "$CONFIG_FILE"; then
    echo "✅ Shell integration already installed"
    echo ""
    echo "To reload: source $CONFIG_FILE"
    exit 0
fi

# Ask for confirmation
echo ""
echo "This will add shell integration to: $CONFIG_FILE"
read -p "Continue? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Skipped shell integration"
    echo "To manually add it, see README.md"
    exit 0
fi

# Backup
if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "${CONFIG_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Add integration
if [ "$SHELL_NAME" = "fish" ]; then
    cat >> "$CONFIG_FILE" << 'EOF'

# Kubert shell integration
function kubert
    command kubert $argv | source
end

function assume-role
    command assume-role $argv | source
end
EOF
else
    cat >> "$CONFIG_FILE" << 'EOF'

# Kubert shell integration
kubert() {
    eval "$(command kubert "$@")"
}

assume-role() {
    eval "$(command assume-role "$@")"
}
EOF
fi

echo "✅ Shell integration added to $CONFIG_FILE"
echo ""
echo "======================================================================"
echo "Installation Complete!"
echo "======================================================================"
echo ""
echo "Next steps:"
echo "  1. Reload your shell: source $CONFIG_FILE"
echo "  2. Create config: cp example.kubert.yaml ~/.config/kubert.yaml"
echo "  3. Test: kubert --help"
echo ""

