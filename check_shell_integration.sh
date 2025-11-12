#!/bin/bash

echo "=== Checking Shell Integration ==="
echo ""

# Check if kubert function exists
if type kubert 2>/dev/null | grep -q "function"; then
    echo "✅ kubert shell function is defined"
    echo ""
    type kubert
else
    echo "❌ kubert shell function NOT found"
    echo ""
    echo "You need to add this to your ~/.bashrc or ~/.zshrc:"
    echo ""
    echo "    kubert() {"
    echo "        eval \"\$(command kubert \"\$@\")\""
    echo "    }"
    echo ""
fi

echo ""
echo "=== Testing the difference ==="
echo ""

# Test without eval
echo "1. Running directly (won't work):"
echo "   $ uv run kubert ue1-staging"
echo "   Result: KUBECONFIG only set in Python process, not your shell"
echo ""

# Test with eval
echo "2. Running with eval (correct way):"
echo "   $ eval \"\$(uv run kubert ue1-staging)\""
echo "   Result: KUBECONFIG set in your current shell"
echo ""

echo "=== Quick Test ==="
echo ""
echo "Try this command to test:"
echo "  eval \"\$(uv run kubert ue1-staging)\" && echo \$KUBECONFIG"
echo ""
