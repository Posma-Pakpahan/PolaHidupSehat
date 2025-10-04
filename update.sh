#!/bin/bash

# Update deployment script for Pola Hidup Tracker
# Run this when you want to update the application

set -e

PROJECT_DIR="/var/www/pola_hidup_tracker"

echo "🔄 Updating Pola Hidup Tracker..."

cd $PROJECT_DIR

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "📦 Updating dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🔄 Running migrations..."
python manage.py migrate --settings=pola_hidup_tracker.production_settings

# Collect static files
echo "📄 Collecting static files..."
python manage.py collectstatic --noinput --settings=pola_hidup_tracker.production_settings

# Restart services
echo "🚀 Restarting services..."
sudo systemctl restart pola-hidup-tracker
sudo systemctl restart nginx

echo "✅ Update completed successfully!"
echo "🎉 Your application is now running the latest version"