# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Accept build-time UID and GID from host
ARG HOST_UID=1000
ARG HOST_GID=1000

# Set the working directory
WORKDIR /app

# Install dependencies required by Allure CLI and user management
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        default-jre-headless \
        ca-certificates \
        adduser \
        gosu \
    && rm -rf /var/lib/apt/lists/*

# Create a user with host-matching UID:GID
RUN addgroup --gid ${HOST_GID} appgroup && \
    adduser --uid ${HOST_UID} --gid ${HOST_GID} --disabled-password --gecos "" appuser

# Set the user environment
ENV HOME=/home/appuser
USER appuser

# Switch back to root to install Python dependencies and Allure
USER root

# Upgrade pip and install project requirements
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# ---------- Allure CLI installation ----------
ENV ALLURE_VERSION=2.27.0

RUN wget -q https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz && \
    tar -xzf allure-${ALLURE_VERSION}.tgz -C /opt && \
    rm allure-${ALLURE_VERSION}.tgz

ENV PATH="/opt/allure-${ALLURE_VERSION}/bin:$PATH"

# Copy source code after dependencies (to leverage layer caching)
COPY . /app

# Set permissions for appuser
RUN chown -R ${HOST_UID}:${HOST_GID} /app

# Switch back to the non-root user
USER appuser

# Create reports dir
RUN mkdir -p /app/reports

# Default command
CMD ["pytest"]