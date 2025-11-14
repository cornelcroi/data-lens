#!/bin/bash

# Setup script for data-lens MCP server in Claude Desktop
# This script will automatically configure Claude Desktop to use data-lens

set -e

echo "🚀 data-lens MCP Server Setup for Claude Desktop"
echo "=================================================="
echo ""

# Get the absolute path to this script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_PYTHON="$SCRIPT_DIR/venv/bin/python"
SERVER_PY="$SCRIPT_DIR/server.py"

# Verify files exist
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Error: Virtual environment Python not found at $VENV_PYTHON"
    echo "Please run: python3 -m venv venv && venv/bin/pip install fastmcp duckdb pandas openpyxl pyarrow"
    exit 1
fi

if [ ! -f "$SERVER_PY" ]; then
    echo "❌ Error: server.py not found at $SERVER_PY"
    exit 1
fi

echo "✅ Found Python: $VENV_PYTHON"
echo "✅ Found server: $SERVER_PY"
echo ""

# Test server can be imported
echo "🧪 Testing server..."
if $VENV_PYTHON -c "import server; print('Server OK')" 2>/dev/null; then
    echo "✅ Server imports successfully"
else
    echo "❌ Error: Server failed to import"
    echo "Please check that all dependencies are installed"
    exit 1
fi
echo ""

# Determine OS and config location
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_DIR="$HOME/Library/Application Support/Claude"
    CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"
    echo "📍 Platform: macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CONFIG_DIR="$HOME/.config/Claude"
    CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"
    echo "📍 Platform: Linux"
else
    echo "❌ Unsupported platform: $OSTYPE"
    echo "Please manually configure Claude Desktop"
    exit 1
fi

echo "📍 Config file: $CONFIG_FILE"
echo ""

# Create config directory if it doesn't exist
if [ ! -d "$CONFIG_DIR" ]; then
    echo "📁 Creating config directory..."
    mkdir -p "$CONFIG_DIR"
fi

# Backup existing config
if [ -f "$CONFIG_FILE" ]; then
    BACKUP_FILE="$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    echo "💾 Backing up existing config to:"
    echo "   $BACKUP_FILE"
    cp "$CONFIG_FILE" "$BACKUP_FILE"
    echo ""
fi

# Create or update config
if [ -f "$CONFIG_FILE" ]; then
    echo "📝 Updating existing configuration..."

    # Read existing config and add data-lens server
    TEMP_FILE=$(mktemp)

    # Use Python to merge configs properly
    $VENV_PYTHON << EOF
import json
import sys

config_file = "$CONFIG_FILE"
venv_python = "$VENV_PYTHON"
server_py = "$SERVER_PY"

try:
    with open(config_file, 'r') as f:
        config = json.load(f)
except:
    config = {}

if 'mcpServers' not in config:
    config['mcpServers'] = {}

config['mcpServers']['data-lens'] = {
    'command': venv_python,
    'args': [server_py],
    'env': {}
}

with open('$TEMP_FILE', 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Configuration updated")
EOF

    mv "$TEMP_FILE" "$CONFIG_FILE"
else
    echo "📝 Creating new configuration..."
    cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "data-lens": {
      "command": "$VENV_PYTHON",
      "args": [
        "$SERVER_PY"
      ],
      "env": {}
    }
  }
}
EOF
    echo "✅ Configuration created"
fi

echo ""
echo "✨ Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Quit Claude Desktop completely (if running)"
echo "2. Restart Claude Desktop"
echo "3. In a new conversation, try:"
echo "   'What MCP servers are available?'"
echo "   'Load /Users/corneliu/projects/data-lens/sample_ecommerce_data.csv'"
echo ""
echo "📖 For more help, see CLAUDE_DESKTOP_CONFIG.md"
echo ""
echo "🎉 Happy analyzing!"
