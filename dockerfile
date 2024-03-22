# Use Ubuntu 20.04 as base image
FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install Python 2.7 and pip
RUN apt-get update && apt-get install -y \
    python2.7 \
    python-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create symbolic links for Python 2.7
RUN ln -s /usr/bin/python2.7 /usr/local/bin/python
RUN ln -s /usr/bin/python2.7 /usr/local/bin/python2

# Install necessary libraries
RUN pip install --upgrade pip

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port
EXPOSE 8000

# Command to run your application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]