import streamlit as st
import pymol2
import os
import tempfile
import pandas as pd

from analysis.io import extract_zip, parse_affinity_json, parse_confidence_json, find_affinity_json_path
from analysis.utils import analyze_single_model


#0. Title
st.title("Analyze Boltz Results")


# 1. Model uploads
boltz_zip = st.file_uploader(
    "Upload Boltz prediction result (.zip)",
    type=["zip"],
    accept_multiple_files=False
)


# 2. Show results (for all models)

model_selection = None

if boltz_zip is not None:

    if "boltz_tmpdir" not in st.session_state:
        st.session_state["boltz_tmpdir"] = tempfile.mkdtemp()

    tmpdir = st.session_state["boltz_tmpdir"]

    zip_path = os.path.join(tmpdir, boltz_zip.name)
    with open(zip_path, "wb") as f:
        f.write(boltz_zip.read())

    extract_dir = extract_zip(zip_path, tmpdir)

    # 2-1. Show affinity results (optional: download original json file)

    st.subheader("Ensemble Model Analysis")

    affinity_result = parse_affinity_json(extract_dir)
    for key, value in affinity_result.items():
        st.write(f"{key}: {round(value, 3)}")

    affinity_json_path = find_affinity_json_path(extract_dir)

    with open(affinity_json_path, "rb") as f:
        st.download_button(
            label="Download affinity.json",
            data=f,
            file_name=os.path.basename(affinity_json_path),
            mime="application/json",
        )

    # 2-2. Show confidence matrix & select models
    df = parse_confidence_json(extract_dir)

    st.subheader("Confidence matrix (click and select models to analyze further)")

    df["select"] = False

    checkbox_df = st.data_editor(
        df,
        hide_index=True,
        column_config={
            "select": st.column_config.CheckboxColumn(
                "Select",
                help="Click to include/exclude this pose"
            )
        },
        use_container_width=True
    )

    selected = checkbox_df.loc[checkbox_df["select"], "model_num"].tolist()
    
    st.session_state["boltz"] = {
        "tmpdir": tmpdir,
        "extract_dir": extract_dir,
        "zip_path": zip_path,
        "selected_models": selected
    }


# 3. Run Analysis button

if st.button("Run Analysis"):

    boltz = st.session_state["boltz"]
    extract_dir = boltz["extract_dir"]
    selected_models = boltz["selected_models"]

    if not selected_models:
        st.error("Please select at least one model")
        st.stop()

    results = []

    with pymol2.PyMOL() as pymol:

        cmd = pymol.cmd

        for model_num in selected_models:
            result = analyze_single_model(
                extract_dir=extract_dir,
                model_num=model_num,
                result_dir="./results",
                pymol_cmd=cmd
            )
            results.append(result)

    st.session_state["analysis_results"] = results    


# 4. Representing Results

results = st.session_state.get("analysis_results")

if results:
    st.subheader("Interaction Results")

    for single_result in results:

        model_num = single_result['model_num']
        csv_path = single_result['interaction_csv']
        plddt_path = single_result['plddt_plot']
        pae_path = single_result['pae_plot']

        st.markdown(f"### Results | model_{model_num}")

        # 4-1. Interaction CSV table
        if csv_path and os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            st.dataframe(df)

            with open(csv_path, "rb") as f:
                st.download_button(
                    label=f"Download model_{model_num} interactions",
                    data=f,
                    file_name=os.path.basename(csv_path),
                    mime="text/csv",
                )
        else:
            st.warning(f"Interaction CSV not found: {csv_path}")

        # 4-2. pLDDT plot and download
        if plddt_path and os.path.exists(plddt_path):
            st.markdown("**pLDDT per residue**")
            st.image(plddt_path, use_column_width=True)

            with open(plddt_path, "rb") as f:
                st.download_button(
                    label=f"Download model_{model_num} pLDDT plot",
                    data=f,
                    file_name=os.path.basename(plddt_path),
                    mime="image/png",
                )
        else:
            st.warning(f"pLDDT plot not found: {plddt_path}")

            
        # 4-3. PAE plot and download
        if pae_path and os.path.exists(pae_path):
            st.markdown("**PAE heatmap**")
            st.image(pae_path, use_column_width=True)

            with open(pae_path, "rb") as f:
                st.download_button(
                    label=f"Download model_{model_num} PAE plot",
                    data=f,
                    file_name=os.path.basename(pae_path),
                    mime="image/png",
                )
        else:
            st.warning(f"PAE plot not found: {pae_path}")        