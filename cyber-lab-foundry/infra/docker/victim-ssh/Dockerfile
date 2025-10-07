FROM debian:12-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        openssh-server \
        fail2ban \
        python3 \
        python3-venv \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash victim \
    && echo "victim:WeakPass123!" | chpasswd

RUN mkdir -p /var/run/sshd /var/log/auth

COPY sshd_config.tpl /etc/ssh/sshd_config.tpl
COPY entrypoint.sh /entrypoint.sh
COPY fail2ban/jail.local /etc/fail2ban/jail.local
COPY fail2ban/filter.d/sshd.local /etc/fail2ban/filter.d/sshd.local
RUN chmod +x /entrypoint.sh

EXPOSE 22

ENTRYPOINT ["/entrypoint.sh"]
