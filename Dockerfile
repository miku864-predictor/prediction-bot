# Use a lightweight base image
FROM python:3.12-slim

# Install system dependencies for Chromium and WebDriver
RUN apt-get update && apt-get install -y \
    chromium chromium-driver \
    fonts-liberation \
    wget unzip curl gnupg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Chromium
ENV PATH="/usr/lib/chromium/:${PATH}"
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER=/usr/bin/chromedriver

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run script
CMD ["python", "main.py"]
