# visualisation.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


plt.style.use('ggplot')
sns.set_palette("pastel")


def charger_donnees():
    conn = sqlite3.connect('ventes_magasin.db')

    produits = pd.read_sql("SELECT * FROM Produits", conn)
    clients = pd.read_sql("SELECT * FROM Clients", conn)
    ventes = pd.read_sql("SELECT * FROM Ventes", conn)

    
    produits = produits.rename(columns={'id': 'id_produit', 'nom': 'nom_produit', 'prix': 'prix_unitaire'})
    clients = clients.rename(columns={'id': 'id_client', 'nom': 'nom_client'})
    ventes = ventes.rename(columns={'id': 'id_vente', 'date': 'date_vente'})

    
    df = pd.merge(ventes, produits, on='id_produit')
    df = pd.merge(df, clients, on='id_client')


    df['date_vente'] = pd.to_datetime(df['date_vente'])
    df['montant_total'] = df['quantite'] * df['prix_unitaire']

    conn.close()
    return df



def afficher_visualisations(df):
    
    plt.figure(figsize=(12, 6))
    ca_mensuel = df.resample('D', on='date_vente')['montant_total'].sum()
    sns.lineplot(x=ca_mensuel.index, y=ca_mensuel.values, marker='o')
    plt.title("Évolution quotidienne du chiffre d'affaires")
    plt.xlabel("Date")
    plt.ylabel("Chiffre d'affaires (CFA)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    
    top_produits = df.groupby('nom_produit')['montant_total'].sum().nlargest(5).reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(x='montant_total', y='nom_produit', data=top_produits)
    plt.title("Top 5 produits par chiffre d'affaires")
    plt.xlabel("Chiffre d'affaires (CFA)")
    plt.ylabel("Produit")
    for i, v in enumerate(top_produits['montant_total']):
        plt.text(v, i, f"{v:.2f}CFA", va='center')
    plt.tight_layout()
    plt.show()

    
    parts = df.groupby('categorie')['montant_total'].sum()
    plt.figure(figsize=(8, 8))
    parts.plot.pie(autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.4})
    plt.title("Répartition du chiffre d'affaires par catégorie")
    plt.ylabel("")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Chargement des données...")
    df = charger_donnees()

    print("Affichage des graphiques...")
    afficher_visualisations(df)
