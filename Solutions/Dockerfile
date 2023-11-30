# Use an official Python image as a base image.
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


ENV secret_key "YOUR SECRET KEY FOR STRIPE" 
ENV public_key "YOUR PUBLIC KEY FOR STRIPE"

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN python manage.py migrate --run-syncdb 
# Make port 80 available to the world outside this container
EXPOSE 8000

# Run server when starting the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]