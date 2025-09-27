#!/bin/bash

# Define project root
PROJECT_ROOT="event_management"

# Create main directories
mkdir -p $PROJECT_ROOT/static/css
mkdir -p $PROJECT_ROOT/static/js
mkdir -p $PROJECT_ROOT/templates

# Create top-level files
touch $PROJECT_ROOT/app.py
touch $PROJECT_ROOT/models.py
touch $PROJECT_ROOT/forms.py
touch $PROJECT_ROOT/requirements.txt

# Create static files
touch $PROJECT_ROOT/static/css/style.css
touch $PROJECT_ROOT/static/js/script.js

# Create template files
touch $PROJECT_ROOT/templates/base.html
touch $PROJECT_ROOT/templates/index.html
touch $PROJECT_ROOT/templates/events.html
touch $PROJECT_ROOT/templates/create_event.html
touch $PROJECT_ROOT/templates/event_detail.html
touch $PROJECT_ROOT/templates/register.html

echo "✅ Web application structure created under '$PROJECT_ROOT/'"
