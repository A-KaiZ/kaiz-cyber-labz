FROM debian:12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        tcpdump \
        tshark \
        iproute2 \
        bash \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /opt/capture

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/bash"]
