"""
Simple MCP server for listing and retrieving component details from .libs directories.

This server provides tools to:
1. List components (apps or functions) from index.yaml files
2. Get detailed information about specific components
"""

import os
from pathlib import Path
from typing import Literal, Optional
import yaml
from fastmcp import FastMCP

mcp = FastMCP(
    name="Components MCP Server",
    instructions="Provides access to reusable component libraries stored in .libs directories"
)


def get_libs_directory() -> Path:
    """
    Determine the .libs directory to scan.
    Priority:
    1. Local project .libs
    2. $COMPONENT_DIR/.libs
    3. ~/.cache/agent-tools/.libs (default)
    """
    # Check local .libs first
    local_libs = Path.cwd() / ".libs"
    if local_libs.exists():
        return local_libs

    # Check COMPONENT_DIR environment variable
    component_dir = os.getenv("COMPONENT_DIR")
    if component_dir:
        libs_dir = Path(component_dir) / ".libs"
        if libs_dir.exists():
            return libs_dir

    # Default to ~/.cache/agent-tools/.libs
    default_libs = Path.home() / ".cache" / "agent-tools" / ".libs"
    return default_libs


def find_all_index_files(libs_dir: Path) -> list[tuple[Path, dict]]:
    """
    Find all index.yaml files recursively in .libs directory.
    Returns list of (index_file_path, parsed_data) tuples.

    Supports two formats:
    - App format: { app: { name: ..., description: ... } }
    - Function format: { functions: [ { name: ..., description: ... }, ... ] }
    """
    index_files = []

    if not libs_dir.exists():
        return index_files

    # Recursively find all index.yaml files
    for index_path in libs_dir.rglob("index.yaml"):
        try:
            with open(index_path, 'r') as f:
                data = yaml.safe_load(f)
                # Accept both 'app' and 'functions' formats
                if data and ("functions" in data or "app" in data):
                    index_files.append((index_path, data))
        except Exception as e:
            # Skip files that can't be parsed
            continue

    return index_files


def get_component_type_from_index(index_data: dict) -> str:
    """
    Determine if a component is an 'app' or 'function' based on index.yaml content.

    Rules:
    - If index.yaml has 'app' key → app
    - If index.yaml has 'functions' key → function
    """
    if "app" in index_data:
        return "app"
    elif "functions" in index_data:
        return "function"
    else:
        return "unknown"


def get_module_path(name: str, libs_dir: Path) -> Optional[Path]:
    """
    Convert fully qualified name to module file path.

    Examples:
    - subdir1.subdir2.module.function -> .libs/subdir1/subdir2/module.py
    - subdir1.subdir2.main -> .libs/subdir1/subdir2/main.py (for apps)
    """
    parts = name.split('.')

    # Build path from all parts except the last one (which is the function name)
    # or if it's a main function, include it
    path_parts = parts[:-1]  # All except function name
    module_name = parts[-2] if len(parts) > 1 else parts[0]  # Module name

    # Try: subdir1/subdir2/module.py where module is the second to last part
    if len(path_parts) >= 1:
        # Build directory path
        dir_path = libs_dir
        for part in path_parts[:-1]:  # All directories
            dir_path = dir_path / part

        # Try the module file
        module_file = dir_path / f"{path_parts[-1]}.py"
        if module_file.exists():
            return module_file

    return None


def extract_docstring(file_path: Path, function_name: Optional[str] = None) -> str:
    """Extract docstring from a Python file or specific function."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Simple docstring extraction (module-level or function-level)
        import ast
        tree = ast.parse(content)

        if function_name:
            # Find specific function docstring
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    return ast.get_docstring(node) or "No docstring available"

        # Return module docstring
        return ast.get_docstring(tree) or "No docstring available"
    except Exception as e:
        return f"Error reading docstring: {str(e)}"


@mcp.tool
def list_components(
    type: Optional[Literal["app", "function"]] = None
) -> list[dict]:
    """
    List all components from the .libs directory.

    Component types:
    - 'app': Application with a single main entry point (index.yaml has 1 function)
    - 'function': Library with multiple public functions (index.yaml has multiple functions)

    Args:
        type: Optional type filter - 'app', 'function', or None for all components

    Returns:
        List of components with name and description
    """
    libs_dir = get_libs_directory()

    if not libs_dir.exists():
        return [{
            "error": f"Libraries directory not found: {libs_dir}"
        }]

    # Find all index.yaml files recursively
    index_files = find_all_index_files(libs_dir)

    if not index_files:
        return [{
            "error": "No index.yaml files found in .libs directory"
        }]

    # Collect components
    components = []

    for index_path, index_data in index_files:
        # Determine component type from this index.yaml
        component_type = get_component_type_from_index(index_data)

        # Filter by type if specified, otherwise include all
        if type is None or component_type == type:
            # Handle app format: { app: { name: ..., description: ... } }
            if "app" in index_data:
                app_data = index_data["app"]
                components.append({
                    "name": app_data.get("name", ""),
                    "description": app_data.get("description", "")
                })
            # Handle functions format: { functions: [ {...}, {...} ] }
            elif "functions" in index_data:
                functions = index_data.get("functions", [])
                for func in functions:
                    name = func.get("name", "")
                    description = func.get("description", "")

                    components.append({
                        "name": name,
                        "description": description
                    })

    return components


@mcp.tool
def get_details(
    type: Literal["app", "function"],
    name: str
) -> dict:
    """
    Get detailed information about a specific component.

    Args:
        type: Type of component - 'app' or 'function'
        name: Fully qualified name of the component (e.g., 'subdir1.subdir2.module.function')

    Returns:
        Component details including description (docstring) and root directory
    """
    libs_dir = get_libs_directory()

    if not libs_dir.exists():
        return {
            "error": f"Libraries directory not found: {libs_dir}",
            "name": name,
            "type": type
        }

    # Find all index.yaml files and search for this component
    index_files = find_all_index_files(libs_dir)

    component_index = None
    component_metadata = None

    for index_path, index_data in index_files:
        # Check app format
        if "app" in index_data:
            app_data = index_data["app"]
            if app_data.get("name") == name:
                component_index = index_path
                component_metadata = app_data
                break
        # Check functions format
        elif "functions" in index_data:
            functions = index_data.get("functions", [])
            for func in functions:
                if func.get("name") == name:
                    component_index = index_path
                    component_metadata = func
                    break
            if component_metadata:
                break

    if not component_metadata:
        return {
            "error": f"Component '{name}' not found in any index.yaml",
            "name": name,
            "type": type,
            "root_directory": str(libs_dir)
        }

    # Find the module path
    module_path = get_module_path(name, libs_dir)

    if not module_path:
        return {
            "error": f"Module file not found for component: {name}",
            "name": name,
            "type": type,
            "root_directory": str(libs_dir),
            "note": "Component exists in index.yaml but module file not found"
        }

    # Extract function name from fully qualified name
    parts = name.split('.')
    function_name = parts[-1] if len(parts) > 0 else None

    # Get docstring
    description = extract_docstring(module_path, function_name)

    # Get component directory
    component_dir = component_index.parent if component_index else module_path.parent

    return {
        "name": name,
        "type": type,
        "description": description,
        "short_description": component_metadata.get("description", ""),
        "module_path": str(module_path),
        "component_directory": str(component_dir.relative_to(libs_dir)),
        "root_directory": str(libs_dir)
    }


if __name__ == "__main__":
    mcp.run()
