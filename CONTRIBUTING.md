# Guide de contribution à VIGILEOSAPP25

Merci de votre intérêt pour contribuer à VIGILEOSAPP25 ! Ce guide vous aidera à comprendre comment participer au développement du projet.

## 📋 Table des matières

- [Code de conduite](#code-de-conduite)
- [Comment contribuer](#comment-contribuer)
- [Configuration de l'environnement](#configuration-de-lenvironnement)
- [Standards de développement](#standards-de-développement)
- [Processus de pull request](#processus-de-pull-request)
- [Signalement de bugs](#signalement-de-bugs)
- [Demandes de fonctionnalités](#demandes-de-fonctionnalités)

## 🤝 Code de conduite

En participant à ce projet, vous acceptez de respecter notre [Code de Conduite](CODE_OF_CONDUCT.md). Nous nous engageons à maintenir un environnement accueillant et inclusif pour tous.

## 🚀 Comment contribuer

Il existe plusieurs façons de contribuer au projet :

### 🐛 Signaler des bugs
- Utilisez les [GitHub Issues](https://github.com/vin100time/VIGILEOSAPP25/issues)
- Vérifiez d'abord si le bug n'a pas déjà été signalé
- Utilisez le template de bug report

### 💡 Proposer des fonctionnalités
- Ouvrez une issue avec le label "enhancement"
- Décrivez clairement la fonctionnalité souhaitée
- Expliquez pourquoi cette fonctionnalité serait utile

### 📝 Améliorer la documentation
- Corrigez les erreurs de frappe
- Ajoutez des exemples
- Clarifiez les instructions

### 💻 Contribuer au code
- Corrigez des bugs
- Implémentez de nouvelles fonctionnalités
- Améliorez les performances
- Ajoutez des tests

## 🛠️ Configuration de l'environnement

### Prérequis

- Docker 20.10+
- Docker Compose 2.0+
- Git
- Node.js 18+ (pour le développement frontend)
- Python 3.11+ (pour le développement backend)

### Installation

1. **Forkez le projet** sur GitHub

2. **Clonez votre fork** :
   ```bash
   git clone https://github.com/VOTRE_USERNAME/VIGILEOSAPP25.git
   cd VIGILEOSAPP25
   ```

3. **Ajoutez le remote upstream** :
   ```bash
   git remote add upstream https://github.com/vin100time/VIGILEOSAPP25.git
   ```

4. **Configurez l'environnement** :
   ```bash
   make install
   ```

5. **Vérifiez l'installation** :
   ```bash
   make health
   ```

### Environnement de développement

```bash
# Démarrer l'environnement de développement
make dev-start

# Voir les logs
make dev-logs

# Accéder au shell Django
make dev-shell

# Exécuter les tests
make dev-test

# Arrêter l'environnement
make dev-stop
```

## 📏 Standards de développement

### Structure des commits

Nous utilisons la convention [Conventional Commits](https://www.conventionalcommits.org/) :

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types de commits :**
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage, point-virgules manquants, etc.
- `refactor`: Refactoring du code
- `test`: Ajout ou modification de tests
- `chore`: Maintenance, configuration, etc.

**Exemples :**
```bash
feat(api): add equipment monitoring endpoint
fix(frontend): resolve login form validation issue
docs(readme): update installation instructions
test(backend): add unit tests for alert system
```

### Standards de code

#### Python (Backend)

- **Style** : PEP 8
- **Formatage** : Black
- **Imports** : isort
- **Linting** : flake8
- **Type hints** : Utilisez les annotations de type
- **Docstrings** : Format Google

```python
def create_alert(
    title: str,
    description: str,
    severity: AlertSeverity,
    equipment_id: int
) -> Alert:
    """Create a new alert for the specified equipment.
    
    Args:
        title: The alert title
        description: Detailed description of the alert
        severity: Alert severity level
        equipment_id: ID of the affected equipment
        
    Returns:
        The created Alert instance
        
    Raises:
        ValidationError: If the input data is invalid
        Equipment.DoesNotExist: If the equipment doesn't exist
    """
    # Implementation here
```

#### JavaScript/TypeScript (Frontend)

- **Style** : ESLint + Prettier
- **Conventions** : Airbnb style guide
- **Composants** : Functional components avec hooks
- **Types** : TypeScript strict mode

```typescript
interface AlertProps {
  alert: Alert;
  onAcknowledge: (alertId: number) => void;
  onResolve: (alertId: number) => void;
}

const AlertCard: React.FC<AlertProps> = ({
  alert,
  onAcknowledge,
  onResolve
}) => {
  // Implementation here
};
```

### Tests

#### Backend (Python)

```python
import pytest
from django.test import TestCase
from rest_framework.test import APITestCase

class AlertAPITestCase(APITestCase):
    """Test cases for Alert API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_alert(self):
        """Test alert creation via API."""
        data = {
            'title': 'Test Alert',
            'description': 'Test description',
            'severity': 'high',
            'equipment': self.equipment.id
        }
        response = self.client.post('/api/alerts/', data)
        self.assertEqual(response.status_code, 201)
```

#### Frontend (TypeScript)

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { AlertCard } from './AlertCard';

describe('AlertCard', () => {
  const mockAlert = {
    id: 1,
    title: 'Test Alert',
    severity: 'high',
    status: 'open'
  };

  it('renders alert information correctly', () => {
    render(<AlertCard alert={mockAlert} />);
    
    expect(screen.getByText('Test Alert')).toBeInTheDocument();
    expect(screen.getByText('high')).toBeInTheDocument();
  });

  it('calls onAcknowledge when acknowledge button is clicked', () => {
    const mockOnAcknowledge = jest.fn();
    render(
      <AlertCard 
        alert={mockAlert} 
        onAcknowledge={mockOnAcknowledge} 
      />
    );
    
    fireEvent.click(screen.getByText('Acknowledge'));
    expect(mockOnAcknowledge).toHaveBeenCalledWith(1);
  });
});
```

### Exécution des tests

```bash
# Tests backend
make dev-test

# Tests avec couverture
./scripts/run-tests.sh coverage

# Tests spécifiques
./scripts/run-tests.sh unit --verbose
./scripts/run-tests.sh api --fast

# Vérification de la qualité du code
make lint
./scripts/run-tests.sh lint
```

## 🔄 Processus de pull request

### Avant de soumettre

1. **Synchronisez avec upstream** :
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Créez une branche** :
   ```bash
   git checkout -b feature/ma-nouvelle-fonctionnalite
   ```

3. **Développez et testez** :
   ```bash
   # Faites vos modifications
   make dev-test
   make lint
   ```

4. **Commitez vos changements** :
   ```bash
   git add .
   git commit -m "feat: add new monitoring feature"
   ```

5. **Poussez votre branche** :
   ```bash
   git push origin feature/ma-nouvelle-fonctionnalite
   ```

### Soumission de la PR

1. **Ouvrez une Pull Request** sur GitHub
2. **Utilisez le template** fourni
3. **Décrivez clairement** :
   - Ce que fait votre changement
   - Pourquoi c'est nécessaire
   - Comment tester
   - Screenshots si applicable

### Template de PR

```markdown
## Description

Brève description des changements apportés.

## Type de changement

- [ ] Bug fix (changement non-breaking qui corrige un problème)
- [ ] Nouvelle fonctionnalité (changement non-breaking qui ajoute une fonctionnalité)
- [ ] Breaking change (correction ou fonctionnalité qui casserait la fonctionnalité existante)
- [ ] Documentation

## Comment tester

1. Étapes pour reproduire le comportement
2. Commandes à exécuter
3. Résultats attendus

## Checklist

- [ ] Mon code suit les standards du projet
- [ ] J'ai effectué une auto-review de mon code
- [ ] J'ai commenté mon code, particulièrement dans les zones difficiles à comprendre
- [ ] J'ai fait les changements correspondants à la documentation
- [ ] Mes changements ne génèrent pas de nouveaux warnings
- [ ] J'ai ajouté des tests qui prouvent que ma correction est efficace ou que ma fonctionnalité fonctionne
- [ ] Les tests unitaires nouveaux et existants passent localement avec mes changements
```

### Review process

1. **Review automatique** : Les tests CI/CD doivent passer
2. **Review par les pairs** : Au moins une approbation requise
3. **Review par les mainteneurs** : Pour les changements importants
4. **Merge** : Squash and merge par défaut

## 🐛 Signalement de bugs

### Template de bug report

```markdown
**Décrivez le bug**
Une description claire et concise du bug.

**Pour reproduire**
Étapes pour reproduire le comportement :
1. Allez à '...'
2. Cliquez sur '....'
3. Faites défiler jusqu'à '....'
4. Voir l'erreur

**Comportement attendu**
Une description claire et concise de ce que vous attendiez.

**Screenshots**
Si applicable, ajoutez des screenshots pour aider à expliquer votre problème.

**Environnement :**
 - OS: [e.g. Ubuntu 20.04]
 - Navigateur [e.g. chrome, safari]
 - Version [e.g. 22]
 - Version Docker [e.g. 20.10.8]

**Contexte supplémentaire**
Ajoutez tout autre contexte sur le problème ici.

**Logs**
```
Collez les logs pertinents ici
```
```

### Informations à inclure

- **Environnement** : OS, navigateur, versions
- **Étapes de reproduction** : Détaillées et reproductibles
- **Comportement attendu vs actuel**
- **Logs et messages d'erreur**
- **Screenshots ou vidéos** si pertinent

## 💡 Demandes de fonctionnalités

### Template de feature request

```markdown
**La fonctionnalité est-elle liée à un problème ? Décrivez.**
Une description claire et concise du problème. Ex. Je suis toujours frustré quand [...]

**Décrivez la solution que vous aimeriez**
Une description claire et concise de ce que vous voulez qu'il se passe.

**Décrivez les alternatives que vous avez considérées**
Une description claire et concise de toute solution ou fonctionnalité alternative que vous avez considérée.

**Contexte supplémentaire**
Ajoutez tout autre contexte ou screenshots sur la demande de fonctionnalité ici.
```

### Critères d'acceptation

- **Utilité** : La fonctionnalité doit être utile à la majorité des utilisateurs
- **Faisabilité** : Techniquement réalisable dans l'architecture actuelle
- **Maintenance** : N'ajoute pas de complexité excessive
- **Performance** : N'impacte pas négativement les performances

## 🏷️ Labels et milestones

### Labels utilisés

- **Type** : `bug`, `enhancement`, `documentation`, `question`
- **Priorité** : `priority/low`, `priority/medium`, `priority/high`, `priority/critical`
- **Statut** : `status/needs-review`, `status/in-progress`, `status/blocked`
- **Composant** : `component/backend`, `component/frontend`, `component/docker`
- **Difficulté** : `good first issue`, `help wanted`

### Milestones

- **v1.1.0** : Prochaine version mineure
- **v2.0.0** : Prochaine version majeure
- **Backlog** : Fonctionnalités futures

## 🎯 Bonnes pratiques

### Pour les nouveaux contributeurs

1. **Commencez petit** : Cherchez les issues `good first issue`
2. **Posez des questions** : N'hésitez pas à demander de l'aide
3. **Lisez le code** : Familiarisez-vous avec l'architecture
4. **Suivez les conventions** : Respectez les standards établis

### Pour tous les contributeurs

1. **Testez localement** : Toujours tester avant de soumettre
2. **Documentez** : Mettez à jour la documentation si nécessaire
3. **Communiquez** : Tenez les autres au courant de vos travaux
4. **Soyez patient** : Les reviews peuvent prendre du temps

## 📞 Contact

- **Issues GitHub** : Pour les bugs et fonctionnalités
- **Discussions GitHub** : Pour les questions générales
- **Email** : contact@vigileosapp25.com (pour les questions sensibles)

## 🙏 Remerciements

Merci à tous les contributeurs qui rendent ce projet possible ! Votre aide est précieuse pour améliorer VIGILEOSAPP25.

---

**Rappel** : En contribuant à ce projet, vous acceptez que vos contributions soient sous licence MIT.