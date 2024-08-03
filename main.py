import requests
from bs4 import BeautifulSoup
import csv
import argparse
from collections import Counter


def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def parse_html(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        titles = soup.find_all('title')
        headings = soup.find_all(['h1', 'h2', 'h3'])
        return titles, headings
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return [], []


def save_to_csv(data, filename):
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["URL", "Type", "Content"])
            for item in data:
                writer.writerow(item)
        print(f"Data saved to {filename}")
    except IOError as e:
        print(f"Error saving to {filename}: {e}")


def analyze_data(data):
    all_headings = [content for url, type_,
                    content in data if type_ == "Heading"]
    word_counts = Counter(word.lower()
                          for heading in all_headings for word in heading.split())
    return word_counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simple Web Scraper')
    parser.add_argument('urls', nargs='+', type=str,
                        help='The URLs of the webpages to scrape')
    parser.add_argument('--output', type=str,
                        default='scraped_data.csv', help='The output CSV file')

    args = parser.parse_args()

    all_data = []
    for url in args.urls:
        html_content = fetch_html(url)
        if html_content:
            titles, headings = parse_html(html_content)
            data = [(url, "Title", title.get_text()) for title in titles]
            data += [(url, "Heading", heading.get_text())
                     for heading in headings]
            all_data.extend(data)
        else:
            print(f"Failed to retrieve the content from {url}")

    if all_data:
        save_to_csv(all_data, args.output)
        word_counts = analyze_data(all_data)
        print("Word Frequency in Headings:")
        for word, count in word_counts.most_common(10):
            print(f"{word}: {count}")
