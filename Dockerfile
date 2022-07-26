# base image
FROM jupyter/minimal-notebook:latest

# name your environment and choose the python version
ARG conda_env=strategy-ratios
ARG py_ver=3.10.4

# install packages specified in requirements.txt
COPY --chown=${NB_UID}:${NB_GID} requirements.txt /tmp/
RUN pip install --quiet --no-cache-dir --requirement /tmp/requirements.txt && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# make this environment to be the default one, uncomment the following line:
RUN echo "conda activate ${conda_env}" >> "${HOME}/.bashrc"
