# syntax=docker/dockerfile:1

FROM continuumio/miniconda3:latest

# Install base utilities
# RUN apt-get update && \
#     apt-get install -y default-libmysqlclient-dev && \
#     apt-get install -y wget && \
#     apt-get install -y build-essential && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY expertfinder-production.yml .
RUN conda create --name expertfinder-production python=3.9

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "expertfinder-production", "/bin/bash", "-c"]
RUN conda env update --file expertfinder-production.yml --prune


# Demonstrate the environment is activated:
RUN echo "Make sure flask is installed:"
RUN python -c "import flask"

# The code to run when container is started:
COPY . .

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "expertfinder-production", "python", "app.py"]