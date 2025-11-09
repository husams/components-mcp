"""
Tests for server configuration and setup.
"""

import pytest
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport
from components_mcp.server import mcp


@pytest.fixture
async def mcp_client():
    """Create a test client connected to the MCP server."""
    async with Client(transport=mcp) as client:
        yield client


async def test_server_has_correct_name(mcp_client: Client[FastMCPTransport]):
    """Test that the server has the expected name."""
    assert mcp.name == "Components MCP Server"


async def test_server_exposes_two_tools(mcp_client: Client[FastMCPTransport]):
    """Test that the server exposes exactly 2 tools."""
    tools = await mcp_client.list_tools()
    assert len(tools) == 2

    tool_names = {tool.name for tool in tools}
    assert "list_components" in tool_names
    assert "get_details" in tool_names


async def test_list_components_tool_signature(mcp_client: Client[FastMCPTransport]):
    """Test that list_components tool has correct signature."""
    tools = await mcp_client.list_tools()
    list_tool = next(t for t in tools if t.name == "list_components")

    # Check tool has description
    assert list_tool.description is not None
    assert len(list_tool.description) > 0

    # Check tool has input schema
    assert list_tool.inputSchema is not None


async def test_get_details_tool_signature(mcp_client: Client[FastMCPTransport]):
    """Test that get_details tool has correct signature."""
    tools = await mcp_client.list_tools()
    details_tool = next(t for t in tools if t.name == "get_details")

    # Check tool has description
    assert details_tool.description is not None
    assert len(details_tool.description) > 0

    # Check tool has input schema
    assert details_tool.inputSchema is not None


async def test_server_has_no_resources(mcp_client: Client[FastMCPTransport]):
    """Test that the server exposes no resources."""
    resources = await mcp_client.list_resources()
    assert len(resources) == 0


async def test_server_has_no_prompts(mcp_client: Client[FastMCPTransport]):
    """Test that the server exposes no prompts."""
    prompts = await mcp_client.list_prompts()
    assert len(prompts) == 0
