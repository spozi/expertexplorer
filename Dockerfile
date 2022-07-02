# syntax=docker/dockerfile:1

FROM continuumio/miniconda3:latest

# Install base utilities
# RUN apt-get update && \
#     apt-get install -y default-libmysqlclient-dev && \
#     apt-get install -y wget && \
#     apt-get install -y build-essential && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# Install miniconda
# ENV CONDA_DIR /opt/conda
# RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
#     /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
# ENV PATH=$CONDA_DIR/bin:$PATH

WORKDIR /app

COPY expertfinder-production.yml .
RUN conda create --name expertfinder-production python=3.9
# RUN conda activate expertfinder-production
# RUN conda env update --file expertfinder-production.yml --prune
# RUN conda env create -f expertfinder-production.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "expertfinder-production", "/bin/bash", "-c"]
RUN conda env update --file expertfinder-production.yml --prune


# Demonstrate the environment is activated:
RUN echo "Make sure flask is installed:"
RUN python -c "import flask"

# The code to run when container is started:
COPY . .
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "expertfinder-production", "python", "app.py"]