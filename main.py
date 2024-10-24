import csv
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

# Fonction pour obtenir le contenu HTML d'une page
def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

# Fonction pour télécharger une image
def download_image(image_url, save_path):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

# Fonction pour extraire toutes les informations d'un livre
def extract_book_details(book_url):
    soup = get_soup(book_url)
    
    # Extraire les détails du livre
    title = soup.find('div', class_='product_main').h1.text
    price_incl_tax = soup.find('th', text='Price (incl. tax)').find_next('td').text
    price_excl_tax = soup.find('th', text='Price (excl. tax)').find_next('td').text
    tax = soup.find('th', text='Tax').find_next('td').text
    availability = soup.find('th', text='Availability').find_next('td').text.strip()
    product_type = soup.find('th', text='Product Type').find_next('td').text
    upc = soup.find('th', text='UPC').find_next('td').text
    num_reviews = soup.find('th', text='Number of reviews').find_next('td').text
    rating = soup.find('p', class_='star-rating')['class'][1]
    
    description_tag = soup.find('meta', {'name': 'description'})
    description = description_tag['content'].strip() if description_tag else "No description available"
    
    # URL de l'image
    image_url = soup.find('img')['src']
    image_url = urljoin(book_url, image_url)  # Résoudre le chemin relatif de l'image
    
    return [title, upc, product_type, price_excl_tax, price_incl_tax, tax, availability, rating, num_reviews, description, image_url]

# Fonction pour extraire les informations de tous les livres d'une page
def extract_books_from_page(category_url, category_name):
    soup = get_soup(category_url)
    books_data = []
    
    # Trouver tous les livres sur la page
    books = soup.find_all('article', class_='product_pod')
    
    # Extraire les informations de chaque livre
    for book in books:
        book_url = book.h3.a['href'].replace('../../../', 'http://books.toscrape.com/catalogue/')
        book_details = extract_book_details(book_url)
        
        # Télécharger l'image du livre
        save_image(book_details[-1], book_details[0], category_name)
        
        books_data.append(book_details[:-1])  # On enlève l'URL de l'image pour le CSV
    
    return books_data

# Fonction pour créer des dossiers et télécharger les images
def save_image(image_url, book_title, category_name):
    # Nettoyer le titre du livre pour l'utiliser comme nom de fichier
    book_title_clean = re.sub(r'[^\w\s-]', '', book_title).strip().replace(' ', '_')
    
    # Chemin du répertoire des images pour chaque catégorie
    category_dir = f'images_book2scrap/{category_name}'
    
    # Créer le répertoire pour chaque catégorie s'il n'existe pas
    if not os.path.exists(category_dir):
        os.makedirs(category_dir)
    
    # Chemin complet où l'image sera sauvegardée
    image_path = f"{category_dir}/{book_title_clean}.jpg"
    
    # Télécharger l'image
    download_image(image_url, image_path)

# Fonction pour parcourir toutes les pages d'une catégorie
def extract_books_from_category(category_url, category_name):
    page_number = 1
    all_books = []

    while True:
        # Construire l'URL pour chaque page
        url = f"{category_url}/page-{page_number}.html" if page_number > 1 else category_url
        soup = get_soup(url)
        
        # Extraire les livres de la page actuelle
        books = extract_books_from_page(url, category_name)
        if not books:  # Si aucune donnée de livre n'est trouvée, c'est la dernière page
            break
        
        all_books.extend(books)
        page_number += 1

    return all_books

# Fonction pour enregistrer les livres dans un fichier CSV
def save_books_to_csv(books, category_name):
    # Créer un répertoire pour stocker les fichiers CSV si besoin
    if not os.path.exists('categories_books'):
        os.makedirs('categories_books')
    
    # Sauvegarder dans un fichier CSV
    with open(f'categories_books/{category_name}.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # En-tête avec toutes les informations sauf l'image
        writer.writerow(['Title', 'UPC', 'Product Type', 'Price (Excl. Tax)', 'Price (Incl. Tax)', 'Tax', 'Availability', 'Rating', 'Number of Reviews', 'Description'])
        writer.writerows(books)

# Fonction pour extraire les livres de toutes les catégories
def extract_all_categories(base_url):
    soup = get_soup(base_url)
    
    # Trouver toutes les catégories
    categories = soup.find('ul', class_='nav-list').find_all('a')
    
    # Parcourir chaque catégorie
    for category in categories[1:]:  # Ignorer la première catégorie générale
        cagtegory_name = category.text.strip().replace(' ', '_')
        category_url = f"{base_url}/{category['href']}".replace('index.html', '')
        
        print(f"Extracting books for category: {category_name}")
        books = extract_books_from_category(category_url, category_name)
        save_books_to_csv(books, category_name)
        print(f"Saved {len(books)} books for {category_name}.")

# URL de base du site
base_url = 'http://books.toscrape.com'

# Lancer l'extraction pour toutes les catégories
extract_all_categories(base_url)
