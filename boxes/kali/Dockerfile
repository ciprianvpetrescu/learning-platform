FROM kalilinux/kali-rolling:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends \
    curl wget nmap netcat-traditional dnsutils iputils-ping iproute2 \
    python3 python3-pip gobuster sqlmap hydra john wordlists dirb \
    vim less procps net-tools tmux \
    openssh-client sshpass ftp telnet smbclient tcpdump whois \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /usr/share/doc/* /usr/share/man/*

# ttyd: browser terminal, so users get a real shell without installing anything
ARG TTYD_VER=1.7.7
RUN curl -sSL -o /usr/local/bin/ttyd \
      https://github.com/tsl0922/ttyd/releases/download/${TTYD_VER}/ttyd.aarch64 \
    && chmod +x /usr/local/bin/ttyd

RUN mkdir -p /usr/share/wordlists/dirb && \
    (gunzip -c /usr/share/wordlists/rockyou.txt.gz > /usr/share/wordlists/rockyou.txt 2>/dev/null || true) && \
    (test -f /usr/share/wordlists/dirb/common.txt || \
     cp /usr/share/dirb/wordlists/common.txt /usr/share/wordlists/dirb/common.txt 2>/dev/null || true)

# ttyd wrapper: theme and font live here, so the spawner never passes quoted
# JSON on the command line (bash used to echo it into the terminal on start).
COPY learn-ttyd /usr/local/bin/learn-ttyd
RUN chmod +x /usr/local/bin/learn-ttyd

# a live target IP is written here on spawn so the shell can show it
RUN mkdir -p /work && printf 'Attack workstation ready.\n\n  nmap -sV <target>\n  gobuster dir -u http://<target>/ -w /usr/share/wordlists/dirb/common.txt\n  sqlmap -u "http://<target>/page?id=1" --batch\n  hydra -l user -P /usr/share/wordlists/rockyou.txt ssh://<target>\n' > /work/README.txt
WORKDIR /work
EXPOSE 7681
CMD ["sleep", "infinity"]
