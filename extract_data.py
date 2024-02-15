#extracting data form input.xlsfilr by using beautiful soup
import pandas as pd
from bs4 import BeautifulSoup
import requests

# Step 1: Read URLs from Input.xlsx
input_file = "Input.xlsx"
df = pd.read_excel(input_file)

# Initialize an empty list to store error URLs
error_urls = []

# Step 2: Extract Article Text and Title
for index, row in df.iterrows():
    url = row['URL']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the element containing the article text
    article_content = soup.find('div', class_='td-post-content tagdiv-type')

    # Check if article content is found
    if article_content:
        # Extract title
        title = soup.find('title').get_text()

        # Extract text from <p> and <ol> elements within the article content
        article_text = ""
        for element in article_content.find_all(['p', 'ol']):
            article_text += element.get_text() + "\n"

        # Step 3: Save Extracted Text and Title
        url_id = row['URL_ID']
        with open(f"{url_id}.txt", "w", encoding="utf-8") as file:
            file.write(f"Title: {title}\n\n")
            file.write(article_text)
    else:
        print(f"Article content not found for URL: {url}")
        error_urls.append((row['URL_ID'], url))

print("Extraction and saving complete.")

# Convert error URLs list to DataFrame
error_urls_df = pd.DataFrame(error_urls, columns=['URL_ID', 'URL'])

# Save the URLs with content not found to a separate Excel file
error_file_name = "Error_URLs.xlsx"
error_urls_df.to_excel(error_file_name, index=False)
print(f"Error URLs saved to {error_file_name}.")


#there are some file whose data is not extracted are saved in error_xlxs due to different div name exploring it 
input_file = "Error_URLs.xlsx"
df = pd.read_excel(input_file)

# Initialize an empty list to store error URLs
error_urls = []

# Step 2: Extract Article Text and Title
for index, row in df.iterrows():
    url = row['URL']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the element containing the article text
    article_content = soup.find('div', class_='td-post-content tagdiv-type')

    # Check if article content is found
    if article_content:
        # Extract title
        title = soup.find('title').get_text()

        # Extract text from <p> and <ol> elements within the article content
        article_text = ""
        for element in article_content.find_all(['p', 'ol']):
            article_text += element.get_text() + "\n"

        # Step 3: Save Extracted Text and Title
        url_id = row['URL_ID']
        with open(f"{url_id}.txt", "w", encoding="utf-8") as file:
            file.write(f"Title: {title}\n\n")
            file.write(article_text)
    else:
        print(f"Article content not found for URL: {url}")
        error_urls.append((row['URL_ID'], url))

print("Extraction and saving complete.")