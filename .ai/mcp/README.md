# MCP Server for Pattern-First Framework

This MCP (Model Context Protocol) server integrates your pattern-first framework with Claude Desktop, allowing Claude to directly access and use your patterns.

## Installation

### 1. Install Dependencies

First, create a virtual environment and install the MCP SDK:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate  # On Windows

# Install dependencies
pip install mcp pyyaml
```

### 2. Configure Claude Desktop

Copy the configuration to Claude Desktop's config location:

#### macOS
```bash
cp claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

#### Windows
```powershell
copy claude_desktop_config.json %APPDATA%\Claude\claude_desktop_config.json
```

#### Linux
```bash
cp claude_desktop_config.json ~/.config/Claude/claude_desktop_config.json
```

**Note**: You may need to merge this configuration with any existing config file.

### 3. Update Paths

Edit the Claude Desktop config file and update the absolute path to match your repository location:

```json
{
  "mcpServers": {
    "pattern-framework": {
      "command": "/absolute/path/to/your/project/.ai/mcp/run.sh"
    }
  }
}
```

### 4. Restart Claude Desktop

After configuration, fully quit and restart Claude Desktop for the changes to take effect.

## Available MCP Tools

Once configured, Claude will have access to these tools:

### `generate_from_pattern`
Generate code using existing patterns in your library.
- Input: `task` (string) - What to generate

### `search_patterns`
Search for patterns matching a query.
- Input: `query` (string) - Search term
- Input: `domain` (optional) - Filter by domain (frontend/infrastructure/api/database)

### `list_all_patterns`
List all available patterns organized by domain.

### `validate_code`
Validate code against your framework philosophy.
- Input: `code` (string) - Code to validate

### `get_pattern_instructions`
Get instructions for creating a new pattern.
- Input: `task` (string) - Task the pattern should solve
- Input: `domain` (string) - Domain for the pattern

## Resources

The MCP server also exposes your patterns and philosophy as resources that Claude can read:

- **Philosophy**: `pattern-framework://philosophy`
- **Patterns**: `pattern-framework://patterns/{domain}/{pattern-name}.md`

## Testing the Server

To test the server manually:

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the server
python .ai/mcp/server.py
```

The server expects stdio communication, so it will wait for input. You can exit with Ctrl+C.

## Troubleshooting

### "MCP SDK not installed" error
Make sure you've installed the SDK in a virtual environment and the launch script can find it.

### Server doesn't start in Claude
1. Check that the path in claude_desktop_config.json is absolute and correct
2. Make sure run.sh is executable: `chmod +x .ai/mcp/run.sh`
3. Check Claude's logs for error messages

### Patterns not showing up
Ensure your patterns follow the correct format with YAML frontmatter and are in the .ai/patterns/ directory.

## How It Works

1. When Claude Desktop starts, it launches the MCP server
2. The server exposes your patterns as resources and tools
3. Claude can read patterns, search them, and generate code using them
4. All generation follows your pattern-first philosophy
5. No free-form code generation - only from validated patterns

## Development

To add new capabilities to the MCP server:

1. Edit `.ai/mcp/server.py`
2. Add new tools in `handle_list_tools()`
3. Implement tool logic in `handle_call_tool()`
4. Restart Claude Desktop to load changes