import requests
from bs4 import BeautifulSoup


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


if __name__ == "__main__":
    url = "https://www.bbc.com/"
    html_content = fetch_html(url)
    if html_content:
        titles, headings = parse_html(html_content)
        print("Titles:")
        for title in titles:
            print(title.get_text())
        print("\nHeadings:")
        for heading in headings:
            print(heading.get_text())
    else:
        print("Failed to retrieve the content.")
