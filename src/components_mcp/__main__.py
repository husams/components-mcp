"""Entry point for running the Components MCP Server."""

import argparse
from .server import mcp


def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(
        description="Components MCP Server - Provides access to reusable component libraries"
    )
    parser.add_argument(
        "--transport",
        type=str,
        choices=["stdio", "http"],
        default="stdio",
        help="Transport protocol to use (default: stdio)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port number for HTTP transport (default: 8000)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host address for HTTP transport (default: 0.0.0.0)"
    )

    args = parser.parse_args()

    # Run with specified transport
    if args.transport == "http":
        mcp.run(transport="http", host=args.host, port=args.port)
    else:
        mcp.run()  # Default stdio transport


if __name__ == "__main__":
    main()
