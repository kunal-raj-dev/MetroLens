
import os
from nirikshak_ocr.config import OCRConfig
cfg = OCRConfig().resolve_paths()
print("det exists:", os.path.isfile(cfg.det_model_path), "path:", cfg.det_model_path)
