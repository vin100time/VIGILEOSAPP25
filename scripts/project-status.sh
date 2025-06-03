#!/bin/bash

# Script de rapport d'état du projet VIGILEOSAPP25
# Génère un rapport complet de l'état du projet

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
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Fonctions utilitaires
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_section() {
    echo -e "${PURPLE}[SECTION]${NC} $1"
    echo "----------------------------------------"
}

# Banner
show_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                         VIGILEOSAPP25 - RAPPORT D'ÉTAT                      ║"
    echo "║                                                                              ║"
    echo "║  Rapport complet de l'état du projet et de l'infrastructure                 ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo "Généré le: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
}

# Vérification de l'environnement
check_environment() {
    log_section "ENVIRONNEMENT"
    
    # Système d'exploitation
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS_INFO=$(lsb_release -d 2>/dev/null | cut -f2 || echo "Linux")
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS_INFO="macOS $(sw_vers -productVersion)"
    else
        OS_INFO="$OSTYPE"
    fi
    echo "Système d'exploitation: $OS_INFO"
    
    # Docker
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
        log_success "Docker: $DOCKER_VERSION"
    else
        log_error "Docker: Non installé"
    fi
    
    # Docker Compose
    if command -v docker-compose &> /dev/null; then
        COMPOSE_VERSION=$(docker-compose --version | cut -d' ' -f3 | cut -d',' -f1)
        log_success "Docker Compose: $COMPOSE_VERSION"
    else
        log_error "Docker Compose: Non installé"
    fi
    
    # Git
    if command -v git &> /dev/null; then
        GIT_VERSION=$(git --version | cut -d' ' -f3)
        log_success "Git: $GIT_VERSION"
    else
        log_error "Git: Non installé"
    fi
    
    # Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        log_success "Node.js: $NODE_VERSION"
    else
        log_warning "Node.js: Non installé"
    fi
    
    # Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        log_success "Python: $PYTHON_VERSION"
    else
        log_error "Python: Non installé"
    fi
    
    echo ""
}

# État des fichiers de configuration
check_configuration() {
    log_section "CONFIGURATION"
    
    cd "$PROJECT_DIR"
    
    # Fichiers d'environnement
    if [ -f .env ]; then
        log_success "Fichier .env présent"
    else
        log_warning "Fichier .env manquant"
    fi
    
    if [ -f .env.example ]; then
        log_success "Fichier .env.example présent"
    else
        log_warning "Fichier .env.example manquant"
    fi
    
    if [ -f .env.development ]; then
        log_success "Fichier .env.development présent"
    else
        log_warning "Fichier .env.development manquant"
    fi
    
    # Docker Compose
    if [ -f docker-compose.yml ]; then
        log_success "docker-compose.yml présent"
    else
        log_error "docker-compose.yml manquant"
    fi
    
    if [ -f docker-compose.dev.yml ]; then
        log_success "docker-compose.dev.yml présent"
    else
        log_warning "docker-compose.dev.yml manquant"
    fi
    
    # Makefile
    if [ -f Makefile ]; then
        log_success "Makefile présent"
    else
        log_warning "Makefile manquant"
    fi
    
    # Certificats SSL
    if [ -f docker/ssl/cert.pem ] && [ -f docker/ssl/key.pem ]; then
        log_success "Certificats SSL présents"
    else
        log_warning "Certificats SSL manquants"
    fi
    
    echo ""
}

# État des services Docker
check_docker_services() {
    log_section "SERVICES DOCKER"
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker non disponible"
        echo ""
        return
    fi
    
    # Services de production
    echo "Services de production:"
    if docker-compose -f docker-compose.yml ps 2>/dev/null | grep -q "Up"; then
        docker-compose -f docker-compose.yml ps --format "table {{.Name}}\t{{.State}}\t{{.Ports}}" 2>/dev/null || echo "Aucun service en cours d'exécution"
    else
        echo "Aucun service de production en cours d'exécution"
    fi
    
    echo ""
    
    # Services de développement
    echo "Services de développement:"
    if docker-compose -f docker-compose.dev.yml ps 2>/dev/null | grep -q "Up"; then
        docker-compose -f docker-compose.dev.yml ps --format "table {{.Name}}\t{{.State}}\t{{.Ports}}" 2>/dev/null || echo "Aucun service en cours d'exécution"
    else
        echo "Aucun service de développement en cours d'exécution"
    fi
    
    echo ""
}

# État du dépôt Git
check_git_status() {
    log_section "DÉPÔT GIT"
    
    cd "$PROJECT_DIR"
    
    if [ ! -d .git ]; then
        log_warning "Pas un dépôt Git"
        echo ""
        return
    fi
    
    # Branche actuelle
    CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "Inconnue")
    echo "Branche actuelle: $CURRENT_BRANCH"
    
    # Statut des fichiers
    if git diff-index --quiet HEAD -- 2>/dev/null; then
        log_success "Aucune modification non commitée"
    else
        log_warning "Modifications non commitées détectées"
        echo "Fichiers modifiés:"
        git status --porcelain | head -10
        if [ $(git status --porcelain | wc -l) -gt 10 ]; then
            echo "... et $(( $(git status --porcelain | wc -l) - 10 )) autres fichiers"
        fi
    fi
    
    # Commits en avance/retard
    if git remote get-url origin &>/dev/null; then
        REMOTE_URL=$(git remote get-url origin)
        echo "Remote origin: $REMOTE_URL"
        
        if git fetch origin &>/dev/null; then
            AHEAD=$(git rev-list --count HEAD ^origin/$CURRENT_BRANCH 2>/dev/null || echo "0")
            BEHIND=$(git rev-list --count origin/$CURRENT_BRANCH ^HEAD 2>/dev/null || echo "0")
            
            if [ "$AHEAD" -gt 0 ]; then
                log_warning "$AHEAD commit(s) en avance"
            fi
            
            if [ "$BEHIND" -gt 0 ]; then
                log_warning "$BEHIND commit(s) en retard"
            fi
            
            if [ "$AHEAD" -eq 0 ] && [ "$BEHIND" -eq 0 ]; then
                log_success "À jour avec origin/$CURRENT_BRANCH"
            fi
        else
            log_warning "Impossible de récupérer les informations du remote"
        fi
    else
        log_warning "Aucun remote configuré"
    fi
    
    # Dernier commit
    LAST_COMMIT=$(git log -1 --format="%h - %s (%cr)" 2>/dev/null || echo "Aucun commit")
    echo "Dernier commit: $LAST_COMMIT"
    
    echo ""
}

# Structure du projet
check_project_structure() {
    log_section "STRUCTURE DU PROJET"
    
    cd "$PROJECT_DIR"
    
    # Répertoires principaux
    local dirs=("backend" "frontend" "docker" "scripts")
    for dir in "${dirs[@]}"; do
        if [ -d "$dir" ]; then
            log_success "Répertoire $dir/ présent"
        else
            log_error "Répertoire $dir/ manquant"
        fi
    done
    
    # Fichiers importants
    local files=("README.md" "API_DOCUMENTATION.md" ".gitignore" "Makefile")
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            log_success "Fichier $file présent"
        else
            log_warning "Fichier $file manquant"
        fi
    done
    
    # Statistiques du code
    echo ""
    echo "Statistiques du code:"
    
    if [ -d backend ]; then
        PYTHON_FILES=$(find backend -name "*.py" | wc -l)
        PYTHON_LINES=$(find backend -name "*.py" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}' || echo "0")
        echo "  Backend Python: $PYTHON_FILES fichiers, $PYTHON_LINES lignes"
    fi
    
    if [ -d frontend ]; then
        JS_FILES=$(find frontend -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" | wc -l)
        if [ "$JS_FILES" -gt 0 ]; then
            JS_LINES=$(find frontend -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}' || echo "0")
            echo "  Frontend JS/TS: $JS_FILES fichiers, $JS_LINES lignes"
        fi
    fi
    
    echo ""
}

# Santé des services
check_services_health() {
    log_section "SANTÉ DES SERVICES"
    
    # Vérifier si les services sont en cours d'exécution
    if docker-compose -f docker-compose.yml ps 2>/dev/null | grep -q "Up" || docker-compose -f docker-compose.dev.yml ps 2>/dev/null | grep -q "Up"; then
        
        # Test de l'API de santé
        if curl -s -f http://localhost:8000/api/health/ >/dev/null 2>&1; then
            log_success "API de santé accessible"
            
            # Récupérer les détails de santé
            HEALTH_DATA=$(curl -s http://localhost:8000/api/health/ 2>/dev/null)
            if [ $? -eq 0 ]; then
                echo "Détails de santé:"
                echo "$HEALTH_DATA" | python3 -m json.tool 2>/dev/null || echo "$HEALTH_DATA"
            fi
        else
            log_error "API de santé non accessible"
        fi
        
        # Test de l'interface web
        if curl -s -f http://localhost:3000/ >/dev/null 2>&1; then
            log_success "Interface web accessible"
        else
            log_warning "Interface web non accessible"
        fi
        
        # Test de l'admin Django
        if curl -s -f http://localhost:8000/admin/ >/dev/null 2>&1; then
            log_success "Interface admin accessible"
        else
            log_warning "Interface admin non accessible"
        fi
        
    else
        log_warning "Aucun service en cours d'exécution"
    fi
    
    echo ""
}

# Utilisation des ressources
check_resource_usage() {
    log_section "UTILISATION DES RESSOURCES"
    
    # Espace disque
    echo "Espace disque:"
    df -h . | tail -1 | awk '{print "  Utilisé: " $3 " / " $2 " (" $5 ")"}'
    
    # Volumes Docker
    if command -v docker &> /dev/null; then
        echo ""
        echo "Volumes Docker:"
        docker volume ls --format "table {{.Name}}\t{{.Driver}}" 2>/dev/null | grep vigileosapp || echo "  Aucun volume VIGILEOSAPP trouvé"
        
        echo ""
        echo "Images Docker:"
        docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" 2>/dev/null | grep vigileosapp || echo "  Aucune image VIGILEOSAPP trouvée"
    fi
    
    echo ""
}

# Recommandations
show_recommendations() {
    log_section "RECOMMANDATIONS"
    
    cd "$PROJECT_DIR"
    
    local recommendations=()
    
    # Vérifications de sécurité
    if [ -f .env ] && grep -q "django-insecure" .env 2>/dev/null; then
        recommendations+=("🔒 Changez la clé secrète Django en production")
    fi
    
    if [ -f .env ] && grep -q "admin123" .env 2>/dev/null; then
        recommendations+=("🔒 Changez le mot de passe admin par défaut")
    fi
    
    # Vérifications de configuration
    if [ ! -f docker/ssl/cert.pem ]; then
        recommendations+=("🔐 Générez des certificats SSL pour HTTPS")
    fi
    
    if [ ! -f .gitignore ]; then
        recommendations+=("📝 Ajoutez un fichier .gitignore")
    fi
    
    # Vérifications de développement
    if [ ! -f backend/pytest.ini ]; then
        recommendations+=("🧪 Configurez pytest pour les tests")
    fi
    
    if [ ! -f .pre-commit-config.yaml ]; then
        recommendations+=("🔧 Configurez pre-commit pour la qualité du code")
    fi
    
    # Vérifications de déploiement
    if ! docker-compose -f docker-compose.yml ps 2>/dev/null | grep -q "Up"; then
        recommendations+=("🚀 Testez le déploiement en production")
    fi
    
    # Affichage des recommandations
    if [ ${#recommendations[@]} -eq 0 ]; then
        log_success "Aucune recommandation - Le projet est bien configuré !"
    else
        echo "Recommandations pour améliorer le projet:"
        for rec in "${recommendations[@]}"; do
            echo "  $rec"
        done
    fi
    
    echo ""
}

# Commandes utiles
show_useful_commands() {
    log_section "COMMANDES UTILES"
    
    echo "Développement:"
    echo "  make dev-start          # Démarrer l'environnement de développement"
    echo "  make dev-logs           # Voir les logs en temps réel"
    echo "  make dev-shell          # Accéder au shell Django"
    echo "  make dev-test           # Exécuter les tests"
    echo ""
    echo "Production:"
    echo "  make prod-deploy        # Déployer en production"
    echo "  make prod-logs          # Voir les logs de production"
    echo "  make backup             # Sauvegarder la base de données"
    echo ""
    echo "Maintenance:"
    echo "  make health             # Vérifier la santé des services"
    echo "  make clean              # Nettoyer les ressources Docker"
    echo "  ./scripts/deploy.sh     # Script de déploiement avancé"
    echo ""
}

# Fonction principale
main() {
    show_banner
    check_environment
    check_configuration
    check_docker_services
    check_git_status
    check_project_structure
    check_services_health
    check_resource_usage
    show_recommendations
    show_useful_commands
    
    echo -e "${GREEN}Rapport d'état généré avec succès !${NC}"
    echo "Pour plus d'informations, consultez la documentation dans README.md"
}

# Exécution du script principal
main "$@"