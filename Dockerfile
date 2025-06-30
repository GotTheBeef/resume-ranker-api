# Use an official lightweight Python image
FROM python:3.11-slim

# Prevent .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir uvicorn

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8080

# Run the FastAPI app with uvicorn, using 1 worker for small deployments
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]