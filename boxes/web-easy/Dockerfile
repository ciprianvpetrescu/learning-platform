FROM php:8.2-apache
RUN docker-php-ext-install pdo pdo_mysql 2>/dev/null || true
RUN a2enmod rewrite
COPY src/ /var/www/html/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 80
CMD ["/entrypoint.sh"]
