# dockerAI
YouTube Video: Build AI Agents with Docker, Here’s How

## Instructions

Here's a basic Dockerfile that should work for this purpose:

```dockerfile
# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python script into the container
COPY hello_world.py .

# Run the Python script when the container launches
CMD ["python", "hello_world.py"]
```

This Dockerfile does the following:

1. Uses the official Python 3.9 slim image as the base.
2. Sets the working directory inside the container to `/app`.
3. Copies your `hello_world.py` file into the container.
4. Specifies the command to run when the container starts, which is to execute the Python script.

To use this Dockerfile:

1. Make sure your Python script is named `hello_world.py` and is in the same directory as the Dockerfile.
2. Build the Docker image using: `docker build -t hello-world-python .`
3. Run the container using: `docker run hello-world-python`

Would you like me to explain any part of this Dockerfile or provide more information about using Docker with Python?

### Data set creation using LLM prompting
give me 10 idesas for a simple dataset for LLM fine-tuning

let's go with idea #1

create a new CSV dataset, with 30 rows, with 5 different columns