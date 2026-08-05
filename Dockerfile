# Use official lightweight Python 3.12 image
FROM python:3.12-slim

# Copy uv binary directly from official Astral registry image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install required runtime dependencies using uv
RUN uv pip install --system duckdb pandas

# Copy application source code
COPY src/ ./src/

# Default entry point runs the database verification suite
CMD ["python", "src/validate_staging.py"]