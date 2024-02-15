# Load positive and negative word lists
positive_words = set()
with open('positive-words.txt', 'r', encoding='ISO-8859-1') as file:
    positive_words.update(word.strip().lower() for word in file.readlines())

negative_words = set()
with open('negative-words.txt', 'r', encoding='ISO-8859-1') as file:
    negative_words.update(word.strip().lower() for word in file.readlines())

# Tokenize preprocessed text
tokens = preprocessed_text.txt.split()

# Calculate positive and negative scores
positive_score = sum(1 for token in tokens if token in positive_words)
negative_score = sum(1 for token in tokens if token in negative_words)

# Calculate polarity score
total_words = len(tokens)
polarity_score = (positive_score - negative_score) / total_words

# Calculate subjectivity score
subjectivity_score = (positive_score + negative_score) / total_words

print("Positive Score:", positive_score)
print("Negative Score:", negative_score)
print("Polarity Score:", polarity_score)
print("Subjectivity Score:", subjectivity_score)
