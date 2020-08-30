import nltk
import sys
import os
import string
import math

FILE_MATCHES = 4
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }

    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    result = dict()

    data_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), directory)

    for file_name in os.listdir(data_folder):
        if not file_name.endswith(".txt"): continue

        with open(os.path.join(data_folder, file_name), 'r') as file:
            result[file_name] = file.read()

    return result

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = nltk.tokenize.word_tokenize(document)

    return list(filter(None, [
        x.lower().translate({ord(i): None for i in string.punctuation}) 
        for x in tokens if x not in nltk.corpus.stopwords.words("english")
    ]))


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    wordDocumentCounter = dict()
    result = dict()

    for words in documents.values():
        for word in set(words):
            if word not in wordDocumentCounter:
                wordDocumentCounter[word] = 0
            
            wordDocumentCounter[word] = wordDocumentCounter[word] + 1

    for word, count in wordDocumentCounter.items():
        result[word] = math.log(len(documents) / count)

    return result


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    fileNameOrder = dict()

    for fileName, words in files.items():
        fileNameOrder[fileName] = sum([idfs[word] * words.count(word) for word in query if word in words])
    
    sorted_files = [k for k, v in sorted(fileNameOrder.items(), key=lambda kv: kv[1], reverse=True)]

    return sorted_files[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentenceOrder = dict()

    for sentence, words in sentences.items():
        sentenceOrder[sentence] = (
            # Matching word measure
            sum([idfs[word] for word in query if word in words]),
            # Query term density
            sum([words.count(word) / len(words) for word in query if word in words])
        )

    sorted_sentences = [k for k, v in sorted(sentenceOrder.items(), key=lambda kv: kv[1], reverse=True)]

    return sorted_sentences[:n]

if __name__ == "__main__":
    main()
