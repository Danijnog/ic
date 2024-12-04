import numpy as np
from umap import UMAP


def umap_reduce_dim(embeddings, n_dimensions) -> np.ndarray:
    """
    Reduces the dimensionality of embedding vectors using UMAP.
    - Note: UMAP algorithm is configured with four principal parameters:
      - 'spread', 'min_dist', 'n_neighbors', 'metric'
    Fine-tuning those parameters is the most important part of using the algorithm.
    """
    umap = UMAP(
        n_components=n_dimensions, spread=1.8, min_dist=0.05, n_neighbors=40, 
        metric="cosine", random_state=42
    )

    low_dim_embeddings = umap.fit_transform(embeddings)

    embeddings = np.array(embeddings)
    print(f"Original embedding dimension: {embeddings.shape[1]}")
    print(f"Embedding dimension after UMAP: {low_dim_embeddings.shape[1]}")

    return low_dim_embeddings, umap
