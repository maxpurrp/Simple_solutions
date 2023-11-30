# Use an official Python image as a base image.
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


ENV secret_key sk_test_51OHpX0FhC9Kku47zLIS8kRWCginjZyZtlMeehDO8pOm9rEpjGtRoe3D2BvR4FiLMX4lTVfyjP40BJBTIzg9eEMTU00lCwZaxta
ENV public_key pk_test_51OHpX0FhC9Kku47zBtSoRkMqGscHbJkcJUBGVx04TklLYT8t7xT1pDUYtNJxG2PLaF3193aK7QoPTlomrmfoZkqt00n8Ez6BlA

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8000

# Run server when starting the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]