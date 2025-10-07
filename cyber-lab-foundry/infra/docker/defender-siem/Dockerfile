FROM opensearchproject/opensearch:2.11.0

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        jq \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir requests

RUN curl -L "https://artifacts.opensearch.org/releases/bundle/opensearch-dashboards/2.11.0/opensearch-dashboards-2.11.0-linux-x64.tar.gz" \
    | tar zx -C /opt
RUN ln -s /opt/opensearch-dashboards-2.11.0 /opt/opensearch-dashboards

COPY entrypoint.sh /entrypoint.sh
COPY logshipper.py /logshipper.py
RUN chmod +x /entrypoint.sh

ENV DISABLE_SECURITY_PLUGIN=true \
    OPENSEARCH_INITIAL_ADMIN_PASSWORD=admin123

USER opensearch

ENTRYPOINT ["/entrypoint.sh"]
