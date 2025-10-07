FROM python:3.11-slim

ARG DEVCONTAINER="false"

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
        bash \
        curl \
        git \
        jq \
        nano \
        netcat-openbsd \
        nmap \
        openssh-client \
        unzip \
        wordlists \
        hydra \
        sqlmap \
        sudo \
        tcpdump \
    && rm -rf /var/lib/apt/lists/*

# Install feroxbuster
RUN curl -L "https://github.com/epi052/feroxbuster/releases/download/v2.10.4/feroxbuster_amd64" -o /usr/local/bin/feroxbuster \
    && chmod +x /usr/local/bin/feroxbuster

RUN useradd -ms /bin/bash student && echo "student ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

COPY entrypoint.sh /entrypoint.sh
COPY motd.txt /etc/motd
RUN chmod +x /entrypoint.sh && chown student:student /entrypoint.sh

USER student
WORKDIR /home/student

ENV PATH="/home/student/.local/bin:$PATH"

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/bin/bash"]
