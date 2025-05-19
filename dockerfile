# Base image
FROM python:slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .


RUN pip install --no-cache-dir -e .

# Do not run training here (avoid credential requirement)

EXPOSE 5000

# Run training + app when container starts
CMD ["bash", "-c", "python pipeline/training_pipeline.py && python application.py"]
