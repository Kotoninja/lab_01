#!/bin/bash

echo "🚀 Running checks..."

# 1. Ruff
if ! uv run ruff check . --quiet; then
    echo "❌ Tests failed! Running full ruff output below:"
    uv run ruff check .
    exit 1
fi

# 2. Mypy
if ! uv run mypy . --no-error-summary; then
    echo "❌ Tests failed! Running full mypy output below:"
    uv run mypy .
    exit 1
fi

# 3. Pytest (completely hidden unless it fails)
if ! uv run pytest . -q --no-header --no-summary > /dev/null 2>&1; then
    echo "❌ Tests failed! Running full pytest output below:"
    uv run pytest .
    exit 1
fi

echo "✅ All checks passed successfully!"
