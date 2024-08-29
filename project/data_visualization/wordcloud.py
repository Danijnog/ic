from wordcloud import WordCloud, STOPWORDS
import os
import pandas as pd
import matplotlib.pyplot as plt

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

def word_cloud(df):
    """Retorna um objeto WordCloud gerado a partir das mensagens no DataFrame passado como parâmetro da função."""
    messages = df['message']
    messages_string = " ".join(s for s in messages)

    # Stopwords
    stopwords = set(STOPWORDS)
    stop_words = ["da", "meu", "que", "de", "os", "é",  "e", "o", "para",
                    "mesmo", "só", "aqui", "agora", "todo", "deu", "isso",
                    "todos", "ou", "ma", "mai", "mas", "sim", "ele", "mais",
                    "tudo", "se", "tem", "até", "não", "você", "aí", "já", "q",
                    "vc", "pq", "assim", "foi", "já", "pois", "cara", "em", "como",
                    "depois", "esse", "por", "está", "eles", "ela", "pra", "conversa",
                    "aborda", "um", "à", "Há", "na", "uma", "sobre", "Brasil", "Brasília",
                    "contra", "necessidade", "entre", "além", "Também", "também", "grupo",
                    "discute", "ao", "política", "menciona", "crítica", "críticas", "governo",
                    "ações", "atual", "protesto", "Discussão", "situação", "dos", "Bolsonaro",
                    "Lula", "após", "apoio", "manifestações"]
    
    stopwords.update(stop_words)
    wordcloud = WordCloud(stopwords = stopwords, background_color = 'black', max_words = 100,
                          width = 1600, height = 800).generate(messages_string)
    
    return wordcloud

def plot_wordcloud(wordcloud):
    """Plota o gráfico do objeto WordCloud, gerando a nuvem de palavras."""
    fig, ax = plt.subplots(figsize = (10, 6))
    ax.imshow(wordcloud)
    ax.set_axis_off()

    plt.savefig('wordcloud.png')

def get_wordcloud_for_cluster(df, cluster):
    df_copy = df.copy()
    df_copy = df_copy.rename(columns = {'label': 'message'})

    df_copy['clusters'] = df_copy['clusters'].astype(int)
    df_copy = df_copy[df_copy['clusters'].isin([cluster])]

    wordcloud = word_cloud(df_copy)

    return wordcloud

