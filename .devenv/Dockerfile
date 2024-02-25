################################################################################
FROM phusion/baseimage:jammy-1.0.1

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update --yes && apt-get upgrade --yes && \
    apt-get install --yes --no-install-recommends \
    git vim screen curl ssh \
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3-pip \
    python3-wheel \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# PYTHON SETUP & VIRTUAL ENV
RUN python3.11 -m venv /root/venv
ENV VIRTUAL_ENV=/root/venv
ENV PATH="/root/venv/bin:$PATH"
# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# Create and setup work dir
WORKDIR /root/app
COPY . .
RUN pip3 install --upgrade pip
RUN python3 -m pip install --upgrade setuptools
RUN pip3 install jupyterlab
RUN pip3 install -e .[dev]

# NOTE: This does not actually publish the port on its own.
# One must use docker run with the `-P` flag to publish all
# ports exposed this way.
EXPOSE 8888

ENV SHELL=/bin/bash
CMD ["jupyter-lab","--ip=0.0.0.0","--port=8888","--no-browser","--allow-root"]
################################################################################
