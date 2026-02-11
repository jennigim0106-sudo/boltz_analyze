import numpy as np
import matplotlib.pyplot as plt
import os


def plot_pae(npz_path, out_dir, model_num):
    data = np.load(npz_path)
    pae = data["pae"]

    fig, ax = plt.subplots(figsize=(5, 5))

    im = ax.imshow(pae, cmap="viridis", origin="upper")
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("PAE (Å)")

    # === 축 위치 조정 ===
    ax.xaxis.set_label_position("top")
    ax.xaxis.tick_top()

    ax.yaxis.set_label_position("left")
    ax.yaxis.tick_left()

    ax.set_xlabel("Residue index")
    ax.set_ylabel("Residue index")

    plt.tight_layout()

    out_png = os.path.join(out_dir, f"model_{model_num}_pae.png")
    plt.savefig(out_png, dpi=200)
    plt.close()

    return out_png
