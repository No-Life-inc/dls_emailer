# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install poetry
RUN pip install --no-cache-dir poetry

# Install dependencies using poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi


# Make port 5050 available to the world outside this container
EXPOSE 5050

# Run subscriber.py when the container launches
CMD ["python", "./src/emailer.py"]

