import os
import zipfile
import pandas as pd
import json
import re

def extract_zip(zip_path, out_root):
    extract_dir = os.path.join(out_root, "extracted")
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_dir)

    return extract_dir

def find_model_file(
    extract_dir: str,
    pattern: str,
) -> str:

    regex = re.compile(pattern)

    for root, _, files in os.walk(extract_dir):
        for f in files:
            if regex.match(f):
                return os.path.join(root, f)

    raise FileNotFoundError(
        f"No file matching pattern '{pattern}' found in {extract_dir}"
    )


def find_affinity_json_path(extract_dir: str) -> str:
    for root, _, files in os.walk(extract_dir):
        for f in files:
            if f.startswith("affinity") and f.endswith(".json"):
                return os.path.join(root, f)

    raise FileNotFoundError("affinity*.json not found in Boltz zip")


def parse_affinity_json(extract_dir: str):
    for root, _, files in os.walk(extract_dir):
        for f in files:
            if f.startswith("affinity") and f.endswith(".json"):
                json_path = os.path.join(root, f)
                with open(json_path, "r") as r:
                    affinity_result = json.load(r)
                return affinity_result

def parse_confidence_json(extract_dir: str) -> pd.DataFrame:
    records = []

    for root, _, files in os.walk(extract_dir):
        for f in files:
            if not (f.startswith("confidence") and f.endswith(".json")):
                continue

            # get model_num
            m = re.search(r"_model_(\d+)\.json$", f)
            if m is None:
                continue  # 형식 안 맞으면 스킵

            model_num = int(m.group(1))
            json_path = os.path.join(root, f)

            with open(json_path, "r") as r:
                conf = json.load(r)

            # Record dictionary for each model
            record = {
                "model_num": model_num,
                "confidence_score": conf.get("confidence_score"),
                "ptm": conf.get("ptm"),
                "iptm": conf.get("iptm"),
                "ligand_iptm": conf.get("ligand_iptm"),
                "protein_iptm": conf.get("protein_iptm"),
                "complex_plddt": conf.get("complex_plddt"),
                "complex_iplddt": conf.get("complex_iplddt"),
                "complex_pde": conf.get("complex_pde"),
                "complex_ipde": conf.get("complex_ipde"),
            }

            records.append(record)

    if not records:
        raise FileNotFoundError("No confidence_*.json files found in Boltz zip")

    df = pd.DataFrame(records)
    df = df.sort_values("model_num").reset_index(drop=True)

    return df