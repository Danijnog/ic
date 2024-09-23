from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords

import os
import pandas as pd
import matplotlib.pyplot as plt

N_WORDS = 100

from connection.db_processing import clear_messages

def get_df_for_word_cloud(groups, min_number_of_messages):
    """Retorna um DataFrame que será utilizado para criar um objeto WordCloud."""
    data = []
    
    for index, row in groups.iterrows():
        group_id = row['channel_id']
        group_dir = f'data/msgPerGroup/ID_{group_id}'
        csv_files = os.listdir(group_dir)
        csv_files.sort()

        for file in csv_files:
            file_path = f'{group_dir}/{file}'
            df = pd.read_csv(file_path)
            num_messages = len(df)

            if num_messages <= min_number_of_messages:
                messages = clear_messages(file_path)
                data.append({
                    'message': messages
                })
    
    df = pd.DataFrame(data)

    return df

def get_sentences_from_clusters(df) -> dict:
    sentences = df.groupby('cluster')['label'].apply(list).to_dict()

    return sentences

def generate_wordcloud(words, title):
    wordcloud = WordCloud(width = 800, height = 400, background_color = 'black').generate(' '.join(words))
    path = f"utils/wordclouds/wordcloud_{title}.png"

    plt.figure(figsize = (8, 4))
    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.title(title)
    plt.axis('off')
    plt.savefig(path)
    plt.show()

def word_cloud(sentences):
    """Gera as nuvens de palavras de todos os clusters a partir do dicionário sentences passado como parâmetro."""
    nltk.download('stopwords')

    stop_words_pt = set(stopwords.words('portuguese'))
    stop_words_en = set(stopwords.words('english'))

    aditional_stop_words = []
    combined_stop_words = list(stop_words_pt.union(stop_words_en).union(aditional_stop_words))

    # Unindo todos os sumários e criando uma lista de labels
    all_sentences = []
    labels = []
    for label, sents in sentences.items():
        all_sentences.extend(sents)
        labels.extend([label] * len(sents))
    
    cluster_documents = {label: ' '.join(sents) for label, sents in sentences.items()}

    # Cria o vetorizador TF-IDF
    tfidf_vectorizer = TfidfVectorizer(stop_words = combined_stop_words, smooth_idf = False, max_df = 0.9)

    # Ajustando e transformando as sentenças
    tfidf_matrix = tfidf_vectorizer.fit_transform(cluster_documents.values())

    # Extraindo os nomes das palavras (features)
    feature_names = tfidf_vectorizer.get_feature_names_out()

    # Criando um DataFrame com os valores de TF-IDF
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), index = cluster_documents.keys(), columns = feature_names)

    # Normalizando para cada classe
    tfidf_normalized = tfidf_df.div(tfidf_df.sum(axis = 1), axis = 0)

    # Selecionando as top 100 palavras para cada classe
    top_words_by_class = {}
    for label in tfidf_normalized.index:
        top_words_by_class[label] = tfidf_normalized.loc[label].nlargest(N_WORDS).index.tolist()

    # Quantidade de documentos que temos
    print(f"Quantidade de documentos: {len(cluster_documents)}")

    # Gera as nuvens de palavras pra cada classe
    for label, words in top_words_by_class.items():
        generate_wordcloud(words, f"Cluster - {label}")

