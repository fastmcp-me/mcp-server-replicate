# Development Workflow

This document outlines our core development workflow for the MCP Server Replicate project.

## Core Development Loop

1. **Planning**
   - Review requirements and existing code
   - Check documentation (especially NOTES.md)
   - Plan implementation approach
   - Understand FastMCP patterns and best practices

2. **Testing**
   - Write tests first (TDD approach)
   - Test environment validation
   - Test tool registration and schemas
   - Test error conditions
   - Run tests with `uv run pytest`

3. **Implementation**
   - Write code to pass tests
   - Use FastMCP decorators and type hints
   - Add clear docstrings for API docs
   - Handle error cases with JSONRPCError
   - Validate environment variables early

4. **Verification**
   - Run full test suite
   - Run linters (ruff, black, mypy)
   - Review changes for clarity
   - Update documentation
   - Check type hints and schemas

5. **Integration**
   - Update TASKS.md
   - Update NOTES.md with new patterns
   - Commit with conventional commits
   - Push changes

## Key Principles

- Write tests before implementation (TDD)
- Use FastMCP patterns consistently
- Keep documentation comprehensive
- Follow code style guidelines
- Handle errors with JSON-RPC
- Validate environment early

## FastMCP Patterns

### Tool Definition
```python
@server.tool()
async def my_tool(
    ctx: Context,  # MCP context
    param: str,    # Required parameter
    opt: int | None = None,  # Optional parameter
) -> Any:
    """Tool description here."""
    # Implementation
```

### Error Handling
```python
raise JSONRPCError(
    jsonrpc="2.0",
    id=0,  # FastMCP handles this
    error=ErrorData(
        code=METHOD_NOT_FOUND,
        message="Clear error message"
    )
)
```

### Environment Validation
```python
def validate_environment() -> None:
    load_dotenv()
    if not os.getenv("REQUIRED_VAR"):
        raise ValueError("REQUIRED_VAR missing")
```

## Commands

```bash
# Run tests
uv run pytest
uv run pytest -v  # Verbose output
uv run pytest -k "test_name"  # Run specific test

# Run linters
uv run ruff check .
uv run black --check .
uv run mypy .

# Format code
uv run black .
uv run ruff --fix .
