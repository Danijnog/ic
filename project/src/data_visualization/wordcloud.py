import matplotlib.pyplot as plt
import nltk
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud

N_WORDS = 100


def get_sentences_from_clusters(df) -> dict:
    """
    Group labels by cluster and returns them as a dictionary.
    Keys: Cluster identifiers.
    Values: Lists of sentences (labels) for each cluster.
    """
    sentences = df.groupby("cluster")["label"].apply(list).to_dict()

    return sentences


def generate_wordcloud(words, title) -> None:
    """
    Generates and saves a WordCloud image from a list of words.
    """
    wordcloud = WordCloud(width=800, height=400, background_color="black").generate(" ".join(words))
    path = f"utils/wordclouds/wordcloud_{title}.png"

    plt.figure(figsize=(8, 4))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title(title)
    plt.axis("off")
    plt.savefig(path)
    plt.show()


def word_cloud(sentences) -> None:
    """
    Generates WordClouds for each cluster from a dictionary of sentences.
    """
    nltk.download("stopwords")

    stop_words_pt = set(stopwords.words("portuguese"))
    stop_words_en = set(stopwords.words("english"))

    aditional_stop_words = []
    combined_stop_words = list(stop_words_pt.union(stop_words_en).union(aditional_stop_words))

    # Merging all summaries and creating a list of labels
    all_sentences = []
    labels = []
    for label, sents in sentences.items():
        all_sentences.extend(sents)
        labels.extend([label] * len(sents))

    cluster_documents = {label: " ".join(sents) for label, sents in sentences.items()}

    # Creates the Vectorizer TF-IDF
    tfidf_vectorizer = TfidfVectorizer(stop_words=combined_stop_words, smooth_idf=False, max_df=0.9)

    # Fit and transform the sentences
    tfidf_matrix = tfidf_vectorizer.fit_transform(cluster_documents.values())

    # Extract the name of the words (features)
    feature_names = tfidf_vectorizer.get_feature_names_out()

    # Creates a DataFrame with the values of TF-IDF
    tfidf_df = pd.DataFrame(
        tfidf_matrix.toarray(), index=cluster_documents.keys(), columns=feature_names
    )

    # Normalizes for each class
    tfidf_normalized = tfidf_df.div(tfidf_df.sum(axis=1), axis=0)

    # Selects the top 100 words for each class
    top_words_by_class = {}
    for label in tfidf_normalized.index:
        top_words_by_class[label] = tfidf_normalized.loc[label].nlargest(N_WORDS).index.tolist()

    print(f"Documents: {len(cluster_documents)}")
    # Generates wordcloud for each class
    for label, words in top_words_by_class.items():
        generate_wordcloud(words, f"Cluster - {label}")
