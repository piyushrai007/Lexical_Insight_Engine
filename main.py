import os
import sys
import pandas as pd
from bs4 import BeautifulSoup
import requests
from nltk.tokenize import sent_tokenize, word_tokenize
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

# Read input Excel file
input_file = sys.argv[1]  # Get input Excel file from command line argument
input_df = pd.read_excel(input_file)

# Process each text file in the txt directory
for filename in os.listdir('txt'):
    if filename.endswith('.txt'):
        url_id, _ = os.path.splitext(filename)
        file_path = os.path.join('txt', filename)
        if not os.path.exists(file_path):
            continue  # Skip rows where text file is not found
        with open(file_path, 'r', encoding='utf-8') as file:
            article_text = file.read()
        # Preprocess text
        tokens = preprocess_text(article_text)
        # Calculate text analysis metrics
        metrics = calculate_metrics(tokens)
        # Find corresponding row in input DataFrame
        row_index = input_df.index[input_df['URL_ID'] == int(url_id)].tolist()
        if row_index:
            row_index = row_index[0]
            # Add calculated metrics as additional columns to input DataFrame
            input_df.loc[row_index, 'POSITIVE SCORE'] = metrics[0]
            input_df.loc[row_index, 'NEGATIVE SCORE'] = metrics[1]
            input_df.loc[row_index, 'POLARITY SCORE'] = metrics[2]
            input_df.loc[row_index, 'SUBJECTIVITY SCORE'] = metrics[3]
            input_df.loc[row_index, 'AVG SENTENCE LENGTH'] = metrics[4]
            input_df.loc[row_index, 'PERCENTAGE OF COMPLEX WORDS'] = metrics[5]
            input_df.loc[row_index, 'FOG INDEX'] = metrics[6]
            input_df.loc[row_index, 'AVG NUMBER OF WORDS PER SENTENCE'] = metrics[7]
            input_df.loc[row_index, 'COMPLEX WORD COUNT'] = metrics[8]
            input_df.loc[row_index, 'WORD COUNT'] = metrics[9]
            input_df.loc[row_index, 'SYLLABLE PER WORD'] = metrics[10]
            input_df.loc[row_index, 'PERSONAL PRONOUNS'] = metrics[11]
            input_df.loc[row_index, 'AVG WORD LENGTH'] = metrics[12]

# Write updated DataFrame to Excel file
input_df.to_excel('Output.xlsx', index=False)
