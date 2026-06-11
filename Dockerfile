FROM --platform=$TARGETPLATFORM python:3.9-slim

WORKDIR /app

# Install system dependencies (required for some Python libraries)
RUN apt-get update && apt-get install -y \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Environment variables configuration
ENV TV_IP="" \
    TV_MAC="" \
    TV_KEY="" \
    MY_PC_IP="" \
    MY_PC_MAC="" \
    DAD_PC_IP="" \
    DAD_PC_MAC=""

# Expose the port that the application runs on
EXPOSE 8080

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

