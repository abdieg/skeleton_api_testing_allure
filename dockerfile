# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Upgrade pip because old pip sometimes chokes on newer metadata
RUN pip install --no-cache-dir --upgrade pip

# Install project requirements
RUN pip install --no-cache-dir -r requirements.txt

# Install git so pip can pull packages directly from GitHub
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

# Force pytest-html (main branch, banner fix) via git URL
RUN pip install --no-cache-dir "git+https://github.com/pytest-dev/pytest-html@main#egg=pytest-html"

# Create reports dir inside container
RUN mkdir -p /app/reports

# Command to run the application
CMD ["pytest"]