# ============================================================
# StudioBook – Render.com Deployment Dockerfile
# Laravel 12 + React (Inertia.js) + SQLite
# ============================================================
FROM php:8.2-apache

# Enable Apache modules
RUN a2enmod rewrite headers

# Install PHP extensions required by Laravel
RUN apt-get update && apt-get install -y --no-install-recommends \
    libzip-dev \
    libsqlite3-dev \
    unzip \
    curl \
    && docker-php-ext-install pdo pdo_sqlite pdo_mysql zip bcmath \
    && rm -rf /var/lib/apt/lists/*

# Install Composer
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# Set Apache document root to Laravel's public directory
ENV APACHE_DOCUMENT_ROOT=/var/www/html/public
RUN sed -ri -e 's!/var/www/html!${APACHE_DOCUMENT_ROOT}!g' \
    /etc/apache2/sites-available/*.conf \
    /etc/apache2/apache2.conf

# Copy backend source (includes pre-built frontend assets in public/build/)
WORKDIR /var/www/html
COPY backend/ ./

# Install PHP dependencies (production only)
RUN composer install --no-dev --optimize-autoloader --no-interaction --no-progress

# Ensure storage & cache directories exist and are writable
RUN mkdir -p storage/framework/sessions \
    storage/framework/views \
    storage/framework/cache/data \
    storage/logs \
    bootstrap/cache \
    database \
    && chown -R www-data:www-data storage bootstrap/cache database \
    && chmod -R 775 storage bootstrap/cache database

# Copy startup script
COPY scripts/render-start.sh /usr/local/bin/render-start.sh
RUN chmod +x /usr/local/bin/render-start.sh

# Expose port (Render sets PORT env var)
EXPOSE 10000

# Start the application
CMD ["/usr/local/bin/render-start.sh"]
