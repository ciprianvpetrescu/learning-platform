FROM debian:bookworm-slim
ENV DEBIAN_FRONTEND=noninteractive

# A deliberately dated host: a handful of services with historic weaknesses,
# all of which run natively on ARM. Teaches enumeration and known-exploit
# recognition without depending on amd64-only images.
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends \
      python3 python3-pip vsftpd openssh-server nginx netcat-openbsd \
      inetutils-telnetd telnetd procps iproute2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# --- an SSH service with a weak, guessable credential ---
RUN useradd -m -s /bin/bash analyst && \
    echo 'analyst:analyst123' | chpasswd && \
    mkdir -p /run/sshd

# --- anonymous FTP with a readable directory ---
RUN mkdir -p /srv/ftp/pub && \
    printf 'Internal file share. Reports archived here.\n' > /srv/ftp/pub/README.txt && \
    printf 'DB_PASSWORD=B4ckup2019!\nDB_USER=svc_backup\n' > /srv/ftp/pub/db_backup.ini && \
    chmod -R 755 /srv/ftp

# --- a web app with a debug endpoint that leaks environment ---
COPY webapp /var/www/html
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN useradd -m -s /bin/bash webdev && \
    printf 'LEGACY_HOST_NOTE=Rename this account before production\n' > /home/webdev/notes.txt && \
    chown webdev:webdev /home/webdev/notes.txt

EXPOSE 21 22 23 80
CMD ["/entrypoint.sh"]
