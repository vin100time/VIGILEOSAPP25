#!/bin/bash

# Script de tests automatisés pour VIGILEOSAPP25
# Usage: ./scripts/run-tests.sh [type] [options]

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$PROJECT_DIR/backend"

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

# Affichage de l'aide
show_help() {
    echo "Usage: $0 [TYPE] [OPTIONS]"
    echo ""
    echo "Types de tests:"
    echo "  unit          Tests unitaires uniquement"
    echo "  integration   Tests d'intégration uniquement"
    echo "  api           Tests API uniquement"
    echo "  all           Tous les tests (défaut)"
    echo "  coverage      Tests avec rapport de couverture"
    echo "  lint          Vérification de la qualité du code"
    echo "  security      Tests de sécurité"
    echo ""
    echo "Options:"
    echo "  --verbose     Mode verbeux"
    echo "  --fast        Tests rapides uniquement"
    echo "  --parallel    Exécution en parallèle"
    echo "  --failfast    Arrêter au premier échec"
    echo "  --keepdb      Garder la base de données de test"
    echo ""
    echo "Exemples:"
    echo "  $0 unit --verbose"
    echo "  $0 api --fast"
    echo "  $0 coverage"
    echo "  $0 lint"
}

# Tests unitaires
run_unit_tests() {
    log_info "Exécution des tests unitaires..."
    
    local options=""
    if [[ "$VERBOSE" == "true" ]]; then
        options="$options --verbose"
    fi
    if [[ "$FAST" == "true" ]]; then
        options="$options -m 'not slow'"
    fi
    if [[ "$PARALLEL" == "true" ]]; then
        options="$options --numprocesses auto"
    fi
    if [[ "$FAILFAST" == "true" ]]; then
        options="$options --exitfirst"
    fi
    if [[ "$KEEPDB" == "true" ]]; then
        options="$options --reuse-db"
    fi
    
    if docker-compose -f docker-compose.dev.yml ps | grep -q "vigileosapp-web-dev"; then
        # Utiliser le conteneur Docker
        docker-compose -f docker-compose.dev.yml exec -T web-dev python -m pytest -m unit $options
    else
        # Exécution locale
        cd "$BACKEND_DIR"
        python -m pytest -m unit $options
    fi
}

# Tests d'intégration
run_integration_tests() {
    log_info "Exécution des tests d'intégration..."
    
    local options=""
    if [[ "$VERBOSE" == "true" ]]; then
        options="$options --verbose"
    fi
    if [[ "$PARALLEL" == "true" ]]; then
        options="$options --numprocesses auto"
    fi
    if [[ "$FAILFAST" == "true" ]]; then
        options="$options --exitfirst"
    fi
    if [[ "$KEEPDB" == "true" ]]; then
        options="$options --reuse-db"
    fi
    
    if docker-compose -f docker-compose.dev.yml ps | grep -q "vigileosapp-web-dev"; then
        docker-compose -f docker-compose.dev.yml exec -T web-dev python -m pytest -m integration $options
    else
        cd "$BACKEND_DIR"
        python -m pytest -m integration $options
    fi
}

# Tests API
run_api_tests() {
    log_info "Exécution des tests API..."
    
    local options=""
    if [[ "$VERBOSE" == "true" ]]; then
        options="$options --verbose"
    fi
    if [[ "$FAILFAST" == "true" ]]; then
        options="$options --exitfirst"
    fi
    if [[ "$KEEPDB" == "true" ]]; then
        options="$options --reuse-db"
    fi
    
    if docker-compose -f docker-compose.dev.yml ps | grep -q "vigileosapp-web-dev"; then
        docker-compose -f docker-compose.dev.yml exec -T web-dev python -m pytest -m api $options
    else
        cd "$BACKEND_DIR"
        python -m pytest -m api $options
    fi
}

# Tous les tests
run_all_tests() {
    log_info "Exécution de tous les tests..."
    
    local options=""
    if [[ "$VERBOSE" == "true" ]]; then
        options="$options --verbose"
    fi
    if [[ "$FAST" == "true" ]]; then
        options="$options -m 'not slow'"
    fi
    if [[ "$PARALLEL" == "true" ]]; then
        options="$options --numprocesses auto"
    fi
    if [[ "$FAILFAST" == "true" ]]; then
        options="$options --exitfirst"
    fi
    if [[ "$KEEPDB" == "true" ]]; then
        options="$options --reuse-db"
    fi
    
    if docker-compose -f docker-compose.dev.yml ps | grep -q "vigileosapp-web-dev"; then
        docker-compose -f docker-compose.dev.yml exec -T web-dev python -m pytest $options
    else
        cd "$BACKEND_DIR"
        python -m pytest $options
    fi
}

# Tests avec couverture
run_coverage_tests() {
    log_info "Exécution des tests avec rapport de couverture..."
    
    local options="--cov=. --cov-report=html --cov-report=term-missing"
    if [[ "$VERBOSE" == "true" ]]; then
        options="$options --verbose"
    fi
    if [[ "$FAST" == "true" ]]; then
        options="$options -m 'not slow'"
    fi
    if [[ "$KEEPDB" == "true" ]]; then
        options="$options --reuse-db"
    fi
    
    if docker-compose -f docker-compose.dev.yml ps | grep -q "vigileosapp-web-dev"; then
        docker-compose -f docker-compose.dev.yml exec -T web-dev python -m pytest $options
        log_info "Rapport de couverture généré dans htmlcov/"
    else
        cd "$BACKEND_DIR"
        python -m pytest $options
        log_info "Rapport de couverture généré dans htmlcov/"
    fi
}

# Vérification de la qualité du code
run_lint_checks() {
    log_info "Vérification de la qualité du code..."
    
    cd "$BACKEND_DIR"
    
    # Flake8
    log_info "Vérification avec flake8..."
    if docker-compose -f docker-compose.dev.yml ps | grep -q "vigileosapp-web-dev"; then
        docker-compose -f docker-compose.dev.yml exec -T web-dev flake8 .
    else
        flake8 .
    fi
    
    # Black
    log_info "Vérification du formatage avec black..."
    if docker-compose -f docker-compose.dev.yml ps | grep -q "vigileosapp-web-dev"; then
        docker-compose -f docker-compose.dev.yml exec -T web-dev black --check .
    else
        black --check .
    fi
    
    # isort
    log_info "Vérification des imports avec isort..."
    if docker-compose -f docker-compose.dev.yml ps | grep -q "vigileosapp-web-dev"; then
        docker-compose -f docker-compose.dev.yml exec -T web-dev isort --check-only .
    else
        isort --check-only .
    fi
    
    log_success "Vérifications de qualité terminées"
}

# Tests de sécurité
run_security_tests() {
    log_info "Exécution des tests de sécurité..."
    
    cd "$BACKEND_DIR"
    
    # Bandit pour la sécurité Python
    log_info "Analyse de sécurité avec bandit..."
    if docker-compose -f docker-compose.dev.yml ps | grep -q "vigileosapp-web-dev"; then
        docker-compose -f docker-compose.dev.yml exec -T web-dev bandit -r . -x tests/,migrations/
    else
        bandit -r . -x tests/,migrations/
    fi
    
    # Safety pour les vulnérabilités des dépendances
    log_info "Vérification des vulnérabilités avec safety..."
    if docker-compose -f docker-compose.dev.yml ps | grep -q "vigileosapp-web-dev"; then
        docker-compose -f docker-compose.dev.yml exec -T web-dev safety check
    else
        safety check
    fi
    
    log_success "Tests de sécurité terminés"
}

# Fonction principale
main() {
    cd "$PROJECT_DIR"
    
    # Valeurs par défaut
    TEST_TYPE="all"
    VERBOSE="false"
    FAST="false"
    PARALLEL="false"
    FAILFAST="false"
    KEEPDB="false"
    
    # Analyse des arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            unit|integration|api|all|coverage|lint|security)
                TEST_TYPE="$1"
                shift
                ;;
            --verbose)
                VERBOSE="true"
                shift
                ;;
            --fast)
                FAST="true"
                shift
                ;;
            --parallel)
                PARALLEL="true"
                shift
                ;;
            --failfast)
                FAILFAST="true"
                shift
                ;;
            --keepdb)
                KEEPDB="true"
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                log_error "Option inconnue: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    echo "🧪 VIGILEOSAPP25 - Tests automatisés"
    echo "Type de test: $TEST_TYPE"
    echo "=================================="
    
    case $TEST_TYPE in
        "unit")
            run_unit_tests
            ;;
        "integration")
            run_integration_tests
            ;;
        "api")
            run_api_tests
            ;;
        "all")
            run_all_tests
            ;;
        "coverage")
            run_coverage_tests
            ;;
        "lint")
            run_lint_checks
            ;;
        "security")
            run_security_tests
            ;;
        *)
            log_error "Type de test invalide: $TEST_TYPE"
            show_help
            exit 1
            ;;
    esac
    
    log_success "Tests terminés avec succès !"
}

# Exécution du script principal
main "$@"