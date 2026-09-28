FROM debian:12-slim
RUN apt-get update -qq && apt-get install -y -qq python3 python3-pip iproute2 iputils-ping dnsutils netcat-openbsd openssh-server curl >/dev/null 2>&1 && mkdir -p /var/run/sshd
RUN pip3 install --break-system-packages --no-cache-dir flask 2>/dev/null || true
COPY *.py /opt/lab/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
