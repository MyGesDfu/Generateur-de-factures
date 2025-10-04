#!/usr/bin/env python
"""
Script pour créer les utilisateurs et groupes de test pour l'application de facturation.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invoice_generator.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password


def create_groups():
    groups_data = [
        {
            'name': 'Administrateurs',
            'permissions': ['add_product', 'change_product', 'delete_product', 'view_product',
                          'add_invoice', 'change_invoice', 'delete_invoice', 'view_invoice']
        },
        {
            'name': 'Gestionnaires',
            'permissions': ['add_product', 'change_product', 'view_product',
                          'add_invoice', 'change_invoice', 'view_invoice']
        },
        {
            'name': 'Employés',
            'permissions': ['view_product', 'add_invoice', 'change_invoice', 'view_invoice']
        },
        {
            'name': 'Invités',
            'permissions': ['view_product', 'view_invoice']
        }
    ]

    for group_data in groups_data:
        group, created = Group.objects.get_or_create(name=group_data['name'])
        if created:
            print(f"✓ Groupe '{group.name}' créé")
        else:
            print(f"→ Groupe '{group.name}' existe déjà")


def create_test_users():
    users_data = [
        {
            'username': 'admin',
            'password': 'admin123',
            'email': 'admin@example.com',
            'first_name': 'Super',
            'last_name': 'Administrateur',
            'is_staff': True,
            'is_superuser': True,
            'group': 'Administrateurs'
        },
        {
            'username': 'manager',
            'password': 'manager123',
            'email': 'manager@example.com',
            'first_name': 'Marie',
            'last_name': 'Gestionnaire',
            'is_staff': True,
            'is_superuser': False,
            'group': 'Gestionnaires'
        },
        {
            'username': 'employee',
            'password': 'employee123',
            'email': 'employee@example.com',
            'first_name': 'Jean',
            'last_name': 'Employé',
            'is_staff': False,
            'is_superuser': False,
            'group': 'Employés'
        },
        {
            'username': 'guest',
            'password': 'guest123',
            'email': 'guest@example.com',
            'first_name': 'Visiteur',
            'last_name': 'Invité',
            'is_staff': False,
            'is_superuser': False,
            'group': 'Invités'
        }
    ]

    for user_data in users_data:
        if User.objects.filter(username=user_data['username']).exists():
            print(f"→ Utilisateur '{user_data['username']}' existe déjà")
            continue

        user = User.objects.create(
            username=user_data['username'],
            password=make_password(user_data['password']),
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            is_staff=user_data['is_staff'],
            is_superuser=user_data['is_superuser']
        )

        try:
            group = Group.objects.get(name=user_data['group'])
            user.groups.add(group)
            print(f"Utilisateur '{user.username}' créé et ajouté au groupe '{group.name}'")
        except Group.DoesNotExist:
            print(f"Groupe '{user_data['group']}' non trouvé pour l'utilisateur '{user.username}'")


def main():
    print("=== Création des groupes et utilisateurs de test ===\n")

    print("1. Création des groupes...")
    create_groups()

    print("\n2. Création des utilisateurs de test...")
    create_test_users()

    print("\n=== Résumé des comptes créés ===")
    print("Administrateur : admin / admin123")
    print("Gestionnaire  : manager / manager123")
    print("Employé       : employee / employee123")
    print("Invité        : guest / guest123")

    print("\n✓ Configuration terminée avec succès !")


if __name__ == '__main__':
    main()