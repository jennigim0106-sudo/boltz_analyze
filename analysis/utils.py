import os
from analysis.interactions import extract_interactions
from analysis.plot_plddt import plot_plddt
from analysis.plot_pae import plot_pae
from analysis.io import find_model_file


def analyze_single_model(
    extract_dir: str,
    model_num: int,
    result_dir: str,
    pymol_cmd
):

    # 3-0. Find files
    pdb_path = find_model_file(
        extract_dir,
        pattern=rf".*_model_{model_num}\.pdb$"
    )

    plddt_npz = find_model_file(
        extract_dir,
        pattern=rf"plddt_.*_model_{model_num}\.npz$"
    )

    pae_npz = find_model_file(
        extract_dir,
        pattern=rf"pae_.*_model_{model_num}\.npz$"
    )

    model_outdir = os.path.join(result_dir, f"model_{model_num}")
    os.makedirs(model_outdir, exist_ok=True)

    # 3-1. Interaction analysis (PyMOL)
    interaction_csv = extract_interactions(
        cmd=pymol_cmd,
        pdb_path=pdb_path,
        out_dir=model_outdir,
        model_num=model_num,
    )

    # 3-2. pLDDT plot
    plddt_png = plot_plddt(
        npz_path=plddt_npz,
        out_dir=model_outdir,
        model_num=model_num,
    )

    # 3-3. PAE plot
    pae_png = plot_pae(
        npz_path=pae_npz,
        out_dir=model_outdir,
        model_num=model_num,
    )

    return {
        "model_num": model_num,
        "pdb_path": pdb_path,
        "interaction_csv": interaction_csv,
        "plddt_plot": plddt_png,
        "pae_plot": pae_png,
    }
