# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose port (Render will use the PORT env variable)
EXPOSE 5000

# Use gunicorn for production (more stable than Flask dev server)
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app
