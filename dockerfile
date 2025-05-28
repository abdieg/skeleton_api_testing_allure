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

# ---------- Allure CLI installation ----------
ENV ALLURE_VERSION=2.27.0
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget openjdk-11-jre-headless && \
    wget -q https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz && \
    tar -xzf allure-${ALLURE_VERSION}.tgz -C /opt && \
    ln -s /opt/allure-${ALLURE_VERSION}/bin/allure /usr/bin/allure && \
    rm allure-${ALLURE_VERSION}.tgz && \
    rm -rf /var/lib/apt/lists/*

# Create reports dir inside container
RUN mkdir -p /app/reports

# Command to run the application
CMD ["pytest"]