# Dockerfile
FROM python:3.11-slim

# Create a non-root user (e.g., "appuser")
RUN adduser --disabled-password --gecos '' appuser

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY backend /

# Change to the non-root user
USER appuser

# Expose the port that the app uses
EXPOSE 8080

# Command to start the application
CMD ["python", "main.py"]