import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def tokenize_text(text):
    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
    
    return filtered_tokens

def main():
    # Read the text file
    with open('Text.txt', 'r', encoding='utf-8') as file: 
        text = file.read()

    # Tokenize the text
    filtered_tokens = tokenize_text(text)

    # Print the filtered tokens
    print(len(filtered_tokens))
    print(filtered_tokens)

    # Save filtered tokens to a new text file
    with open('filtered_tokens.txt', 'w', encoding='utf-8') as file: 
        file.write('\n'.join(filtered_tokens))

if __name__ == '__main__':
    main()
