FROM php:8.2-apache
RUN mkdir -p /var/log/php-lab && touch /var/log/php-lab/access.log && chmod 666 /var/log/php-lab/access.log
COPY src/ /var/www/html/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && chmod -R 777 /var/www/html/uploads
EXPOSE 80
CMD ["/entrypoint.sh"]
