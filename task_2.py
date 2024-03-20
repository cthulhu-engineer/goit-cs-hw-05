import string
import requests
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict, Counter
import matplotlib.pyplot as plt


def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None


def clean_text(text):
    text = text.lower()
    return text.translate(str.maketrans("", "", string.punctuation))


def map_function(word):
    return (word, 1)


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled


def reduce_function(item):
    word, counts = item
    return word, sum(counts)


def map_reduce(text):
    text = clean_text(text)
    words = text.split()

    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

        shuffled_values = shuffle_function(mapped_values)
        reduced_values = dict(executor.map(reduce_function, shuffled_values.items()))

    return reduced_values


def visualize_top_words(word_counts):
    top_words = dict(Counter(word_counts).most_common(10))

    plt.figure(figsize=(10, 6))
    plt.barh(list(top_words.keys()), list(top_words.values()), color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title('Top 10 Most Frequent Words')
    plt.gca().invert_yaxis()
    plt.show()


if __name__ == '__main__':
    url = "https://www.gutenberg.org/files/2600/2600-0.txt"
    text = get_text(url)
    if text:
        word_counts = map_reduce(text)
        visualize_top_words(word_counts)
    else:
        print("Не вдалося завантажити текст для аналізу.")
