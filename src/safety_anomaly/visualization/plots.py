"""Generate figures for reports and the Streamlit dashboard."""
from __future__ import annotations
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA


def create_pca_projection(X: np.ndarray, n_components: int = 3, random_state: int = 42):
    n_components = min(int(n_components), X.shape[0] - 1, X.shape[1])
    if n_components < 2:
        raise ValueError("PCA requires at least two usable dimensions and three observations.")
    pca = PCA(n_components=n_components, random_state=random_state)
    coords = pca.fit_transform(X)
    columns = [f"PC{i+1}" for i in range(n_components)]
    return pd.DataFrame(coords, columns=columns), pca.explained_variance_ratio_


def save_pca_figure(coords: pd.DataFrame, labels, path: str | Path, title: str):
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    y = np.asarray(labels) == -1
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(coords.loc[~y, "PC1"], coords.loc[~y, "PC2"], s=12, alpha=0.35, label="Inlier")
    ax.scatter(coords.loc[y, "PC1"], coords.loc[y, "PC2"], s=18, alpha=0.8, label="Anomaly")
    ax.set(title=title, xlabel="Principal component 1", ylabel="Principal component 2")
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(output, dpi=160, bbox_inches="tight")
    plt.close(fig)


def save_missingness_figure(frame: pd.DataFrame, path: str | Path, top_n: int = 15):
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    missing = (frame.isna().mean() * 100).sort_values(ascending=False).head(top_n).sort_values()
    fig, ax = plt.subplots(figsize=(9, max(4, len(missing) * 0.3)))
    missing.plot(kind="barh", ax=ax)
    ax.set_xlabel("Missing values (%)")
    ax.set_ylabel("Column")
    ax.set_title("Columns with the highest missingness")
    fig.tight_layout()
    fig.savefig(output, dpi=160, bbox_inches="tight")
    plt.close(fig)
