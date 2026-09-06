FROM python:3.12-slim

# Install system dependencies (C compilers / curl required for C-extensions)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy uv and uvx binaries directly from official Astral registry image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy project specification files
COPY pyproject.toml uv.lock README.md* ./

# Install project dependencies into container environment
RUN uv sync --frozen --no-install-project

# Copy source scripts and configuration
COPY src/ ./src/
COPY Snakefile ./

# Default entrypoint runs Snakemake pipeline inside container
CMD ["uv", "run", "snakemake", "--cores", "1"]