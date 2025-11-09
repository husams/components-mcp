"""Entry point for running the Components MCP Server."""

from .server import mcp


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
