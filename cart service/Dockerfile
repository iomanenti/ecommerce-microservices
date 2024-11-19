# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the service files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir Flask

# Expose the port the service will run on
EXPOSE 5003

# Run the application
CMD ["python", "app.py"]