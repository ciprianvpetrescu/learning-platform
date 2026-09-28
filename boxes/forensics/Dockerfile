FROM debian:12-slim
RUN apt-get update -qq && apt-get install -y -qq python3 zip unzip file xxd sleuthkit foremost libimage-exiftool-perl >/dev/null 2>&1 || true
COPY make_evidence.py /make_evidence.py
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
