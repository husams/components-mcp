# FastMCP Documentation - Table of Contents

## Getting Started

- [Welcome to FastMCP 2.0](welcome.md)
  - Beyond Basic MCP
  - What is MCP?
  - Why FastMCP?
  - LLM-Friendly Docs

- [Installation](installation.md)
  - Install FastMCP
  - Verify Installation
  - Dependency Licensing
  - Upgrading from the Official MCP SDK
  - Versioning Policy
  - Contributing to FastMCP

- [Quickstart](quick_start.md)
  - Create a FastMCP Server
  - Add a Tool
  - Run the Server
  - Call Your Server
  - Deploy to FastMCP Cloud

## Core Concepts

- [The FastMCP Server](overview.md)
  - Creating a Server
  - Components (Tools, Resources, Prompts)
  - Tag-Based Filtering
  - Running the Server
  - Custom Routes
  - Composing Servers
  - Proxying Servers
  - OpenAPI Integration
  - Server Configuration

- [Tools](tools.md)
  - The `@tool` Decorator
  - Tool Parameters and Return Values
  - Input Validation Modes
  - Error Handling

- [Decorating Methods](decorating_methods.md)
  - Why Are Methods Hard?
  - Instance Methods
  - Class Methods
  - Static Methods
  - Best Practices

- [Resources & Templates](resources.md)
  - Resource URIs
  - Resource Templates
  - Dynamic Resources
  - Resource Metadata

- [Prompts](prompts.md)
  - Creating Prompts
  - Prompt Arguments
  - Message Templates
  - Prompt Metadata

## Advanced Features

- [Server Composition](composition.md)
  - Importing Servers
  - Mounting Servers
  - Server Prefixes and Namespacing

- [Tool Transformation](tool_transformation.md)
  - Why Transform Tools?
  - Basic Transformation
  - Modifying Schemas
  - Argument Mapping
  - Custom Behavior

- [MCP Context](context.md)
  - Accessing Context
  - Context Variables
  - Request Information

- [User Elicitation](elicitation.md)
  - Interactive User Input
  - Form-Based Elicitation
  - Validation

- [LLM Sampling](llm_sampling.md)
  - Calling LLMs from Tools
  - Sampling Configuration
  - Model Selection

- [Progress Reporting](progress_reporting.md)
  - Progress Notifications
  - Long-Running Operations
  - Progress Tracking

- [Client Logging](logging.md)
  - Log Levels
  - Structured Logging
  - Client-Side Logs

- [MCP Middleware](middleware.md)
  - What is MCP Middleware?
  - Creating Middleware
  - Middleware Chains
  - Use Cases

- [Storage Backends](storage_backend.md)
  - Persistent Storage
  - Storage Providers
  - Configuration

## Development & Testing

- [Testing Your Server](testing.md)
  - Testing with FastMCP Client
  - Pytest Fixtures
  - Test Best Practices
  - Using Inline Snapshots

## Deployment & Configuration

- [FastMCP CLI](cli.md)
  - Commands Overview
  - Running Servers
  - Development Mode
  - Installing Servers
  - Project Management

- [Running Your Server](running_your_server.md)
  - Transport Options
  - STDIO Transport
  - HTTP Transport
  - Server Lifecycle

- [HTTP Deployment](http_deployment.md)
  - HTTP Configuration
  - Authentication
  - CORS and Security
  - Production Deployment

- [Project Configuration](project_configuration.md)
  - Environment Variables
  - Configuration Files
  - Server Discovery
  - CLI Configuration

---

**Note**: This documentation reflects FastMCP's `main` branch and may include features not yet released. Features are generally marked with version badges (e.g. `New in version: 2.13.1`) to indicate when they were introduced.
