FROM debian:12-slim
RUN apt-get update -qq && apt-get install -y -qq python3 python3-flask curl >/dev/null 2>&1
COPY ldap_sim.py /ldap_sim.py
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
