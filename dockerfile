FROM python:3.10-slim

ARG HOST_UID=1000
ARG HOST_GID=1000

# Create working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        default-jre-headless \
        ca-certificates \
        adduser \
        git \
    && rm -rf /var/lib/apt/lists/*

# Create group and user matching host UID/GID
RUN addgroup --gid ${HOST_GID} appgroup && \
    adduser --uid ${HOST_UID} --gid ${HOST_GID} --disabled-password --gecos "" appuser

# Upgrade pip and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Allure CLI
ENV ALLURE_VERSION=2.27.0
RUN wget -q https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz && \
    tar -xzf allure-${ALLURE_VERSION}.tgz -C /opt && \
    rm allure-${ALLURE_VERSION}.tgz

ENV PATH="/opt/allure-${ALLURE_VERSION}/bin:$PATH"

# Copy application code
COPY . .

# Ensure reports folder is ready and owned
RUN mkdir -p /app/reports && chown -R ${HOST_UID}:${HOST_GID} /app

# Switch to non-root user at runtime (not during build!)
USER appuser

# Default command
CMD ["pytest"]