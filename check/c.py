import pandas as pd
import requests
from bs4 import BeautifulSoup

# Read URLs from error.xls
input_file ="Error_URLs.xlsx"
df = pd.read_excel(input_file)

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    url = row['URL']  # Assuming the column name in the Excel file is 'url'

    # Send a GET request to the URL and retrieve the HTML content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all div elements with class 'tdb-block-inner' and 'td-fix-index'
        divs = soup.find_all('div', class_='tdb-block-inner td-fix-index')

        # Check if any divs were found
        if divs:
            # Extract the title
            title = soup.title.get_text()

            # Extract the content from all found divs
            content = "\n".join([div.get_text() for div in divs])

            # Save the content and title to a .txt file
            url_id = row['URL_ID']  # Assuming the column name in the Excel file is 'url_id'
            with open(f"{url_id}.txt", "w", encoding="utf-8") as file:
                file.write(f"Title: {title}\n\n")
                file.write(content)

            print(f"Content saved for URL_ID: {url_id}")
        else:
            print(f"No divs found for URL: {url}")
    else:
        print(f"Failed to retrieve the HTML content for URL: {url}")

print("Extraction and saving complete.")
