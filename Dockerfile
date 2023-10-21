# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the contents of the directory into the container at /app/
COPY . /app

# Expose port 8080
EXPOSE 8080

# Install dependencies, combine commands, and remove cache
RUN pip install -r /app/requirements.txt --no-cache-dir \
    && playwright install --with-deps chromium

# Run Start.py when the container launches
CMD ["python", "-u", "/app/Start.py"]
