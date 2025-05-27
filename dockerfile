# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Force pytest-html greater than 4.2.1 to fix banner issue
RUN pip install --no-cache-dir "pytest-html>=4.2.1"

# Create reports dir inside container
RUN mkdir -p /app/reports

# Command to run the application
CMD ["pytest"]