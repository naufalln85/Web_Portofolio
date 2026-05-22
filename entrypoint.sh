#!/bin/bash
set -e

echo "🔄 Menunggu database PostgreSQL siap..."
while ! python -c "
import os, psycopg2
conn = psycopg2.connect(
    dbname=os.environ.get('DB_NAME','portfolio_db'),
    user=os.environ.get('DB_USER','portfolio_user'),
    password=os.environ.get('DB_PASSWORD',''),
    host=os.environ.get('DB_HOST','db'),
    port=os.environ.get('DB_PORT','5432')
)
conn.close()
" 2>/dev/null; do
    echo "  ⏳ Database belum siap, menunggu 2 detik..."
    sleep 2
done
echo "✅ Database siap!"

echo "📦 Menjalankan makemigrations..."
python manage.py makemigrations portfolio --noinput

echo "📦 Menjalankan migrate..."
python manage.py migrate --noinput

echo "📂 Mengumpulkan static files..."
python manage.py collectstatic --noinput

echo "🌱 Menjalankan seed data portfolio..."
python manage.py seed_portfolio

echo "🚀 Memulai Gunicorn server..."
exec gunicorn portfolio_project.wsgi:application --bind 0.0.0.0:8000 --workers 2
