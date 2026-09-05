import os
import subprocess
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[4]
dirs_to_test = [root, root / "apps" / "api", root / "tests"]

helper_script = root / "AI_CONTEXT" / "EXPERIMENTS" / "MEMBER_1_PHASE_B_AUDIT" / "04_MODEL_AUDIT" / "check_model_exists.py"
helper_script.write_text("""
import os
from nirikshak_ocr.config import OCRConfig
cfg = OCRConfig().resolve_paths()
print("det exists:", os.path.isfile(cfg.det_model_path), "path:", cfg.det_model_path)
""", encoding="utf-8")

for d in dirs_to_test:
    res = subprocess.run(["python", str(helper_script)], cwd=str(d), capture_output=True, text=True)
    label = "." if d == root else str(d.relative_to(root))
    print(f"CWD: {label:15} -> exit={res.returncode}, out={res.stdout.strip()}, err={res.stderr.strip()}")

with tempfile.TemporaryDirectory() as tmpdir:
    env = os.environ.copy()
    env["METROLENS_ROOT"] = str(root)
    res = subprocess.run(["python", str(helper_script)], cwd=tmpdir, env=env, capture_output=True, text=True)
    print(f"CWD: TempDir WITH METROLENS_ROOT -> exit={res.returncode}, out={res.stdout.strip()}")

with tempfile.TemporaryDirectory() as tmpdir:
    env = os.environ.copy()
    env.pop("METROLENS_ROOT", None)
    env.pop("METROLENS_MODELS_DIR", None)
    res = subprocess.run(["python", str(helper_script)], cwd=tmpdir, env=env, capture_output=True, text=True)
    print(f"CWD: TempDir WITHOUT METROLENS_ROOT -> exit={res.returncode}, out={res.stdout.strip()}")
