FROM debian:12-slim
RUN apt-get update -qq && apt-get install -y -qq openssh-server sudo vim cron python3 passwd >/dev/null 2>&1
RUN mkdir -p /var/run/sshd
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 22 80
CMD ["/entrypoint.sh"]
