from bertopic import BERTopic
from bertopic.representation import MaximalMarginalRelevance
from hdbscan import HDBSCAN
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from umap import UMAP


def get_topics(sentences, n_dimensions) -> tuple[BERTopic, list[int]]:
    """
    Generates topics from a list of sentences using BERTopic.
    Fine-tunes the model with UMAP, HDBScan, TF-IDF Vectorizer, and Maximal Marginal Relevance.
    """
    umap = UMAP(
        n_components=n_dimensions,
        spread=1.8,
        min_dist=0.05,
        n_neighbors=40,
        metric="cosine",
        random_state=42,
    )

    hdbscan_model = HDBSCAN(min_cluster_size=118, prediction_data=True)

    stop_words_pt = set(stopwords.words("portuguese"))
    aditional_stopwords = []
    combined_stop_words = list(stop_words_pt.union(aditional_stopwords))
    tfidf_vectorizer = TfidfVectorizer(stop_words=combined_stop_words, smooth_idf=False)

    # Maximal Marginal Relevance (decrease the redundancy and improve the diversity of keywords)
    representation_model = MaximalMarginalRelevance(diversity=0.9)

    topic_model = BERTopic(
        language="portuguese",
        umap_model=umap,
        hdbscan_model=hdbscan_model,
        vectorizer_model=tfidf_vectorizer,
        representation_model=representation_model,
        nr_topics=2
    )

    topics = topic_model.fit_transform(sentences)

    return topic_model, topics


def get_cluster_topics(sentences, n_dimensions) -> list[dict]:
    """
    Generates topics using BERTopic for each cluster from a dictionary of sentences.
    """
    cluster_topics = []

    for cluster, summaries in sentences.items():
        print(f"Running BERTopic on cluster {cluster}...")
        topic_model, topics = get_topics(summaries, n_dimensions)

        cluster_topics.append(
            {"Cluster": cluster, "Topic": topics, "Model": topic_model, "Summaries": summaries}
        )

    return cluster_topics
