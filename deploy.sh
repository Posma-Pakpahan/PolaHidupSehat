#!/bin/bash

# Deployment script for Pola Hidup Tracker
# Run this script on your VPS

set -e

PROJECT_NAME="pola_hidup_tracker"
PROJECT_DIR="/var/www/$PROJECT_NAME"
REPO_URL="https://github.com/posma-pakpahan/pola-hidup-tracker.git"  # Update with your repo
PYTHON_VERSION="3.11"
DB_NAME="pola_hidup_tracker"
DB_USER="tracker_user"

echo "🚀 Starting deployment of Pola Hidup Tracker..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "📦 Installing required packages..."
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib redis-server git curl

# Install Python 3.11 if not available
if ! command -v python3.11 &> /dev/null; then
    echo "📦 Installing Python 3.11..."
    sudo apt install -y software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt update
    sudo apt install -y python3.11 python3.11-venv python3.11-dev
fi

# Create project directory
echo "📁 Creating project directory..."
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

# Clone or update repository
if [ -d "$PROJECT_DIR/.git" ]; then
    echo "🔄 Updating existing repository..."
    cd $PROJECT_DIR
    git pull origin main
else
    echo "📥 Cloning repository..."
    git clone $REPO_URL $PROJECT_DIR
    cd $PROJECT_DIR
fi

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup PostgreSQL database
echo "🗄️ Setting up PostgreSQL database..."
sudo -u postgres psql << EOF
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH ENCRYPTED PASSWORD 'secure_password_123';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
ALTER USER $DB_USER CREATEDB;
\q
EOF

# Create environment file
echo "⚙️ Creating environment configuration..."
cat > .env << EOF
DEBUG=False
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=secure_password_123
DB_HOST=localhost
DB_PORT=5432
USE_HTTPS=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@posma-pakpahan.me
REDIS_URL=redis://127.0.0.1:6379/1
EOF

# Create logs directory
mkdir -p logs

# Run Django migrations
echo "🔄 Running Django migrations..."
python manage.py migrate --settings=pola_hidup_tracker.production_settings

# Create superuser (if not exists)
echo "👤 Creating superuser..."
python manage.py shell --settings=pola_hidup_tracker.production_settings << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@posma-pakpahan.me', 'AdminPassword123!')
    print("Superuser created: admin / AdminPassword123!")
else:
    print("Superuser already exists")
EOF

# Apply healthy lifestyle template for admin
echo "🎯 Applying healthy lifestyle template..."
python manage.py apply_healthy_template --user admin --current-week-only --settings=pola_hidup_tracker.production_settings

# Collect static files
echo "📄 Collecting static files..."
python manage.py collectstatic --noinput --settings=pola_hidup_tracker.production_settings

# Create Gunicorn systemd service
echo "⚙️ Setting up Gunicorn service..."
sudo tee /etc/systemd/system/pola-hidup-tracker.service > /dev/null << EOF
[Unit]
Description=Pola Hidup Tracker Django application
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --workers 3 --bind unix:$PROJECT_DIR/pola_hidup_tracker.sock pola_hidup_tracker.wsgi:application --settings=pola_hidup_tracker.production_settings
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Create Nginx configuration
echo "🌐 Setting up Nginx configuration..."
sudo tee /etc/nginx/sites-available/pola-hidup-tracker > /dev/null << EOF
server {
    listen 80;
    server_name tracker.posma-pakpahan.me 31.97.221.115;

    client_max_body_size 20M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
    
    location /media/ {
        alias $PROJECT_DIR/mediafiles/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$PROJECT_DIR/pola_hidup_tracker.sock;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/pola-hidup-tracker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Start and enable services
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl start pola-hidup-tracker
sudo systemctl enable pola-hidup-tracker
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Setup SSL with Let's Encrypt (optional)
read -p "🔒 Do you want to setup SSL with Let's Encrypt? (y/n): " setup_ssl
if [ "$setup_ssl" = "y" ]; then
    echo "🔒 Setting up SSL..."
    sudo apt install -y certbot python3-certbot-nginx
    sudo certbot --nginx -d tracker.posma-pakpahan.me
fi

echo "✅ Deployment completed successfully!"
echo ""
echo "🎉 Your Pola Hidup Tracker is now running at:"
echo "   http://tracker.posma-pakpahan.me"
echo "   http://31.97.221.115"
echo ""
echo "👤 Admin credentials:"
echo "   Username: admin"
echo "   Password: AdminPassword123!"
echo ""
echo "🔧 Useful commands:"
echo "   sudo systemctl status pola-hidup-tracker"
echo "   sudo systemctl restart pola-hidup-tracker"
echo "   sudo tail -f $PROJECT_DIR/logs/django.log"
echo "   sudo journalctl -u pola-hidup-tracker -f"