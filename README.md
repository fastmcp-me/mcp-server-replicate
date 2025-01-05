# MCP Server for Replicate API

A Model Context Protocol (MCP) server implementation for the Replicate API, enabling AI model inference through a standardized protocol.

## Features

- FastMCP server implementation using MCP SDK 1.2.0+
- Integration with Replicate API for model inference
- Decorator-based tool definitions
- Standardized tool and resource interfaces
- Modern Python development practices

## Requirements

- Python 3.11+
- [UV](https://github.com/astral-sh/uv) for dependency management
- Replicate API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mcp-server-replicate.git
cd mcp-server-replicate
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Replicate API key
```

3. Install dependencies using UV:
```bash
uv pip install --system
```

## Development

This project uses UV for dependency management and virtual environment handling. Here are some common commands:

### Adding Dependencies

```bash
# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev package-name
```

### Running Commands

```bash
# Run a command in the virtual environment
uv run python script.py

# Run an installed CLI tool
uv run cli-tool-name

# Run a command without installing (one-off execution)
uvx cli-tool-name
```

### Managing Dependencies

```bash
# Update dependencies
uv pip sync

# Show outdated packages
uv pip list --outdated
```

## Project Structure

```
mcp-server-replicate/
├── .env.example        # Example environment variables
├── .gitignore         # Git ignore rules
├── README.md          # Project documentation
├── NOTES.md           # Implementation notes and guidelines
├── TASKS.md           # Development tasks and roadmap
├── TESTING.md         # Testing guidelines and practices
├── WORKFLOW.md        # Development workflow documentation
├── pyproject.toml     # Project metadata and dependencies
├── src/               # Source code directory
│   └── mcp_server_replicate/
│       ├── __init__.py
│       └── server.py  # FastMCP server implementation
├── tests/             # Test directory
│   ├── __init__.py
│   └── test_server.py # Server tests
└── uv.lock            # Locked dependencies
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes using [Conventional Commits](https://www.conventionalcommits.org/):
   ```bash
   git commit -m "feat: add amazing feature"
   git commit -m "fix: resolve issue with something"
   ```
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
