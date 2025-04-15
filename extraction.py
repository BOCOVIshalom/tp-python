# extraction.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

plt.style.use('ggplot')
sns.set_palette("pastel")



def extraire_donnees():
    """Connecte à la base SQLite et extrait les données fusionnées"""
    conn = sqlite3.connect('ventes_magasin.db')

    
    produits = pd.read_sql("SELECT * FROM Produits", conn)
    clients = pd.read_sql("SELECT * FROM Clients", conn)
    ventes = pd.read_sql("SELECT * FROM Ventes", conn)

    produits = produits.rename(columns={
        'id': 'id_produit',
        'nom': 'nom_produit',
        'prix': 'prix_unitaire'
    })

    clients = clients.rename(columns={
        'id': 'id_client',
        'nom': 'nom_client'
    })

    ventes = ventes.rename(columns={
        'id': 'id_vente',
        'date': 'date_vente'
    })

    df = pd.merge(ventes, produits, on='id_produit')
    df = pd.merge(df, clients, on='id_client')

    df['date_vente'] = pd.to_datetime(df['date_vente'])

    df['montant_total'] = df['quantite'] * df['prix_unitaire']

    conn.close()
    return df


def analyser_donnees(df):
    resultats = {}

    resultats['ca_total'] = df['montant_total'].sum()
    resultats['panier_moyen'] = df['montant_total'].mean()

    resultats['top_produits_quantite'] = df.groupby('nom_produit')['quantite'].sum().nlargest(5)
    resultats['top_produits_ca'] = df.groupby('nom_produit')['montant_total'].sum().nlargest(5)
    resultats['top_clients'] = df.groupby('nom_client')['montant_total'].sum().nlargest(5)

    resultats['stats'] = df[['quantite', 'montant_total']].describe()

    return resultats


def generer_visualisations(df, resultats):

    plt.figure(figsize=(12, 6))
    ca_mensuel = df.resample('M', on='date_vente')['montant_total'].sum()
    sns.lineplot(x=ca_mensuel.index, y=ca_mensuel.values, marker='o')
    plt.title("Évolution du chiffre d'affaires mensuel")
    plt.xlabel("Mois")
    plt.ylabel("Chiffre d'affaires (CFA)")
    plt.tight_layout()
    plt.savefig('evolution_ca.png')
    plt.close()

    plt.figure(figsize=(10, 6))
    top_produits = resultats['top_produits_ca'].reset_index()
    sns.barplot(x='montant_total', y='nom_produit', data=top_produits)
    plt.title("Top 5 produits par chiffre d'affaires")
    for i, v in enumerate(top_produits['montant_total']):
        plt.text(v, i, f"{v:.2f}CFA", va='center')
    plt.tight_layout()
    plt.savefig('top5_produits.png')
    plt.close()

    plt.figure(figsize=(8, 8))
    parts = df.groupby('categorie')['montant_total'].sum()
    parts.plot.pie(autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.4})
    plt.title("Répartition du chiffre d'affaires par catégorie")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig('parts_categories.png')
    plt.close()


if __name__ == "__main__":
    print("Début de l'analyse...")

    print("Extraction des données...")
    donnees = extraire_donnees()

    
    print("Analyse des données...")
    resultats = analyser_donnees(donnees)

    
    print("\n=== RÉSULTATS CLÉS ===")
    print(f"✅ CA total : {resultats['ca_total']:.2f} CFA")
    print(f"✅ Panier moyen : {resultats['panier_moyen']:.2f} CFA")
    print("\nTop 5 produits par CA :")
    print(resultats['top_produits_ca'])
    print("\nStatistiques descriptives :")
    print(resultats['stats'])

    
    print("\nGénération des graphiques...")
    generer_visualisations(donnees, resultats)

    print("✅ Analyse terminée. Graphiques enregistrés dans le dossier courant.")
