FROM python:3.11-slim

WORKDIR /app

# Install debugpy and other system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY mcp_server/requirements .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY mcp_server/ .

# Expose ports: 8000 for potential HTTP transport, 5678 for debugpy
EXPOSE 8000 5678

# Set Python path
ENV PYTHONPATH=/app

# Run the server with debugpy
# CMD ["python", "server.py"]
