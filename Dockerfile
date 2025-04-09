# Use the official Python 3.12.7 slim image
FROM python:3.12.7-slim

# Set the working directory inside the container
WORKDIR /app

# Install system-level dependencies required for PostgreSQL and building Python packages
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements folder with all files
COPY requirements/ /app/requirements/

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements/development.txt

# Copy the entire project into the container
COPY . .

# Expose the port Django will run on
EXPOSE 8004

# Make the script executable
RUN chmod +x /app/entrypoint.sh

# Set the shell script as the default command
CMD ["/app/entrypoint.sh"]
