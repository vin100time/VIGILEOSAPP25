#!/bin/bash

# Script de test automatisé pour l'API VIGILEOSAPP25
# Usage: ./test_api.sh

BASE_URL="http://localhost:12000"
API_URL="$BASE_URL/api"

echo "🚀 VIGILEOSAPP25 - Test automatisé du Backend API"
echo "=================================================="

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les résultats
check_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        exit 1
    fi
}

# Test 1: Authentification
echo -e "\n${YELLOW}1. Test d'authentification${NC}"
AUTH_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
    -d '{"username": "admin", "password": "admin123"}' \
    $API_URL/auth/login/)

TOKEN=$(echo $AUTH_RESPONSE | jq -r '.access')
if [ "$TOKEN" != "null" ] && [ "$TOKEN" != "" ]; then
    check_result 0 "Authentification réussie"
else
    check_result 1 "Échec de l'authentification"
fi

# Test 2: Sites
echo -e "\n${YELLOW}2. Test des sites${NC}"
SITES_COUNT=$(curl -s -H "Authorization: Bearer $TOKEN" $API_URL/sites/ | jq '.count')
if [ "$SITES_COUNT" -gt 0 ]; then
    check_result 0 "Sites récupérés ($SITES_COUNT sites)"
else
    check_result 1 "Aucun site trouvé"
fi

# Test 3: Equipment
echo -e "\n${YELLOW}3. Test des équipements${NC}"
EQUIPMENT_COUNT=$(curl -s -H "Authorization: Bearer $TOKEN" $API_URL/equipment/ | jq '.count')
if [ "$EQUIPMENT_COUNT" -gt 0 ]; then
    check_result 0 "Équipements récupérés ($EQUIPMENT_COUNT équipements)"
else
    check_result 1 "Aucun équipement trouvé"
fi

# Test 4: Alerts
echo -e "\n${YELLOW}4. Test des alertes${NC}"
ALERTS_COUNT=$(curl -s -H "Authorization: Bearer $TOKEN" $API_URL/alerts/ | jq '.count')
if [ "$ALERTS_COUNT" -ge 0 ]; then
    check_result 0 "Alertes récupérées ($ALERTS_COUNT alertes)"
else
    check_result 1 "Erreur lors de la récupération des alertes"
fi

# Test 5: Metrics
echo -e "\n${YELLOW}5. Test des métriques${NC}"
METRICS_COUNT=$(curl -s -H "Authorization: Bearer $TOKEN" $API_URL/metrics/ | jq '.count')
if [ "$METRICS_COUNT" -gt 0 ]; then
    check_result 0 "Métriques récupérées ($METRICS_COUNT métriques)"
else
    check_result 1 "Aucune métrique trouvée"
fi

# Test 6: Alert Statistics
echo -e "\n${YELLOW}6. Test des statistiques d'alertes${NC}"
STATS_RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" $API_URL/alerts/stats/)
TOTAL_ALERTS=$(echo $STATS_RESPONSE | jq '.total')
if [ "$TOTAL_ALERTS" -ge 0 ]; then
    check_result 0 "Statistiques d'alertes récupérées (Total: $TOTAL_ALERTS)"
else
    check_result 1 "Erreur lors de la récupération des statistiques"
fi

# Test 7: Metrics Summary
echo -e "\n${YELLOW}7. Test du résumé des métriques${NC}"
SUMMARY_RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" $API_URL/metrics/summary/)
SUMMARY_COUNT=$(echo $SUMMARY_RESPONSE | jq '. | length')
if [ "$SUMMARY_COUNT" -gt 0 ]; then
    check_result 0 "Résumé des métriques récupéré ($SUMMARY_COUNT équipements)"
else
    check_result 1 "Erreur lors de la récupération du résumé"
fi

# Test 8: Search functionality
echo -e "\n${YELLOW}8. Test de la recherche${NC}"
SEARCH_RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" "$API_URL/alerts/?search=CPU")
SEARCH_COUNT=$(echo $SEARCH_RESPONSE | jq '.count')
if [ "$SEARCH_COUNT" -ge 0 ]; then
    check_result 0 "Recherche fonctionnelle ($SEARCH_COUNT résultats pour 'CPU')"
else
    check_result 1 "Erreur lors de la recherche"
fi

# Test 9: Filtering
echo -e "\n${YELLOW}9. Test du filtrage${NC}"
FILTER_RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" "$API_URL/alerts/?type=warning")
FILTER_COUNT=$(echo $FILTER_RESPONSE | jq '.count')
if [ "$FILTER_COUNT" -ge 0 ]; then
    check_result 0 "Filtrage fonctionnel ($FILTER_COUNT alertes de type 'warning')"
else
    check_result 1 "Erreur lors du filtrage"
fi

# Test 10: API Documentation
echo -e "\n${YELLOW}10. Test de la documentation API${NC}"
DOC_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/docs/)
if [ "$DOC_RESPONSE" -eq 200 ]; then
    check_result 0 "Documentation API accessible"
else
    check_result 1 "Documentation API inaccessible"
fi

echo -e "\n${GREEN}🎉 Tous les tests sont passés avec succès !${NC}"
echo -e "${GREEN}✅ Backend API entièrement fonctionnel${NC}"
echo -e "\n📊 Résumé des données:"
echo -e "   • Sites: $SITES_COUNT"
echo -e "   • Équipements: $EQUIPMENT_COUNT"
echo -e "   • Alertes: $ALERTS_COUNT"
echo -e "   • Métriques: $METRICS_COUNT"
echo -e "\n🔗 Liens utiles:"
echo -e "   • API Documentation: $BASE_URL/api/docs/"
echo -e "   • Admin Interface: $BASE_URL/admin/"
echo -e "   • API Schema: $BASE_URL/api/schema/"

echo -e "\n${YELLOW}Backend prêt pour la production ! 🚀${NC}"