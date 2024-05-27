# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install flask pandas langchain_openai pandasai psycopg2-binary

# Make port 5555 available to the world outside this container
EXPOSE 5555

# Define environment variable for OpenAI API key
ENV OPENAI_API_KEY=""

# Run app.py when the container launches
CMD ["python", "app.py"]