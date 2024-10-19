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
COPY . /Rule-Engine-with-AST

# Expose the port FastAPI will run on (default: 8000)
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
