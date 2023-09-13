FROM mcr.microsoft.com/devcontainers/universal:2-linux

RUN python -m pip install pipenv && \
    printf "export PIPENV_SHELL=bash\npipenv shell" >/home/codespace/.python/current/bin/pipenv-shell && \
    chmod +x /home/codespace/.python/current/bin/pipenv-shell

ENTRYPOINT bash
