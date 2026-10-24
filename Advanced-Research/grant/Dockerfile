# GraNT Framework - Production Docker Image
# Multi-stage build for optimal size and security

# ============================================================================
# Stage 1: Builder
# ============================================================================
FROM python:3.11-slim as builder

LABEL maintainer="NeuralBlitz <NuralNexus@icloud.com>"
LABEL description="GraNT Framework - Next-Generation ML/AI Architecture"

# Set working directory
WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# ============================================================================
# Stage 2: Runtime
# ============================================================================
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/root/.local/bin:$PATH

# Create app user for security
RUN useradd -m -u 1000 grant && \
    mkdir -p /app /data /outputs && \
    chown -R grant:grant /app /data /outputs

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=grant:grant . .

# Install package in development mode
RUN pip install --no-cache-dir -e .

# Switch to non-root user
USER grant

# Expose ports (if needed for API)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import grant; print('OK')" || exit 1

# Default command: run demo
CMD ["python", "examples/complete_demo.py"]

# ============================================================================
# Build and Run Instructions
# ============================================================================
# 
# Build:
#   docker build -t grant-framework:latest .
#
# Run demo:
#   docker run --rm grant-framework:latest
#
# Interactive mode:
#   docker run -it --rm grant-framework:latest /bin/bash
#
# Mount volumes:
#   docker run --rm \
#     -v $(pwd)/data:/data \
#     -v $(pwd)/outputs:/outputs \
#     grant-framework:latest
#
# GPU support (requires nvidia-docker):
#   docker run --rm --gpus all grant-framework:latest
# ============================================================================
