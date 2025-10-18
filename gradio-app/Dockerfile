# Backend (Gradio ML App) Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from gradio-app directory
COPY gradio-app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files from gradio-app directory
COPY gradio-app/app.py .

# Copy ML models and data from project root
COPY ml ./ml
COPY data ./data

# Expose Gradio port
EXPOSE 7860

# Run Gradio app (accessible from outside container)
CMD ["python", "app.py"]
