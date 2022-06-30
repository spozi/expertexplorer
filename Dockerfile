# syntax=docker/dockerfile:1

FROM --platform=linux/amd64 python:3.9.12-slim

# Install base utilities
RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev && \
    apt-get install -y wget && \
    apt-get install -y build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH

WORKDIR /app

COPY environment.yml .
RUN conda env create -f environment.yml

# The code to run when container is started:
COPY . .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
# ENTRYPOINT ["./entrypoint.sh"]