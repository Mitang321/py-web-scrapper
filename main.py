import requests

def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

if __name__ == "__main__":
    url = "https://www.bbc.com/"
    html_content = fetch_html(url)
    if html_content:
        print(html_content[:500])  # Print the first 500 characters of the HTML content
    else:
        print("Failed to retrieve the content.")
