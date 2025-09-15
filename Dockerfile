# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only source code and data needed
COPY src/ ./src
COPY data/ ./data

# Expose the Dash port
EXPOSE 8050

# Command to run the dashboard
CMD ["python", "src/dashboard_app.py"]