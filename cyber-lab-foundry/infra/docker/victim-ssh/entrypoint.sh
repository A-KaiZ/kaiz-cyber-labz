#!/bin/bash
set -Eeuo pipefail

MAX_AUTH_TRIES=${MAX_AUTH_TRIES:-6}
LOGIN_GRACE_TIME=${LOGIN_GRACE_TIME:-120}
ENABLE_FAIL2BAN=${ENABLE_FAIL2BAN:-false}

sed -e "s/{{MAX_AUTH_TRIES}}/${MAX_AUTH_TRIES}/" \
    -e "s/{{LOGIN_GRACE_TIME}}/${LOGIN_GRACE_TIME}/" \
    /etc/ssh/sshd_config.tpl > /etc/ssh/sshd_config

echo "victim ALL=(ALL) ALL" >> /etc/sudoers

if [[ "${ENABLE_FAIL2BAN}" == "true" ]]; then
    service fail2ban start
else
    rm -f /var/run/fail2ban/fail2ban.sock || true
fi

/usr/sbin/sshd -D -e
