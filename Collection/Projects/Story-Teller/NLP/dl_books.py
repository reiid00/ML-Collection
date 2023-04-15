# !pip install requests beautifulsoup4 # required

import os
import re
import requests
from bs4 import BeautifulSoup

# Set a directory to save the downloaded books
save_dir = 'data/books/'
os.makedirs(save_dir, exist_ok=True)

# Fetch the top 100 books list from Project Gutenberg
url = 'https://www.gutenberg.org/browse/scores/top'
response = requests.get(url)

# Parse the response HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find the top 100 books section in the HTML
ol = soup.find_all('ol')[0]

# Extract the book links
book_links = ol.find_all('a')

# Function to find the TXT file URL from the book's HTML page
def find_txt_file_url(book_page_url):
    book_page_url = book_page_url.replace('ebooks','files')
    book_page_response = requests.get(book_page_url)
    book_page_soup = BeautifulSoup(book_page_response.text, 'html.parser')
    file_links = book_page_soup.find_all('a', href=re.compile(r'\d+-0\.txt'))

    if file_links:
        return f'{book_page_url}/{file_links[0]["href"]}'
    return None

# Iterate through the book links and download the books
for idx, book_link in enumerate(book_links):
    book_page_url = 'https://www.gutenberg.org' + book_link['href']
    book_title = book_link.text.strip()

    print(f'Downloading {idx + 1}/100: {book_title}')

    txt_file_url = find_txt_file_url(book_page_url)
    print(txt_file_url)

    if txt_file_url:
        try:
            # Fetch the book content
            book_response = requests.get(txt_file_url)
            book_response.raise_for_status()

            # Save the book to a file
            with open(os.path.join(save_dir, f'{idx + 1:03d}_{book_title}.txt'), 'w', encoding='utf-8') as f:
                f.write(book_response.text)

        except requests.exceptions.RequestException as e:
            print(f'Error downloading {book_title}: {e}')
    else:
        print(f'Error: TXT file URL not found for {book_title}')

print('Finished downloading the top 100 books from Project Gutenberg.')