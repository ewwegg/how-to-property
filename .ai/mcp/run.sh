#!/bin/bash

# MCP Server Launch Script for Pattern-First Framework

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Move to project root (two levels up from .ai/mcp/)
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Change to project root
cd "$PROJECT_ROOT"

# Set PYTHONPATH to include project root and .ai directory
export PYTHONPATH="$PROJECT_ROOT:$PROJECT_ROOT/.ai:$PYTHONPATH"

# Check if virtual environment exists
if [ -d ".venv" ]; then
    echo "Using virtual environment at .venv" >&2
    source .venv/bin/activate
    PYTHON_CMD="python"
elif [ -d "venv" ]; then
    echo "Using virtual environment at venv" >&2
    source venv/bin/activate
    PYTHON_CMD="python"
else
    echo "No virtual environment found, using system Python" >&2
    PYTHON_CMD="python3"
fi

# Check if MCP is installed
if ! $PYTHON_CMD -c "import mcp" 2>/dev/null; then
    echo "ERROR: MCP SDK not installed" >&2
    echo "Please install it with:" >&2
    echo "  $PYTHON_CMD -m pip install mcp pyyaml" >&2
    exit 1
fi

# Run the MCP server
exec $PYTHON_CMD "$SCRIPT_DIR/server.py"