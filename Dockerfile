# This dockerfile content was in majority written by ChatGPT 3.5 turbo
# Promt: help write a dockerfile to deploy a streamlit application on docker

# Use an official Python runtime as a parent image
FROM python:3.7-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Update pip 
RUN /usr/local/bin/python -m pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose port for the Streamlit app
EXPOSE 8501

# Run app.py when the container launches
CMD ["streamlit", "run", "OpenAI_Demos.py"]