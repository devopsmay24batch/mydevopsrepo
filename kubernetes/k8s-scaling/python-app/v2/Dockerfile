# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python application files to the container
COPY app.py .

# Install Flask
RUN pip install Flask

# Specify the command to run the application
CMD ["python", "app.py"]
