# Debian Jessie debootstrap from 2017-02-27
# https://github.com/docker-library/official-images/commit/aa5973d0c918c70c035ec0746b8acaec3a4d7777
FROM debian@sha256:52af198afd8c264f1035206ca66a5c48e602afb32dc912ebf9e9478134601ec4

MAINTAINER Jonas Paul Westermann <jonas.westermann@barcelonagse.com>

USER root

# Install all OS dependencies for notebook server that starts but lacks all
# features (e.g., download as all possible file formats)
ENV DEBIAN_FRONTEND noninteractive
RUN REPO=http://cdn-fastly.deb.debian.org \
 && echo "deb $REPO/debian jessie main\ndeb $REPO/debian-security jessie/updates main" > /etc/apt/sources.list \
 && apt-get update && apt-get -yq dist-upgrade \
 && apt-get install -yq --no-install-recommends \
    wget \
    bzip2 \
    ca-certificates \
    sudo \
    locales \
    git \
    curl \
    fonts-liberation \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Install Tini
RUN wget --quiet https://github.com/krallin/tini/releases/download/v0.10.0/tini && \
    echo "1361527f39190a7338a0b434bd8c88ff7233ce7b9a4876f3315c22fce7eca1b0 *tini" | sha256sum -c - && \
    mv tini /usr/local/bin/tini && \
    chmod +x /usr/local/bin/tini

# Configure environment
ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/bin:$PATH
ENV SHELL /bin/bash
ENV NB_USER econ_user
ENV NB_UID 1000
ENV HOME /home/$NB_USER
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Create econ_user user with UID=1000 and in the 'users' group
RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && \
    mkdir -p $CONDA_DIR && \
    chown $NB_USER $CONDA_DIR

USER $NB_USER

# Install conda as econ_user and check the md5 sum provided on the download site
ENV MINICONDA_VERSION 4.3.21
RUN cd /tmp && \
    mkdir -p $CONDA_DIR && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    echo "c1c15d3baba15bf50293ae963abef853 *Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh" | md5sum -c - && \
    /bin/bash Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    $CONDA_DIR/bin/conda config --system --prepend channels conda-forge && \
    $CONDA_DIR/bin/conda config --system --set auto_update_conda false && \
    $CONDA_DIR/bin/conda config --system --set show_channel_urls true && \
    $CONDA_DIR/bin/conda update --all && \
    conda clean -tipsy

# Install Jupyter Notebook and Hub
RUN conda install --quiet --yes \
    'notebook=5.0.*' \
    'jupyterhub=0.7.*' \
    'jupyterlab=0.24.*' \
    && conda clean -tipsy

USER root

EXPOSE 8888
WORKDIR $HOME

# Setup notebook directory in the user directory
RUN git clone https://github.com/Westermann/Luminosity
WORKDIR $HOME/Luminosity/
RUN git checkout lights_on
WORKDIR $HOME/Luminosity/lights_on
RUN conda install --quiet --yes \
		--file requirements.txt
RUN mkdir figures
RUN mkdir -p data/downloads/Version_4_DMSP-OLS_Nighttime_Lights_Time_Series
RUN mkdir -p data/nightlights/year
RUN chmod -R +x src
RUN src/setup/get_Version-4-DMSP-OLS-Nighttime-Lights-Composites.sh
RUN python src/setup/compress_Version-4-DMSP-OLS-Nighttime-Lights-Composites.py
RUN rm -r data/downloads
RUN chown -R $NB_USER:users $HOME

# # Configure container startup
ENTRYPOINT ["tini", "--"]
CMD ["jupyter", "notebook", "--no-browser"]

# # Add local files as late as possible to avoid cache busting
COPY start.sh /usr/local/bin/
COPY start-singleuser.sh /usr/local/bin/
COPY jupyter/jupyter_notebook_config.py /etc/jupyter/
RUN mkdir -p $HOME/.jupyter
COPY jupyter $HOME/.jupyter/custom
RUN chown -R $NB_USER:users /etc/jupyter/

# # Switch back to econ_user to avoid accidental container runs as root
USER $NB_USER

