#!/bin/bash

# Script d'initialisation pour VIGILEOSAPP25
# Ce script configure l'environnement de développement complet

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
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

log_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

# Banner
show_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                            VIGILEOSAPP25                                     ║"
    echo "║                    Script d'initialisation du projet                        ║"
    echo "║                                                                              ║"
    echo "║  Ce script va configurer votre environnement de développement complet       ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Vérification des prérequis
check_prerequisites() {
    log_step "Vérification des prérequis..."
    
    local missing_tools=()
    
    # Vérifier Docker
    if ! command -v docker &> /dev/null; then
        missing_tools+=("Docker")
    fi
    
    # Vérifier Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        missing_tools+=("Docker Compose")
    fi
    
    # Vérifier Git
    if ! command -v git &> /dev/null; then
        missing_tools+=("Git")
    fi
    
    # Vérifier Make
    if ! command -v make &> /dev/null; then
        missing_tools+=("Make")
    fi
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        log_error "Outils manquants: ${missing_tools[*]}"
        log_info "Veuillez installer les outils manquants avant de continuer."
        exit 1
    fi
    
    log_success "Tous les prérequis sont installés"
}

# Configuration de l'environnement
setup_environment() {
    log_step "Configuration de l'environnement..."
    
    cd "$PROJECT_DIR"
    
    # Créer les répertoires nécessaires
    log_info "Création des répertoires..."
    mkdir -p docker/ssl
    mkdir -p logs
    mkdir -p backups
    mkdir -p media
    mkdir -p static
    
    # Copier le fichier d'environnement
    if [ ! -f .env ]; then
        log_info "Configuration du fichier d'environnement..."
        cp .env.development .env
        log_success "Fichier .env créé pour le développement"
    else
        log_warning "Fichier .env déjà présent"
    fi
    
    # Générer une clé secrète Django
    log_info "Génération d'une clé secrète Django..."
    SECRET_KEY=$(python3 -c "
import secrets
import string
alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
secret_key = ''.join(secrets.choice(alphabet) for i in range(50))
print(secret_key)
")
    
    # Remplacer la clé secrète dans le fichier .env
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    else
        # Linux
        sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    fi
    
    log_success "Clé secrète générée et configurée"
}

# Génération des certificats SSL pour le développement
generate_ssl_certificates() {
    log_step "Génération des certificats SSL pour le développement..."
    
    if [ ! -f docker/ssl/cert.pem ]; then
        log_info "Génération des certificats SSL auto-signés..."
        
        # Créer un fichier de configuration OpenSSL
        cat > docker/ssl/openssl.conf << EOF
[req]
distinguished_name = req_distinguished_name
x509_extensions = v3_req
prompt = no

[req_distinguished_name]
C = FR
ST = France
L = Paris
O = VIGILEOSAPP25
OU = Development
CN = localhost

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = 127.0.0.1
DNS.3 = 0.0.0.0
IP.1 = 127.0.0.1
IP.2 = 0.0.0.0
EOF
        
        # Générer la clé privée et le certificat
        openssl req -x509 -newkey rsa:4096 -keyout docker/ssl/key.pem -out docker/ssl/cert.pem \
            -days 365 -nodes -config docker/ssl/openssl.conf
        
        # Nettoyer le fichier de configuration temporaire
        rm docker/ssl/openssl.conf
        
        log_success "Certificats SSL générés"
    else
        log_info "Certificats SSL déjà présents"
    fi
}

# Configuration Git
setup_git() {
    log_step "Configuration Git..."
    
    # Vérifier si on est dans un dépôt Git
    if [ ! -d .git ]; then
        log_info "Initialisation du dépôt Git..."
        git init
        
        # Ajouter le remote origin si fourni
        read -p "URL du dépôt distant (optionnel): " REMOTE_URL
        if [ ! -z "$REMOTE_URL" ]; then
            git remote add origin "$REMOTE_URL"
            log_success "Remote origin ajouté: $REMOTE_URL"
        fi
    fi
    
    # Configuration utilisateur Git si pas déjà configuré
    if [ -z "$(git config user.name)" ]; then
        read -p "Nom d'utilisateur Git: " GIT_NAME
        git config user.name "$GIT_NAME"
    fi
    
    if [ -z "$(git config user.email)" ]; then
        read -p "Email Git: " GIT_EMAIL
        git config user.email "$GIT_EMAIL"
    fi
    
    log_success "Configuration Git terminée"
}

# Installation des hooks pre-commit
setup_precommit() {
    log_step "Configuration des hooks pre-commit..."
    
    # Créer le fichier de configuration pre-commit
    cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: debug-statements

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3
        files: ^backend/

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        files: ^backend/
        args: [--max-line-length=88, --extend-ignore=E203,W503]

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        files: ^backend/
        args: [--profile=black]
EOF
    
    log_success "Configuration pre-commit créée"
}

# Construction des images Docker
build_docker_images() {
    log_step "Construction des images Docker..."
    
    log_info "Construction de l'image backend..."
    docker-compose -f docker-compose.dev.yml build --no-cache web-dev
    
    log_info "Construction de l'image frontend..."
    docker-compose -f docker-compose.dev.yml build --no-cache frontend-dev
    
    log_success "Images Docker construites"
}

# Démarrage des services
start_services() {
    log_step "Démarrage des services..."
    
    log_info "Démarrage de PostgreSQL et Redis..."
    docker-compose -f docker-compose.dev.yml up -d postgres-dev redis-dev
    
    # Attendre que les services soient prêts
    log_info "Attente de la disponibilité des services..."
    sleep 10
    
    log_info "Démarrage de l'application web..."
    docker-compose -f docker-compose.dev.yml up -d web-dev
    
    log_info "Démarrage de Celery..."
    docker-compose -f docker-compose.dev.yml up -d celery-dev
    
    log_info "Démarrage du frontend..."
    docker-compose -f docker-compose.dev.yml up -d frontend-dev
    
    log_info "Démarrage de MailHog..."
    docker-compose -f docker-compose.dev.yml up -d mailhog
    
    log_success "Tous les services sont démarrés"
}

# Initialisation de la base de données
init_database() {
    log_step "Initialisation de la base de données..."
    
    log_info "Exécution des migrations..."
    docker-compose -f docker-compose.dev.yml exec -T web-dev python manage.py migrate
    
    log_info "Collecte des fichiers statiques..."
    docker-compose -f docker-compose.dev.yml exec -T web-dev python manage.py collectstatic --noinput
    
    log_info "Création du superutilisateur..."
    docker-compose -f docker-compose.dev.yml exec -T web-dev python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@localhost', 'admin123')
    print('Superutilisateur créé: admin/admin123')
else:
    print('Superutilisateur déjà existant')
EOF
    
    log_success "Base de données initialisée"
}

# Affichage des informations finales
show_final_info() {
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                        INITIALISATION TERMINÉE !                            ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo -e "${BLUE}🚀 Votre environnement de développement est prêt !${NC}"
    echo ""
    echo -e "${YELLOW}📍 URLs d'accès:${NC}"
    echo "  • Frontend React:     http://localhost:3000"
    echo "  • Backend Django:     http://localhost:8000"
    echo "  • Admin Django:       http://localhost:8000/admin"
    echo "  • API Documentation:  http://localhost:8000/api/docs"
    echo "  • MailHog (emails):   http://localhost:8025"
    echo ""
    echo -e "${YELLOW}🔑 Connexion admin:${NC}"
    echo "  • Utilisateur: admin"
    echo "  • Mot de passe: admin123"
    echo ""
    echo -e "${YELLOW}🛠️ Commandes utiles:${NC}"
    echo "  • make dev-logs       # Voir les logs"
    echo "  • make dev-shell      # Accéder au shell Django"
    echo "  • make dev-test       # Exécuter les tests"
    echo "  • make dev-stop       # Arrêter les services"
    echo "  • make help           # Voir toutes les commandes"
    echo ""
    echo -e "${GREEN}✨ Bon développement !${NC}"
}

# Fonction principale
main() {
    show_banner
    
    echo -e "${YELLOW}Ce script va:${NC}"
    echo "  1. Vérifier les prérequis"
    echo "  2. Configurer l'environnement"
    echo "  3. Générer les certificats SSL"
    echo "  4. Configurer Git"
    echo "  5. Installer les hooks pre-commit"
    echo "  6. Construire les images Docker"
    echo "  7. Démarrer les services"
    echo "  8. Initialiser la base de données"
    echo ""
    
    read -p "Continuer ? (y/N): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Initialisation annulée"
        exit 0
    fi
    
    check_prerequisites
    setup_environment
    generate_ssl_certificates
    setup_git
    setup_precommit
    build_docker_images
    start_services
    init_database
    show_final_info
}

# Exécution du script principal
main "$@"