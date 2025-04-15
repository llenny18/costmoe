import requests
from bs4 import BeautifulSoup

# Replace this with the website URL you want to scrape
url = "https://en.wikipedia.org/wiki/Main_Page"

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Get the raw HTML content
    html_content = response.text

    # Optionally parse it with BeautifulSoup (prettified)
    soup = BeautifulSoup(html_content, "html.parser")
    pretty_html = soup.prettify()

    # Print or save the HTML
    print(pretty_html)

    # Save to a file
    with open("scraped_page.html", "w", encoding="utf-8") as f:
        f.write(pretty_html)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
