# Books Scraper

## Description

Ce projet est un script Python conçu pour scraper des informations sur des livres à partir du site [Books to Scrape](http://books.toscrape.com). Le script extrait les détails des livres de chaque catégorie, télécharge les images correspondantes, et génère des fichiers CSV contenant les informations recueillies pour chaque catégorie.

Les informations extraites pour chaque livre incluent :
- Le titre
- L'UPC
- Le type de produit
- Le prix (hors taxes et TTC)
- Le montant des taxes
- La disponibilité
- La note (étoiles)
- Le nombre de commentaires
- La description
- L'image du livre

## Fonctionnalités

- **Extraction des livres** : Le script parcourt toutes les catégories de livres et scrape les informations de chaque livre.
- **Téléchargement des images** : Chaque image de livre est téléchargée et sauvegardée dans un dossier correspondant à sa catégorie.
- **Fichiers CSV** : Les informations de chaque catégorie de livres sont enregistrées dans un fichier CSV distinct.
- **Pagination automatique** : Le script gère automatiquement la pagination pour récupérer tous les livres d'une catégorie.

## Prérequis

Avant d'exécuter le script, assurez-vous d'avoir installé les dépendances suivantes :

- Python 3.x
- Bibliothèques Python :
  - `requests`
  - `beautifulsoup4`
  - `lxml`

Vous pouvez installer les dépendances nécessaires via pip :

```bash
pip install requests beautifulsoup4 lxml
```
## Structure des Dossiers
Le script génère les fichiers et dossiers suivants :

- *categories_books/*  : Contient un fichier CSV pour chaque catégorie de livres, avec les détails des livres.
- *images_book2scrap/* : Contient un sous-dossier pour chaque catégorie, où les images des livres sont téléchargées.
## Utilisation
Pour exécuter le script, suivez les étapes ci-dessous :

1.  Clonez ce dépôt GitHub sur votre machine locale :
```bash

git clone https://github.com/votre-utilisateur/votre-depot.git 
```
2. Accédez au dossier du projet :
```bash

cd votre-depot

```
3. Exécutez le script Python : 
```bash

python main.py
```
Le script commencera à extraire les informations de toutes les catégories de livres du site Books to Scrape. Les fichiers CSV seront générés dans le dossier categories_books, et les images seront téléchargées dans le dossier images_book2scrap.

Exemple de Résultat
- **Fichier CSV** : Chaque fichier CSV contiendra les colonnes suivantes :
**Title, UPC, Product Type, Price (Excl. Tax), Price (Incl. Tax), Tax, Availability, Rating, Number of Reviews, Description**
- **Images** : Les images seront sauvegardées dans un dossier par catégorie avec un nom basé sur le titre du livre.
## Problèmes connus
- Certaines pages peuvent générer des erreurs 404 si elles n'existent pas. Le script gère cela en passant à la page suivante sans interrompre l'exécution.
- Assurez-vous d'avoir une bonne connexion Internet pour télécharger les images correctement.
## Contributions
Les contributions sont les bienvenues ! Si vous trouvez un bug ou souhaitez proposer des améliorations, n'hésitez pas à ouvrir une issue ou soumettre une pull request.

Licence
Ce projet est sous licence MIT. Vous êtes libre de l'utiliser, de le modifier et de le distribuer.'''


