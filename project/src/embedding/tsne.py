import numpy as np
from sklearn.manifold import TSNE


def tsne_reduce_dim(embeddings) -> np.ndarray:
    """
    Reduces the dimensionality of embedding vectors using t-SNE.
    - Note: The t-SNE algorithm is configured with a parameter called 'perplexity' to balance local
    and global data structure representation.
    """
    perplexity = 20
    tsne = TSNE(n_components=2, perplexity=perplexity)
    low_dim_embeddings = tsne.fit_transform(embeddings)

    print(f"Original embedding dimension: {embeddings.shape[1]}")
    print(f"Embedding dimension after t-SNE: {np.array(low_dim_embeddings).ndim}")

    return low_dim_embeddings
