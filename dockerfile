# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Upgrade pip because old pip sometimes chokes on newer metadata
RUN pip install --no-cache-dir --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Force pytest-html (latest main, banner fix) without needing git
RUN pip install --no-cache-dir "pytest-html @ https://github.com/pytest-dev/pytest-html/archive/refs/heads/main.zip"

# Create reports dir inside container
RUN mkdir -p /app/reports

# Command to run the application
CMD ["pytest"]