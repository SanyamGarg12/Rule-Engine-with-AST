# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Install system dependencies required for psycopg2 (PostgreSQL)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    pkg-config \
    && apt-get clean

# Set the working directory in the container
WORKDIR /Rule-Engine-with-AST

# Copy the requirements file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files to the container
COPY . .

# Expose the port FastAPI will run on (default: 8000)
EXPOSE 8000

# Set environment variables (e.g., for DATABASE_URL)
# You can define a default value or leave it blank for users to override
ENV DATABASE_URL="postgresql://rule_user:1234567@host.docker.internal:5433/rule_engine"

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
