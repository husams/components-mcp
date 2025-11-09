# Components MCP Server

A simple MCP server that provides tools to list and retrieve details about reusable components stored in `.libs` directories.

## Features

This server provides **two tools**:

1. **list_components**: Lists all components of a given type (app or function)
2. **get_details**: Returns detailed information about a specific component

## Component Types

Components are classified based on their `index.yaml` file:

- **function**: Multiple public functions (2+ entries in index.yaml)
  - Libraries with multiple reusable functions
  - Each function is independently callable
  - Example: utility library with text formatting, math operations, etc.

- **app**: Single main entry point (1 entry in index.yaml)
  - Complete application with a main function
  - Helper/private modules in subdirectories
  - Example: email application with one main() function that handles all operations

## Installation

### Option 1: Run with uvx (No Installation Required)

The fastest way to use the server:

```bash
# Run directly with uvx (from local directory)
uvx --from . components-mcp

# Or from a built package
uvx --from dist/components_mcp-0.1.0-py3-none-any.whl components-mcp

# Or from a Git repository
uvx --from git+https://github.com/your-org/components-mcp.git components-mcp
```

### Option 2: Install Locally

```bash
# Install with uv
uv sync

# Or with pip
pip install -e .
```

## Usage

### Running the Server

```bash
# METHOD 1: Run with uvx (recommended for quick use)
uvx --from . components-mcp

# METHOD 2: Run with FastMCP CLI
fastmcp run src/components_mcp/server.py

# METHOD 3: Run as installed command
uv run components-mcp

# METHOD 4: Run as Python module
python -m components_mcp

# Run with HTTP transport
fastmcp run src/components_mcp/server.py --transport http --port 8000

# Run with MCP Inspector for testing
fastmcp dev src/components_mcp/server.py
```

### Installing in MCP Clients

```bash
# Install in Claude Desktop
fastmcp install claude-desktop src/components_mcp/server.py

# Install in Claude Code
fastmcp install claude-code src/components_mcp/server.py

# Install in Cursor
fastmcp install cursor src/components_mcp/server.py
```

## Component Directory Discovery

The server scans for `.libs` directories in the following order:

1. **Local project**: `./libs` (current working directory)
2. **Environment variable**: `$COMPONENT_DIR/.libs`
3. **Default cache**: `~/.cache/agent-tools/.libs`

Set the `COMPONENT_DIR` environment variable to use a custom location:

```bash
export COMPONENT_DIR=/path/to/components
fastmcp run server.py
```

## Tools

### 1. list_components

Lists components from the .libs directory.

**Parameters:**
- `type` (optional): Filter by type - `"app"`, `"function"`, or omit to list all

**Returns:**
```json
[
  {
    "name": "category.feature.function_name",
    "description": "Brief description of the component"
  }
]
```

**Examples:**
```python
# List all components (apps + functions)
result = await client.call_tool(
    name="list_components",
    arguments={}
)

# List only functions
result = await client.call_tool(
    name="list_components",
    arguments={"type": "function"}
)

# List only apps
result = await client.call_tool(
    name="list_components",
    arguments={"type": "app"}
)
```

### 2. get_details

Returns detailed information about a specific component.

**Parameters:**
- `type` (required): Either `"app"` or `"function"`
- `name` (required): Fully qualified component name (e.g., `"category.feature.function"`)

**Returns:**
```json
{
  "name": "category.feature.function_name",
  "type": "function",
  "description": "Full docstring from the component",
  "short_description": "Brief description from index.yaml",
  "module_path": "/path/to/.libs/category/feature/module.py",
  "root_directory": "/path/to/.libs",
  "category": "category",
  "feature": "feature"
}
```

**Example:**
```python
# Get details for a specific component
result = await client.call_tool(
    name="get_details",
    arguments={
        "type": "function",
        "name": "utils.service_config.rename_service"
    }
)
```

## Testing

Run the test suite using pytest:

```bash
# Install test dependencies
uv sync --group dev

# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_server.py -v

# Run with coverage
uv run pytest --cov=src/components_mcp
```

## Project Structure

```
components-mcp/
├── src/
│   └── components_mcp/
│       ├── __init__.py
│       ├── __main__.py           # Entry point
│       └── server.py             # MCP server implementation
├── tests/
│   ├── __init__.py
│   ├── test_server.py            # Server configuration tests
│   ├── test_list_components.py  # list_components tool tests
│   └── test_get_details.py      # get_details tool tests
├── .libs/                        # Example component library
│   ├── index.yaml
│   └── example/
│       ├── utils/
│       └── email_app/
├── pyproject.toml
└── README.md
```

## Component Directory Structure

**Note:** There is NO root index.yaml file. Each component directory has its own index.yaml.

### Function Type Components

Components with **multiple public functions** (2+ entries in index.yaml):

```
.libs/
└── category/
    └── feature/                  # Function component
        ├── __init__.py
        ├── index.yaml            # Lists all public functions
        ├── module_1.py           # Contains public function(s)
        └── module_2.py           # Contains public function(s)
```

**Example index.yaml for functions:**
```yaml
functions:
  - name: category.feature.module_1.function_a
    description: First public function
  - name: category.feature.module_1.function_b
    description: Second public function
  - name: category.feature.module_2.function_c
    description: Third public function
```

### App Type Components

Components with a **single main entry point** (1 entry in index.yaml):

```
.libs/
└── category/
    └── app_name/                 # App component
        ├── __init__.py
        ├── index.yaml            # Lists only main function
        ├── main.py               # Contains main() function
        └── helpers/              # Private helper modules
            ├── __init__.py
            ├── helper_1.py
            └── helper_2.py
```

**Example index.yaml for apps:**
```yaml
functions:
  - name: category.app_name.main.main
    description: Main entry point for the application
```

## Building for Distribution

Build distributable packages for uvx or PyPI:

```bash
# Build wheel and source distribution
uv build

# Output will be in dist/
# - dist/components_mcp-0.1.0-py3-none-any.whl (wheel)
# - dist/components_mcp-0.1.0.tar.gz (source)

# Run from built wheel with uvx
uvx --from dist/components_mcp-0.1.0-py3-none-any.whl components-mcp

# Or install from wheel
pip install dist/components_mcp-0.1.0-py3-none-any.whl
```

## Development

```bash
# Run server with auto-reload during development
fastmcp dev src/components_mcp/server.py

# Inspect server components
fastmcp inspect src/components_mcp/server.py

# Generate JSON report
fastmcp inspect src/components_mcp/server.py --format fastmcp -o report.json

# Run tests during development
uv run pytest tests/ -v --tb=short

# Build package
uv build
```

## License

MIT
