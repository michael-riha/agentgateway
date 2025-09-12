#!/bin/bash
set -e

SERVICE_NAME="mcp-server"  # Your service name

echo "Running ruff to fix all issues automatically..."
# This replaces autoflake, isort, and flake8
docker compose run --rm $SERVICE_NAME ruff check --fix --select E,F,I,W,UP --ignore E203 .

echo "Formatting code with black..."
docker compose run --rm $SERVICE_NAME black -v .

# Final check to see if any issues remain that need manual fixing
echo "Checking for remaining issues with ruff..."
docker compose run --rm $SERVICE_NAME ruff check .

# TODO: too exhausting to fix for now!
# echo "Type checking with mypy..."
# docker compose run --rm $SERVICE_NAME mypy --install-types .

echo "All formatting completed!"