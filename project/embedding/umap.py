from umap import UMAP
import numpy as np

def umap_reduce_dim(embeddings, n_dimensions):
    umap_2d = UMAP(n_components = n_dimensions)

    low_dim_embeddings = umap_2d.fit_transform(embeddings)

    print(f"Dimensão do embedding original: {embeddings.shape[1]}")
    print(f"Dimensão do embedding depois de aplicar o UMAP: {np.array(low_dim_embeddings).ndim}")

    return low_dim_embeddings