# uvx Quick Start

The fastest way to run the Components MCP Server without installation.

## Basic Usage

```bash
# Run from project directory
uvx --from . components-mcp
```

## All Methods

```bash
# 1. From local project (development)
uvx --from . components-mcp

# 2. From built wheel (distribution)
uv build
uvx --from dist/components_mcp-0.1.0-py3-none-any.whl components-mcp

# 3. From Git repository (sharing)
uvx --from git+https://github.com/your-org/components-mcp.git components-mcp

# 4. From PyPI (after publishing)
uvx components-mcp
```

## With Custom Component Directory

```bash
COMPONENT_DIR=/path/to/components uvx --from . components-mcp
```

## What is uvx?

`uvx` is part of the `uv` toolchain that:
- Runs Python applications without installing them
- Creates isolated environments automatically
- Handles all dependencies
- Perfect for one-off commands and scripts

## Benefits

✓ **No Installation**: Run without `pip install`
✓ **Isolated**: Doesn't affect global Python environment
✓ **Fast**: Uses uv's speed optimizations
✓ **Reliable**: Always uses exact dependencies
✓ **Shareable**: Easy to share via Git URLs

## Building for uvx

```bash
# Build distributable packages
uv build

# Test the built package
uvx --from dist/components_mcp-0.1.0-py3-none-any.whl components-mcp
```

## Troubleshooting

### uvx not found
```bash
# Install uv first
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Module not found
Make sure you're using `--from` with the correct path:
```bash
uvx --from . components-mcp  # Note the --from flag
```

## More Info

- uv documentation: https://docs.astral.sh/uv/
- uvx guide: https://docs.astral.sh/uv/guides/tools/
