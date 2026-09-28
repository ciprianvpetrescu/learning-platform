FROM python:3.12-slim
RUN pip install --no-cache-dir flask requests && mkdir -p /var/www
COPY src/ /app/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 80 8080
CMD ["/entrypoint.sh"]
