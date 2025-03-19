FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose ports for both Streamlit and FastAPI
EXPOSE 8501
EXPOSE 8000

CMD ["sh", "-c", "streamlit run app.py & uvicorn api:app --host 0.0.0.0 --port 8000"] 