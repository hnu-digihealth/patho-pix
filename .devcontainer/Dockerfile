FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG USER=vscode
RUN apt update \
    && apt install -y --no-install-recommends curl wget git sudo build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
    && apt autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && usermod -s /usr/bin/zsh ${USER}

# Install required software dependencies (openslide)
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-dev python3-opencv libpython3.10-dev libvips-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

USER ${USER}
ARG HOME="/home/${USER}"
WORKDIR ${HOME}

ARG PYTHON_VERSION=3.8
ENV PYENV_ROOT=${HOME}/.pyenv
ARG PYENV_PATH="${PYENV_ROOT}/bin:${PYENV_ROOT}/shims"
ARG PDM_PATH="${HOME}/.local/bin"
ENV PATH="${PYENV_PATH}:${PDM_PATH}:$PATH"
RUN set -x \
    && curl http://pyenv.run | bash \
    && echo 'eval "$(pyenv init -)"' >>${HOME}/.zshrc \
    && pyenv install -v ${PYTHON_VERSION} \
    && pyenv global ${PYTHON_VERSION}

ARG ZSH_CUSTOM=${HOME}/.oh-my-zsh/custom
RUN curl -sSL https://pdm.fming.dev/install-pdm.py | python - \
    && mkdir ${ZSH_CUSTOM}/plugins/pdm \
    && pdm completion zsh > ${ZSH_CUSTOM}/plugins/pdm/_pdm \
    && sed -i "s|^plugins=(|&pdm |" ${HOME}/.zshrc
