# Testing Guidelines

This document outlines testing practices and standards for the MCP Server Replicate project.

## Test Structure

- Tests are located in the `tests/` directory
- Test files mirror the source structure with `test_` prefix
- Each test file focuses on a specific component/module
- Use pytest fixtures for common setup/teardown

## Test Categories

1. **Environment Tests**
   - Test environment variable validation
   - Test .env file loading
   - Test error handling for missing/invalid variables
   - Example:
     ```python
     def test_env_validation(monkeypatch):
         monkeypatch.setenv("REQUIRED_VAR", "value")
         # Should not raise
         validate_environment()
     ```

2. **FastMCP Tests**
   - Test tool registration and schemas
   - Test tool execution and error handling
   - Test async functionality with pytest-asyncio
   - Example:
     ```python
     @pytest.mark.asyncio
     async def test_tool_registration():
         tools = await server.list_tools()
         assert "tool_name" in [t.name for t in tools]
     ```

3. **Integration Tests**
   - Test complete workflows
   - Test API interactions
   - Test error propagation
   - Example:
     ```python
     @pytest.mark.asyncio
     async def test_prediction_workflow():
         result = await predict(ctx, model="model", input={})
         assert result is not None
     ```

## Best Practices

### Avoid Exception Testing
- Do not test for specific exceptions using pytest.raises
- Instead, test the actual state/behavior that would occur
- Focus on validating the correct functioning rather than error cases
- Example:
  ```python
  # Bad - Testing for exception
  with pytest.raises(ValueError):
      result = validate_input("")
      
  # Good - Testing actual state
  result = validate_input("")
  assert result.is_valid is False
  assert result.client is None
  ```

### Testing FastMCP Tools
- Test tool registration
- Test parameter validation
- Test error responses
- Test async behavior
- Test context usage

### Testing Environment
- Use monkeypatch for environment variables
- Test .env file loading
- Test validation failures
- Test empty/invalid values

### Testing Error Handling
- Test JSON-RPC error responses
- Verify error codes and messages
- Test unexpected errors
- Test error propagation

## Test Fixtures

```python
@pytest.fixture
def mock_env(monkeypatch):
    """Set up test environment variables."""
    monkeypatch.setenv("REPLICATE_API_TOKEN", "test_token")
    return monkeypatch

@pytest.fixture
def mock_client():
    """Create a mock Replicate client."""
    return Mock(spec=replicate.Client)
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/test_server.py

# Run tests matching pattern
uv run pytest -k "test_pattern"

# Run with verbose output
uv run pytest -v
```

## Coverage Requirements

- Minimum 90% code coverage
- 100% coverage for critical paths
- Coverage reports in HTML: `uv run pytest --cov=src --cov-report=html`

## Mocking Guidelines

- Mock external services (Replicate API)
- Mock environment variables with monkeypatch
- Mock file system operations when needed
- Document mock behavior clearly

## Test Data

- Use fixtures for test data
- Keep test data minimal
- Use meaningful sample values
- Document data requirements

## Continuous Integration

- Tests run on every commit
- All tests must pass before merge
- Coverage reports generated
- Test results archived

## Troubleshooting

Common test issues and solutions:
1. **Environment Issues**: Use monkeypatch and clean environment
2. **Async Tests**: Use pytest-asyncio and proper markers
3. **Import Issues**: Check module paths and imports
4. **Coverage Issues**: Check excluded lines
