FROM debian:12-slim
RUN apt-get update -qq && apt-get install -y -qq openssh-server procps iproute2 curl >/dev/null 2>&1 && mkdir -p /var/run/sshd
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 22
CMD ["/entrypoint.sh"]
