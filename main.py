import requests
from bs4 import BeautifulSoup
import csv


def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    titles = soup.find_all('title')
    headings = soup.find_all(['h1', 'h2', 'h3'])
    return titles, headings


def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Type", "Content"])
        for item in data:
            writer.writerow(item)


if __name__ == "__main__":
    url = "https://www.bbc.com/"
    html_content = fetch_html(url)
    if html_content:
        titles, headings = parse_html(html_content)
        data = [("Title", title.get_text()) for title in titles]
        data += [("Heading", heading.get_text()) for heading in headings]
        save_to_csv(data, 'scraped_data.csv')
        print("Data saved to scraped_data.csv")
    else:
        print("Failed to retrieve the content.")
