# Stage 1: Build
FROM python:3.12-alpine AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    python3-dev

# Copy requirements and install Python dependencies
COPY requirements/ /app/requirements/
RUN pip install --no-cache-dir --prefix=/install -r /app/requirements/development.txt

# Stage 2: Runtime
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apk add --no-cache \
    libffi \
    libpq

# Copy installed dependencies from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Expose the application port
EXPOSE 8004

# Command to run the application
CMD ["/app/entrypoint.sh"]