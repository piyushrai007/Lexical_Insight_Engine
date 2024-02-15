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
# two links are not working 36 and 49 
#
#data preprosessing tokenization and calculating variables 
import os
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import syllapy
import string

# Function to load stopwords from files
def load_stopwords(directory_path):
    stopwords = set()
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            with open(os.path.join(directory_path, filename), 'r', encoding='ISO-8859-1') as file:
                stopwords.update(word.strip().lower() for word in file)
    return stopwords

# Function to preprocess text
def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text.lower())
    # Remove stopwords and punctuation
    stop_words = load_stopwords('./stop_words')  # Assuming stop words files are in a directory named 'stop_words'
    tokens = [word for word in tokens if word not in stop_words and word not in string.punctuation]
    return tokens

# Function to calculate various text analysis metrics
def calculate_metrics(tokens):
    total_words = len(tokens)
    positive_words = set(open('positive-words.txt', 'r').read().split())
    negative_words = set(open('negative-words.txt', 'r').read().split())
    positive_score = len(positive_words.intersection(tokens))
    negative_score = len(negative_words.intersection(tokens))
    polarity_score = (positive_score - negative_score) / total_words
    subjectivity_score = (positive_score + negative_score) / total_words
    sentences = sent_tokenize(' '.join(tokens))
    avg_sentence_length = sum(len(word_tokenize(sentence)) for sentence in sentences) / len(sentences)
    percentage_complex_words = sum(1 for word in tokens if len(word) > 6) / total_words * 100
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    avg_words_per_sentence = total_words / len(sentences)
    complex_word_count = sum(1 for word in tokens if len(word) > 6)
    syllable_per_word = sum(syllapy.count(word) for word in tokens) / total_words
    personal_pronouns = ['i', 'you', 'he', 'she', 'it', 'we', 'they']
    personal_pronoun_count = sum(1 for word in tokens if word in personal_pronouns)
    avg_word_length = sum(len(word) for word in tokens) / total_words
    return positive_score, negative_score, polarity_score, subjectivity_score, avg_sentence_length, \
           percentage_complex_words, fog_index, avg_words_per_sentence, complex_word_count, total_words, \
           syllable_per_word, personal_pronoun_count, avg_word_length

# Read URLs from Input.xlsx
input_df = pd.read_excel('Input.xlsx')

# Create a DataFrame to store output variables
output_data = []

# Process each text file in the data_txt_files directory
for filename in os.listdir('txt'):
    if filename.endswith('.txt'):
        url_id, _ = os.path.splitext(filename)
        file_path = os.path.join('txt', filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            article_text = file.read()
        # Preprocess text
        tokens = preprocess_text(article_text)
        # Calculate text analysis metrics
        metrics = calculate_metrics(tokens)
        # Find corresponding URL from input DataFrame
        url_row = input_df[input_df['URL_ID'] == url_id]
        if not url_row.empty:
            url = url_row.iloc[0]['URL']
        else:
            url = None
        output_row = [url_id, url] + list(metrics)
        output_data.append(output_row)

# Define column names for output DataFrame
columns = ['URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE',
           'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE',
           'COMPLEX WORD COUNT', 'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH']

# Create output DataFrame
output_df = pd.DataFrame(output_data, columns=columns)

# Write output DataFrame to Excel file
output_df.to_excel('Output.xlsx', index=False)

