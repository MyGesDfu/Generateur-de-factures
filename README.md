# Générateur de Factures

Une application web Django complète pour la gestion de produits et la génération de factures.

## Fonctionnalités

### 🛍️ Gestion des Produits
- Créer, modifier et supprimer des produits
- Gérer les informations : nom, prix, date de péremption
- Détection automatique des produits périmés
- Recherche et pagination
- Interface CRUD complète

### 📄 Système de Facturation
- Créer et modifier des factures
- Sélectionner des produits avec quantités
- Calcul automatique des totaux
- Numérotation automatique des factures
- Détail complet des factures
- Gestion des articles de facture

### 🎯 Interface Utilisateur
- Interface moderne avec Bootstrap 5
- Design responsive
- Navigation intuitive
- Messages de confirmation
- Pagination des listes
- Recherche en temps réel

### 📊 Fonctionnalités Avancées
- Système de pagination
- Recherche par nom/prix pour les produits
- Recherche par numéro/montant pour les factures
- Validation des formulaires
- Admin Django configuré
- API pour récupérer les prix des produits
- **Dark Mode** avec sauvegarde des préférences

## Installation

### Prérequis
- Python 3.8+
- pip

### Installation locale

1. **Cloner le repository**
   ```bash
   git clone https://github.com/MyGesDfu/Generateur-de-factures
   cd "Generateur de factures"
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Effectuer les migrations**
   ```bash
   python manage.py migrate
   ```

4. **Créer un superuser (optionnel)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Ajouter des données d'exemple**
   ```bash
   python create_sample_data.py
   python create_test_users.py
   ```

6. **Démarrer le serveur**
   ```bash
   python manage.py runserver
   ```

7. **Accéder à l'application**
   - Application principale : http://127.0.0.1:8000/
   - Administration Django : http://127.0.0.1:8000/admin/


## Modèles de Données

### Product (Produit)
- `id` : Identifiant unique (auto-généré)
- `name` : Nom du produit (string, max 200 caractères)
- `price` : Prix en euros (decimal, min 0.01)
- `expiration_date` : Date de péremption (date)
- `created_at` : Date de création (auto)
- `updated_at` : Date de modification (auto)

### Invoice (Facture)
- `id` : Identifiant unique (auto-généré)
- `invoice_number` : Numéro de facture (string unique)
- `created_at` : Date de création (auto)
- `total_amount` : Montant total (decimal, calculé auto)

### InvoiceItem (Article de Facture)
- `invoice` : Référence vers la facture (ForeignKey)
- `product` : Référence vers le produit (ForeignKey)
- `quantity` : Quantité (entier positif)
- `unit_price` : Prix unitaire (decimal, copié du produit)


## Stack Technique

- **Framework** : Django 5.2.6
- **Base de données** : SQLite (par défaut)
- **Frontend** : Bootstrap 5.1.3 + Bootstrap Icons
- **Langage** : Python 3.x
- **Styles** : CSS intégré via CDN Bootstrap


## Développement

### Commandes utiles

```bash
# Créer une nouvelle migration
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Lancer les tests
python manage.py test

# Collecte des fichiers statiques (production)
python manage.py collectstatic
```


## Auteur

Développé par Danny Fu dans le cadre d'un exercice pratique Django.
