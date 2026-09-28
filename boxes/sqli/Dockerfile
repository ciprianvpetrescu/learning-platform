FROM php:8.2-apache
RUN docker-php-ext-install pdo_mysql && mkdir -p /var/www
COPY src/ /var/www/html/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && chmod -R 777 /var/www/html
EXPOSE 80
CMD ["/entrypoint.sh"]
