#!/bin/bash

set -e  # Exit on error

# Colors
GREEN="\e[32m"
BLUE="\e[34m"
YELLOW="\e[33m"
RESET="\e[0m"

log() {
    echo -e "${BLUE}[INFO]${RESET} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${RESET} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${RESET} $1"
}

create_dir() {
    if [ ! -d "$1" ]; then
        mkdir -p "$1"
        success "Created directory: $1"
    else
        warn "Directory already exists: $1"
    fi
}

create_file() {
    if [ ! -f "$1" ]; then
        touch "$1"
        success "Created file: $1"
    else
        warn "File already exists: $1"
    fi
}

log "Creating project structure..."

# Directories
create_dir "src"
create_dir "research"

# Files
create_file "src/__init__.py"
create_file "src/helper.py"
create_file "src/prompt.py"
create_file ".env"
create_file "setup.py"
create_file "app.py"
create_file "research/trials.ipynb"
create_file "requirements.txt"

success "Directory and files created successfully!"
