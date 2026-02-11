from analysis.io import extract_zip, parse_confidence_json, parse_affinity_json
import tempfile
import os
import shutil

boltz_zip = "/Users/gimjimin/Desktop/2026_intern/10_BoltzColab runs (2026.02.04)/Boltz run results/6njs_run1.zip"

tmpdir = tempfile.mkdtemp()

# zip 파일을 tmpdir로 복사
zip_path = os.path.join(tmpdir, os.path.basename(boltz_zip))
shutil.copy(boltz_zip, zip_path)

extract_dir = extract_zip(zip_path, tmpdir)

affinity = parse_affinity_json(extract_dir)
df = parse_confidence_json(extract_dir)

print(affinity)
print(df)