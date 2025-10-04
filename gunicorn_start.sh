#!/bin/bash

NAME="pola_hidup_tracker"
DJANGODIR="/var/www/pola_hidup_tracker"
SOCKFILE="$DJANGODIR/pola_hidup_tracker.sock"
USER="www-data"
GROUP="www-data"
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE="pola_hidup_tracker.production_settings"
DJANGO_WSGI_MODULE="pola_hidup_tracker.wsgi"

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=info \
  --log-file=-