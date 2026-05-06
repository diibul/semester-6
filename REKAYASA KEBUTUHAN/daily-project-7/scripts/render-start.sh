#!/bin/bash
set -e

echo "=== StudioBook Render Startup ==="

# Use Render's PORT or default to 10000
PORT="${PORT:-10000}"

# ---------- 1. Environment setup ----------
# Generate APP_KEY if not set (Render generateValue produces a random string, not base64)
if [ -z "$APP_KEY" ] || [ "$APP_KEY" = "true" ]; then
    echo "Generating APP_KEY..."
    php artisan key:generate --force
else
    # Ensure APP_KEY has the correct format
    if [[ ! "$APP_KEY" == base64:* ]]; then
        export APP_KEY="base64:$(echo -n "$APP_KEY" | head -c 32 | base64)"
    fi
fi

# ---------- 2. Database setup ----------
DB_PATH="/var/www/html/database/database.sqlite"
if [ ! -f "$DB_PATH" ]; then
    echo "Creating SQLite database..."
    touch "$DB_PATH"
    chown www-data:www-data "$DB_PATH"
fi

echo "Running migrations..."
php artisan migrate --force --no-interaction

# Seed only if users table is empty (first deploy)
USER_COUNT=$(php artisan tinker --execute="echo App\Models\User::count();" 2>/dev/null || echo "0")
if [ "$USER_COUNT" = "0" ]; then
    echo "Seeding demo data..."
    php artisan db:seed --force --no-interaction
fi

# ---------- 3. Laravel optimization ----------
echo "Caching configuration..."
php artisan config:cache
php artisan route:cache
php artisan view:cache

# ---------- 4. Fix permissions ----------
chown -R www-data:www-data storage bootstrap/cache database

# ---------- 5. Configure Apache port ----------
# Render requires listening on $PORT
sed -i "s/Listen 80/Listen $PORT/" /etc/apache2/ports.conf
sed -i "s/:80/:$PORT/" /etc/apache2/sites-available/000-default.conf

echo "=== Starting Apache on port $PORT ==="
exec apache2-foreground
