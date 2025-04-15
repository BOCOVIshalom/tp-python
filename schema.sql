CREATE TABLE IF NOT EXISTS Produits (
    id INTEGER PRIMARY KEY,
    nom TEXT,
    categorie TEXT,
    prix REAL
);

CREATE TABLE IF NOT EXISTS Clients (
    id INTEGER PRIMARY KEY,
    nom TEXT,
    ville TEXT
);

CREATE TABLE IF NOT EXISTS Ventes (
    id INTEGER PRIMARY KEY,
    id_produit INTEGER,
    id_client INTEGER,
    date TEXT,
    quantite INTEGER
);
