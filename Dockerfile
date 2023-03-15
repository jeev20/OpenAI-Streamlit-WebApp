# This dockerfile content was in majority written by ChatGPT 3.5 turbo
# Promt: help write a dockerfile to deploy a streamlit application on docker

# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose port for the Streamlit app
EXPOSE 8501

# Run app.py when the container launches
CMD ["streamlit", "run", "OpenAI_Demos.py"]