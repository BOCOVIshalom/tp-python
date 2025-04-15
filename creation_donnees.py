import sqlite3
import random
import os
from datetime import datetime, timedelta

if os.path.exists('ventes_magasin.db'):
    os.remove('ventes_magasin.db')

conn = sqlite3.connect('ventes_magasin.db')
cursor = conn.cursor()

with open('schema.sql', 'r', encoding='utf-8') as f:
    cursor.executescript(f.read())

categories = ['Électronique', 'Vêtements', 'Alimentation', 'Maison', 'Loisirs']
produits = []
for i in range(1, 51):
    nom = f"Produit_{i}"
    categorie = random.choice(categories)
    prix = round(random.uniform(10, 200), 2)
    produits.append((i, nom, categorie, prix))

cursor.executemany("INSERT INTO Produits VALUES (?, ?, ?, ?)", produits)


villes = ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Bordeaux']
clients = []
for i in range(1, 51):
    nom = f"Client_{i}"
    ville = random.choice(villes)
    clients.append((i, nom, ville))

cursor.executemany("INSERT INTO Clients VALUES (?, ?, ?)", clients)


for i in range(1, 51):
    id_produit = random.randint(1, 50)
    id_client = random.randint(1, 50)
    quantite = random.randint(1, 5)
    date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
    cursor.execute("INSERT INTO Ventes VALUES (?, ?, ?, ?, ?)", (i, id_produit, id_client, date, quantite))


conn.commit()
conn.close()

print("✅ Base de données créée avec succès avec 50 produits, 50 clients et 50 ventes !")
