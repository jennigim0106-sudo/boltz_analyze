import numpy as np
import matplotlib.pyplot as plt
import os


def plot_plddt(npz_path, out_dir, model_num):
    data = np.load(npz_path)
    plddt = data["plddt"]

    plt.figure(figsize=(8, 3))
    plt.plot(plddt)
    plt.xlabel("Residue index")
    plt.ylabel("pLDDT")
    plt.tight_layout()

    out_png = os.path.join(out_dir, f"model_{model_num}_plddt.png")
    plt.savefig(out_png, dpi=200)
    plt.close()

    return out_png
