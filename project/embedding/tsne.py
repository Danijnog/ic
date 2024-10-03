from sklearn.manifold import TSNE
import numpy as np

def tsne_reduce_dim(embeddings, summaries):
    perplexity = 20
    tsne = TSNE(n_components = 2, perplexity = perplexity)
    low_dim_embeddings = tsne.fit_transform(embeddings)

    print(f"Dimensão do embedding original: {embeddings.shape[1]}")
    print(f"Dimensão do embedding depois de aplicar o t-SNE: {np.array(low_dim_embeddings).ndim}")

    return low_dim_embeddings
