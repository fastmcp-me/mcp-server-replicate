# Use the official Python image with a version that matches our needs
FROM python:3.11-slim-bookworm AS base

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and the lock file to the container
COPY pyproject.toml uv.lock /app/

# Install UV for dependency management
RUN pip install uv

# Install the dependencies using UV
RUN uv sync --frozen --no-install-project --no-dev --no-editable

# Copy the project files into the container
COPY src/ /app/src/

# Ensure the entrypoint is executable
RUN chmod +x /app/src/mcp_server_replicate/__main__.py

# Specify the command to run the MCP server
CMD ["uv", "tool", "run", "mcp-server-replicate"]

# Set environment variable for API token (to be overridden when running the container)
ENV REPLICATE_API_TOKEN=your_api_key_here