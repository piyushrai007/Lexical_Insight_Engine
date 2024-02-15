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
