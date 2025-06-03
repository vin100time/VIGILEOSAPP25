#!/bin/bash

# Script de déploiement pour VIGILEOSAPP25
# Usage: ./scripts/deploy.sh [environment] [action]
# Exemples:
#   ./scripts/deploy.sh production deploy
#   ./scripts/deploy.sh development start
#   ./scripts/deploy.sh production update

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ENVIRONMENT=${1:-production}
ACTION=${2:-deploy}

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonctions utilitaires
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérification des prérequis
check_prerequisites() {
    log_info "Vérification des prérequis..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker n'est pas installé"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose n'est pas installé"
        exit 1
    fi
    
    log_success "Prérequis vérifiés"
}

# Configuration de l'environnement
setup_environment() {
    log_info "Configuration de l'environnement: $ENVIRONMENT"
    
    cd "$PROJECT_DIR"
    
    # Copier le fichier d'environnement approprié
    if [ "$ENVIRONMENT" = "development" ]; then
        if [ ! -f .env ]; then
            cp .env.development .env
            log_info "Fichier .env créé à partir de .env.development"
        fi
    else
        if [ ! -f .env ]; then
            cp .env.example .env
            log_warning "Fichier .env créé à partir de .env.example"
            log_warning "ATTENTION: Modifiez le fichier .env avec vos vraies valeurs avant de continuer"
            read -p "Appuyez sur Entrée pour continuer..."
        fi
    fi
    
    # Créer les répertoires nécessaires
    mkdir -p docker/ssl
    mkdir -p logs
    
    # Générer des certificats SSL auto-signés pour le développement
    if [ "$ENVIRONMENT" = "development" ] && [ ! -f docker/ssl/cert.pem ]; then
        log_info "Génération de certificats SSL auto-signés pour le développement..."
        openssl req -x509 -newkey rsa:4096 -keyout docker/ssl/key.pem -out docker/ssl/cert.pem -days 365 -nodes -subj "/C=FR/ST=France/L=Paris/O=VIGILEOSAPP25/CN=localhost"
    fi
}

# Construction des images Docker
build_images() {
    log_info "Construction des images Docker..."
    
    if [ "$ENVIRONMENT" = "development" ]; then
        docker-compose -f docker-compose.yml --env-file .env.development build --no-cache
    else
        docker-compose -f docker-compose.yml --env-file .env build --no-cache
    fi
    
    log_success "Images construites avec succès"
}

# Démarrage des services
start_services() {
    log_info "Démarrage des services..."
    
    if [ "$ENVIRONMENT" = "development" ]; then
        docker-compose -f docker-compose.yml --env-file .env.development up -d
    else
        docker-compose -f docker-compose.yml --env-file .env up -d
    fi
    
    log_success "Services démarrés"
}

# Arrêt des services
stop_services() {
    log_info "Arrêt des services..."
    
    docker-compose -f docker-compose.yml down
    
    log_success "Services arrêtés"
}

# Mise à jour de l'application
update_application() {
    log_info "Mise à jour de l'application..."
    
    # Pull des nouvelles images
    if [ "$ENVIRONMENT" = "development" ]; then
        docker-compose -f docker-compose.yml --env-file .env.development pull
    else
        docker-compose -f docker-compose.yml --env-file .env pull
    fi
    
    # Reconstruction et redémarrage
    build_images
    
    # Redémarrage avec zero-downtime
    if [ "$ENVIRONMENT" = "development" ]; then
        docker-compose -f docker-compose.yml --env-file .env.development up -d --no-deps web
    else
        docker-compose -f docker-compose.yml --env-file .env up -d --no-deps web
    fi
    
    log_success "Application mise à jour"
}

# Sauvegarde de la base de données
backup_database() {
    log_info "Sauvegarde de la base de données..."
    
    BACKUP_DIR="$PROJECT_DIR/backups"
    mkdir -p "$BACKUP_DIR"
    
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/postgres_backup_$TIMESTAMP.sql.gz"
    
    docker exec vigileosapp-postgres pg_dump -U vigileosapp_user vigileosapp | gzip > "$BACKUP_FILE"
    
    log_success "Sauvegarde créée: $BACKUP_FILE"
}

# Monitoring de la santé
health_check() {
    log_info "Vérification de la santé des services..."
    
    # Vérifier PostgreSQL
    if docker exec vigileosapp-postgres pg_isready -U vigileosapp_user -d vigileosapp > /dev/null 2>&1; then
        log_success "PostgreSQL: OK"
    else
        log_error "PostgreSQL: KO"
    fi
    
    # Vérifier Redis
    if docker exec vigileosapp-redis redis-cli ping > /dev/null 2>&1; then
        log_success "Redis: OK"
    else
        log_error "Redis: KO"
    fi
    
    # Vérifier l'application web
    if curl -f http://localhost:8000/api/health/ > /dev/null 2>&1; then
        log_success "Application Web: OK"
    else
        log_error "Application Web: KO"
    fi
}

# Menu principal
main() {
    echo "🚀 VIGILEOSAPP25 - Script de déploiement"
    echo "Environnement: $ENVIRONMENT"
    echo "Action: $ACTION"
    echo "=================================="
    
    case $ACTION in
        "deploy")
            check_prerequisites
            setup_environment
            build_images
            start_services
            log_success "Déploiement terminé avec succès!"
            ;;
        "start")
            start_services
            ;;
        "stop")
            stop_services
            ;;
        "restart")
            stop_services
            start_services
            ;;
        "update")
            update_application
            ;;
        "build")
            build_images
            ;;
        "backup")
            backup_database
            ;;
        "health")
            health_check
            ;;
        *)
            echo "Actions disponibles:"
            echo "  deploy     - Déploiement complet"
            echo "  start      - Démarrer les services"
            echo "  stop       - Arrêter les services"
            echo "  restart    - Redémarrer les services"
            echo "  update     - Mettre à jour l'application"
            echo "  build      - Construire les images"
            echo "  backup     - Sauvegarder la base de données"
            echo "  health     - Vérifier la santé des services"
            exit 1
            ;;
    esac
}

# Exécution du script principal
main "$@"