"""
Tests for the get_details tool.
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


async def test_get_details_function_component(mcp_client: Client[FastMCPTransport]):
    """Test getting details for a function-type component."""
    result = await mcp_client.call_tool(
        name="get_details",
        arguments={
            "type": "function",
            "name": "example.utils.text_utils.format_text"
        }
    )

    assert result.data is not None

    # Convert to dict for easier assertion
    data = result.data[0] if isinstance(result.data, list) else result.data

    # Check required fields
    assert hasattr(data, 'name') or 'name' in str(data)
    assert hasattr(data, 'type') or 'type' in str(data)
    assert hasattr(data, 'description') or 'description' in str(data)

    # Verify the component name is in the response
    result_str = str(data)
    assert "example.utils.text_utils.format_text" in result_str
    assert "function" in result_str


async def test_get_details_app_component(mcp_client: Client[FastMCPTransport]):
    """Test getting details for an app-type component."""
    result = await mcp_client.call_tool(
        name="get_details",
        arguments={
            "type": "app",
            "name": "example.email_app.main.main"
        }
    )

    assert result.data is not None

    # Convert to dict for easier assertion
    data = result.data[0] if isinstance(result.data, list) else result.data

    # Check required fields
    assert hasattr(data, 'name') or 'name' in str(data)
    assert hasattr(data, 'type') or 'type' in str(data)
    assert hasattr(data, 'description') or 'description' in str(data)

    # Verify the component name and type are in the response
    result_str = str(data)
    assert "example.email_app.main.main" in result_str
    assert "app" in result_str


async def test_get_details_another_function(mcp_client: Client[FastMCPTransport]):
    """Test getting details for another function-type component."""
    result = await mcp_client.call_tool(
        name="get_details",
        arguments={
            "type": "function",
            "name": "example.utils.stats_utils.calculate_stats"
        }
    )

    assert result.data is not None

    # Convert to dict for easier assertion
    data = result.data[0] if isinstance(result.data, list) else result.data

    # Verify the component name is in the response
    result_str = str(data)
    assert "example.utils.stats_utils.calculate_stats" in result_str
    assert "function" in result_str


async def test_get_details_nonexistent(mcp_client: Client[FastMCPTransport]):
    """Test getting details for a non-existent component."""
    result = await mcp_client.call_tool(
        name="get_details",
        arguments={"type": "function", "name": "nonexistent.component.function"}
    )

    assert result.data is not None

    # Should return error information about the component
    result_str = str(result.data)
    assert "nonexistent.component.function" in result_str
    assert "error" in result_str.lower() or "not found" in result_str.lower()


async def test_get_details_response_structure(mcp_client: Client[FastMCPTransport]):
    """Test that get_details returns the expected fields."""
    result = await mcp_client.call_tool(
        name="get_details",
        arguments={
            "type": "function",
            "name": "example.utils.text_utils.format_text"
        }
    )

    assert result.data is not None

    # Check for expected fields in the response
    result_str = str(result.data)
    assert "name" in result_str
    assert "type" in result_str
    assert "description" in result_str
    assert "module_path" in result_str or "module" in result_str
    assert "directory" in result_str
