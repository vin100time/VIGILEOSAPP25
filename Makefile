# Makefile pour VIGILEOSAPP25
# Simplifie les commandes Docker et de développement

.PHONY: help build start stop restart logs clean test migrate shell backup restore

# Variables
COMPOSE_FILE = docker-compose.yml
COMPOSE_DEV_FILE = docker-compose.dev.yml
ENV_FILE = .env
ENV_DEV_FILE = .env.development

# Couleurs pour les messages
BLUE = \033[0;34m
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

# Aide par défaut
help: ## Affiche cette aide
	@echo "$(BLUE)VIGILEOSAPP25 - Commandes disponibles:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Exemples:$(NC)"
	@echo "  make dev-start    # Démarrer en mode développement"
	@echo "  make prod-deploy  # Déployer en production"
	@echo "  make logs         # Voir les logs"
	@echo "  make shell        # Accéder au shell Django"

# =============================================================================
# COMMANDES DE DÉVELOPPEMENT
# =============================================================================

dev-setup: ## Configuration initiale pour le développement
	@echo "$(BLUE)Configuration de l'environnement de développement...$(NC)"
	@cp $(ENV_DEV_FILE) $(ENV_FILE) 2>/dev/null || echo "Fichier .env déjà présent"
	@mkdir -p docker/ssl logs backups
	@echo "$(GREEN)Environnement de développement configuré$(NC)"

dev-build: dev-setup ## Construire les images pour le développement
	@echo "$(BLUE)Construction des images de développement...$(NC)"
	@docker compose -f $(COMPOSE_DEV_FILE) --env-file $(ENV_DEV_FILE) build

dev-start: dev-build ## Démarrer tous les services en mode développement
	@echo "$(BLUE)Démarrage des services de développement...$(NC)"
	@docker compose -f $(COMPOSE_DEV_FILE) --env-file $(ENV_DEV_FILE) up -d
	@echo "$(GREEN)Services démarrés:$(NC)"
	@echo "  - Application: http://localhost:8000"
	@echo "  - Frontend: http://localhost:3000"
	@echo "  - Admin: http://localhost:8000/admin"
	@echo "  - API Docs: http://localhost:8000/api/docs"
	@echo "  - MailHog: http://localhost:8025"

dev-stop: ## Arrêter tous les services de développement
	@echo "$(BLUE)Arrêt des services de développement...$(NC)"
	@docker compose -f $(COMPOSE_DEV_FILE) down

dev-restart: dev-stop dev-start ## Redémarrer les services de développement

dev-logs: ## Afficher les logs de développement
	@docker compose -f $(COMPOSE_DEV_FILE) logs -f

dev-shell: ## Accéder au shell Django en développement
	@docker compose -f $(COMPOSE_DEV_FILE) exec web-dev python manage.py shell

dev-migrate: ## Exécuter les migrations en développement
	@docker compose -f $(COMPOSE_DEV_FILE) exec web-dev python manage.py migrate

dev-makemigrations: ## Créer de nouvelles migrations en développement
	@docker compose -f $(COMPOSE_DEV_FILE) exec web-dev python manage.py makemigrations

dev-superuser: ## Créer un superutilisateur en développement
	@docker compose -f $(COMPOSE_DEV_FILE) exec web-dev python manage.py createsuperuser

dev-test: ## Exécuter les tests en développement
	@docker compose -f $(COMPOSE_DEV_FILE) exec web-dev python manage.py test

dev-clean: ## Nettoyer l'environnement de développement
	@echo "$(BLUE)Nettoyage de l'environnement de développement...$(NC)"
	@docker compose -f $(COMPOSE_DEV_FILE) down -v
	@docker system prune -f
	@echo "$(GREEN)Nettoyage terminé$(NC)"

# =============================================================================
# COMMANDES DE PRODUCTION
# =============================================================================

prod-setup: ## Configuration initiale pour la production
	@echo "$(BLUE)Configuration de l'environnement de production...$(NC)"
	@if [ ! -f $(ENV_FILE) ]; then \
		cp .env.example $(ENV_FILE); \
		echo "$(YELLOW)ATTENTION: Modifiez le fichier .env avec vos vraies valeurs$(NC)"; \
	fi
	@mkdir -p docker/ssl logs backups
	@echo "$(GREEN)Environnement de production configuré$(NC)"

prod-build: prod-setup ## Construire les images pour la production
	@echo "$(BLUE)Construction des images de production...$(NC)"
	@docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) build --no-cache

prod-deploy: prod-build ## Déployer en production
	@echo "$(BLUE)Déploiement en production...$(NC)"
	@docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) up -d
	@echo "$(GREEN)Déploiement terminé$(NC)"
	@echo "  - Application: https://localhost"
	@echo "  - Admin: https://localhost/admin"

prod-start: ## Démarrer les services de production
	@docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) up -d

prod-stop: ## Arrêter les services de production
	@docker compose -f $(COMPOSE_FILE) down

prod-restart: prod-stop prod-start ## Redémarrer les services de production

prod-update: ## Mettre à jour l'application en production
	@echo "$(BLUE)Mise à jour de l'application...$(NC)"
	@docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) pull
	@docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) build --no-cache
	@docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) up -d --no-deps web
	@echo "$(GREEN)Mise à jour terminée$(NC)"

prod-logs: ## Afficher les logs de production
	@docker compose -f $(COMPOSE_FILE) logs -f

prod-shell: ## Accéder au shell Django en production
	@docker compose -f $(COMPOSE_FILE) exec web python manage.py shell

prod-migrate: ## Exécuter les migrations en production
	@docker compose -f $(COMPOSE_FILE) exec web python manage.py migrate

# =============================================================================
# COMMANDES GÉNÉRIQUES
# =============================================================================

logs: ## Afficher les logs (détecte automatiquement l'environnement)
	@if [ -f $(ENV_DEV_FILE) ] && docker compose -f $(COMPOSE_DEV_FILE) ps | grep -q "Up"; then \
		make dev-logs; \
	else \
		make prod-logs; \
	fi

shell: ## Accéder au shell Django (détecte automatiquement l'environnement)
	@if [ -f $(ENV_DEV_FILE) ] && docker compose -f $(COMPOSE_DEV_FILE) ps | grep -q "Up"; then \
		make dev-shell; \
	else \
		make prod-shell; \
	fi

migrate: ## Exécuter les migrations (détecte automatiquement l'environnement)
	@if [ -f $(ENV_DEV_FILE) ] && docker compose -f $(COMPOSE_DEV_FILE) ps | grep -q "Up"; then \
		make dev-migrate; \
	else \
		make prod-migrate; \
	fi

# =============================================================================
# SAUVEGARDE ET RESTAURATION
# =============================================================================

backup: ## Sauvegarder la base de données
	@echo "$(BLUE)Sauvegarde de la base de données...$(NC)"
	@mkdir -p backups
	@TIMESTAMP=$$(date +%Y%m%d_%H%M%S); \
	if docker compose -f $(COMPOSE_FILE) ps | grep -q "vigileosapp-postgres"; then \
		docker exec vigileosapp-postgres pg_dump -U vigileosapp_user vigileosapp | gzip > backups/postgres_backup_$$TIMESTAMP.sql.gz; \
	else \
		docker exec vigileosapp-postgres-dev pg_dump -U vigileosapp_dev vigileosapp_dev | gzip > backups/postgres_backup_dev_$$TIMESTAMP.sql.gz; \
	fi
	@echo "$(GREEN)Sauvegarde créée dans le dossier backups/$(NC)"

restore: ## Restaurer la base de données (usage: make restore BACKUP=fichier.sql.gz)
	@if [ -z "$(BACKUP)" ]; then \
		echo "$(RED)Erreur: Spécifiez le fichier de sauvegarde avec BACKUP=fichier.sql.gz$(NC)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)ATTENTION: Cette opération va écraser la base de données actuelle$(NC)"
	@read -p "Êtes-vous sûr ? (y/N): " confirm && [ "$$confirm" = "y" ]
	@echo "$(BLUE)Restauration de la base de données...$(NC)"
	@gunzip -c $(BACKUP) | docker exec -i vigileosapp-postgres psql -U vigileosapp_user -d vigileosapp
	@echo "$(GREEN)Base de données restaurée$(NC)"

# =============================================================================
# MONITORING ET MAINTENANCE
# =============================================================================

health: ## Vérifier la santé des services
	@echo "$(BLUE)Vérification de la santé des services...$(NC)"
	@curl -s http://localhost:8000/api/health/ | python -m json.tool || echo "$(RED)Service web non disponible$(NC)"

status: ## Afficher le statut des conteneurs
	@echo "$(BLUE)Statut des conteneurs:$(NC)"
	@docker compose -f $(COMPOSE_FILE) ps 2>/dev/null || docker compose -f $(COMPOSE_DEV_FILE) ps

clean: ## Nettoyer les ressources Docker
	@echo "$(BLUE)Nettoyage des ressources Docker...$(NC)"
	@docker compose -f $(COMPOSE_FILE) down -v 2>/dev/null || true
	@docker compose -f $(COMPOSE_DEV_FILE) down -v 2>/dev/null || true
	@docker system prune -f
	@docker volume prune -f
	@echo "$(GREEN)Nettoyage terminé$(NC)"

# =============================================================================
# TESTS ET QUALITÉ
# =============================================================================

test: ## Exécuter tous les tests
	@echo "$(BLUE)Exécution des tests...$(NC)"
	@if docker compose -f $(COMPOSE_DEV_FILE) ps | grep -q "Up"; then \
		docker compose -f $(COMPOSE_DEV_FILE) exec web-dev python manage.py test; \
	else \
		docker compose -f $(COMPOSE_FILE) exec web python manage.py test; \
	fi

lint: ## Vérifier la qualité du code
	@echo "$(BLUE)Vérification de la qualité du code...$(NC)"
	@if docker compose -f $(COMPOSE_DEV_FILE) ps | grep -q "Up"; then \
		docker compose -f $(COMPOSE_DEV_FILE) exec web-dev flake8 .; \
	else \
		echo "$(YELLOW)Démarrez l'environnement de développement pour utiliser lint$(NC)"; \
	fi

# =============================================================================
# UTILITAIRES
# =============================================================================

install: dev-setup dev-start ## Installation complète pour le développement
	@echo "$(GREEN)Installation terminée !$(NC)"
	@echo "$(BLUE)Accédez à l'application sur http://localhost:8000$(NC)"

reset: clean install ## Réinitialisation complète

# Par défaut, afficher l'aide
.DEFAULT_GOAL := help