1. Environment Setup
    * conda env create -f environment.yml
    ( conda activate boltz_analysis

2. Run App: 
    streamlit run main.py

3. Required Input
    * Colab Boltz prediction .zip file
    * must contain:
        - *_model_X.pdb
        - plddt_*_model_X.npz
        - pae_*_model_X.npz
        - confidence_model_X.json
        - affinity.json

4. Output
    For each selected model:
        * interaction CSV
        * pLDDT plot
        * PAE heatmap
