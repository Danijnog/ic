from sklearn.manifold import TSNE
import numpy as np

from summarization.summarization import clear_messages, truncate_text_tokens_decode, num_tokens_from_string

def tsne_reduce_dim(embeddings, summaries):
    perplexity = min(5, len(summaries) - 1)  # Definindo perplexidade como 3 ou n_samples-1, o que for menor
    tsne = TSNE(n_components = 2, perplexity = perplexity)
    low_dim_embeddings = tsne.fit_transform(embeddings)

    print(f"Dimensão do embedding original: {embeddings.shape[1]}")
    print(f"Dimensão do embedding depois de aplicar o t-SNE: {np.array(low_dim_embeddings).ndim}")

    return low_dim_embeddings
