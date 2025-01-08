# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files and enable output buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files into the working directory
COPY . /app/
# Set up environment variables for Django
# Update this based on your database credentials (use Docker Compose for better secrets management)
ENV DB_NAME=booking_system \
    DB_USER=postgres \
    DB_PASSWORD=admin \
    DB_HOST=db \
    DB_PORT=5432

# Expose the application port
EXPOSE 8000

# Run migrations and start the Django development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && \
    echo \"from django.contrib.auth.models import User; \
    User.objects.filter(username='admin').exists() or \
    User.objects.create_superuser('admin', 'admin@admin.com', 'admin')\" | python manage.py shell && \
    python manage.py runserver 0.0.0.0:8000"]

