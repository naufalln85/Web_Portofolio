FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Collect static files (settings.py will be built to handle default/dummy environment variables during build)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Run the app with gunicorn
CMD ["gunicorn", "portfolio_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
