# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=myapp.settings
ENV PYTHONUNBUFFERED=1

# Create and set the working directory in the container
RUN mkdir /app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Collect static files (if applicable)
RUN python manage.py collectstatic --noinput

# Expose the port the application will run on
EXPOSE 8000

# Start the Django application using Gunicorn (adjust the command as needed)
CMD ["gunicorn", "myapp.wsgi:application", "--bind", "0.0.0.0:8000"]
