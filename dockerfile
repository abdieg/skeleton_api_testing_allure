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

# Force pytest-html greater than 4.2.1 to fix banner issue
RUN pip install --no-cache-dir "git+https://github.com/pytest-dev/pytest-html@main#egg=pytest-html"

# Create reports dir inside container
RUN mkdir -p /app/reports

# Command to run the application
CMD ["pytest"]