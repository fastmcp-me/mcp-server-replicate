# Implementation Notes

## Context Window Optimization

The server implements several optimizations to minimize context window usage when interacting with the Replicate API:

1. Model Metadata
   - Only essential fields are returned in model listings (owner, name, description, visibility)
   - Latest version information is minimal, including only ID and creation date
   - Descriptions are kept intact as they are important for model selection
   - Unnecessary fields like tags, architecture details, and license info are omitted
   - Pagination is enforced for model listings to prevent context window overflow
   - Default page size is optimized for typical LLM context windows
   - Response format is optimized for Claude's tool usage patterns

2. Version Information
   - Version listings include only critical metadata (id, created_at, cog_version)
   - OpenAPI schema is included for input validation but other verbose fields are omitted
   - Creation dates use consistent ISO format for predictable string lengths
   - Training details and model weights information are excluded

3. Prediction Results
   - Status responses include only necessary fields for tracking (id, status, output, error)
   - Timestamps use consistent ISO format
   - Error messages are concise but informative
   - URLs and metrics are included for complete status tracking
   - Raw model outputs are passed through without modification

4. Error Handling
   - Error responses use standard JSON-RPC error codes
   - Error messages are kept concise and actionable
   - Stack traces are logged but not included in responses
   - Validation errors include specific field information

These optimizations ensure efficient use of the context window while maintaining all necessary functionality. The balance between completeness and efficiency is achieved by:

- Including only fields that are directly useful to the client
- Using consistent data formats to aid in parsing
- Avoiding duplicate information across related endpoints
- Structuring responses to be easily parsed and validated

## FastMCP Implementation

The server uses FastMCP decorators and patterns for consistent tool implementation:

1. Tool Registration
   - Each tool is registered using the @server.tool() decorator
   - Tools use type hints for automatic schema generation
   - Context parameter is included for future extensibility
   - Optional parameters have clear default values

2. Error Handling
   - JSONRPCError is used for structured error responses
   - Error codes follow JSON-RPC standards
   - Errors are logged for debugging
   - Client errors (4xx) vs Server errors (5xx) are distinguished

3. Response Formatting
   - Consistent return types across all tools
   - Nested objects are flattened where possible
   - Date/time values use ISO format
   - Boolean flags are used instead of strings for status
