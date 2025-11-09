# Components MCP Server - Quick Start

## What's Built

A simple MCP server with **2 tools**:
1. `list_components` - List components by type (app or function)
2. `get_details` - Get detailed information about a component

## Running the Server

### Option 1: Run with uvx (No Installation)
```bash
# From project directory
uvx --from . components-mcp

# From built package
uvx --from dist/components_mcp-0.1.0-py3-none-any.whl components-mcp

# With custom component directory
COMPONENT_DIR=/path/to/components uvx --from . components-mcp
```

### Option 2: Run Directly (After Installation)
```bash
# As a module
python -m components_mcp

# Or using uv
uv run components-mcp
```

### Option 3: Use FastMCP CLI
```bash
# Run with STDIO (for local clients)
fastmcp run src/components_mcp/server.py

# Run with HTTP (for remote access)
fastmcp run src/components_mcp/server.py --transport http --port 8000

# Run with MCP Inspector for testing
fastmcp dev src/components_mcp/server.py
```

### Option 4: Install in MCP Clients
```bash
# Claude Desktop
fastmcp install claude-desktop src/components_mcp/server.py

# Claude Code
fastmcp install claude-code src/components_mcp/server.py
```

## Testing

### Run Test Suite
```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_server.py -v
```

## Using the Tools

### 1. List Components

**List functions** (individual utilities with 1-2 modules):
```json
{
  "name": "list_components",
  "arguments": {"type": "function"}
}
```

**List apps** (complex tools with 3+ modules):
```json
{
  "name": "list_components",
  "arguments": {"type": "app"}
}
```

### 2. Get Component Details

```json
{
  "name": "get_details",
  "arguments": {
    "type": "function",
    "name": "example.utils.text_utils.format_text"
  }
}
```

## Directory Discovery

The server searches for `.libs` in this order:
1. `./libs` (current directory)
2. `$COMPONENT_DIR/.libs`
3. `~/.cache/agent-tools/.libs` (default)

Set custom location:
```bash
export COMPONENT_DIR=/path/to/your/components
python server.py
```

## Component Classification

- **Function**: Feature directory with 1-2 modules (individual utilities)
- **App**: Feature directory with 3+ modules (complex integrated tools)

Example structure:
```
.libs/
├── index.yaml
├── example/
│   ├── utils/              # 2 modules = FUNCTION
│   │   ├── text_utils.py
│   │   └── stats_utils.py
│   └── email_app/          # 3 modules = APP
│       ├── sender.py
│       ├── inbox.py
│       └── search.py
```

## Example Output

### Listing Functions
```json
[
  {
    "name": "example.utils.text_utils.format_text",
    "description": "Format text with various options",
    "root_directory": "/path/to/.libs"
  }
]
```

### Getting Details
```json
{
  "name": "example.utils.text_utils.format_text",
  "type": "function",
  "description": "Format text with various options...",
  "short_description": "Format text with various options",
  "module_path": "/path/to/.libs/example/utils/text_utils.py",
  "root_directory": "/path/to/.libs",
  "category": "example",
  "feature": "utils"
}
```

## Next Steps

1. **Run tests**: `uv run pytest -v`
2. **Inspect the server**: `fastmcp inspect src/components_mcp/server.py`
3. **Install in your client**: `fastmcp install claude-code src/components_mcp/server.py`
4. **Point to your components**: `export COMPONENT_DIR=/your/path`
