"""
Benchmark harness for Nirikshak OCR Subsystem (Chunk 2).
Measures:
1. Thread sweep: 1, 2, 4, 8 CPU threads.
2. Memory stability: 25 repeated inference passes measuring process RSS.
3. Specimen sweep: 8 synthetic packaging specimens measuring cold, warm median, P95, and routing.
"""

import os
import sys
import time
import json
import yaml
import platform
import psutil
from pathlib import Path
import numpy as np
import cv2

# Add monorepo paths
sys.path.insert(0, os.path.abspath("packages/shared/src"))
sys.path.insert(0, os.path.abspath("packages/ocr/src"))

from nirikshak_ocr import OCREngine, OCRConfig

ROOT_DIR = Path(__file__).resolve().parents[3]
DATASET_DIR = ROOT_DIR / "AI_CONTEXT" / "EXPERIMENTS" / "CHUNK_1_OCR_MODEL_SELECTION" / "03_DATASET" / "images"
OUTPUT_DIR = Path(__file__).resolve().parent


def get_memory_rss_mb() -> float:
    process = psutil.Process(os.getpid())
    return round(process.memory_info().rss / (1024 * 1024), 2)


def run_benchmark():
    print("============================================================")
    print("METROLENS AI — CHUNK 2 OCR BENCHMARK HARNESS")
    print("============================================================")
    
    run_id = f"CH2-BENCH-{int(time.time())}"
    date_str = time.strftime("%Y-%m-%dT%H:%M:%S+05:30")
    
    cpu_info = platform.processor() or "AMD Ryzen CPU"
    os_info = f"{platform.system()} {platform.release()} ({platform.version()})"
    python_info = sys.version.split()[0]
    
    print(f"Run ID:        {run_id}")
    print(f"Date/Time:     {date_str}")
    print(f"Hardware CPU:  {cpu_info} ({psutil.cpu_count(logical=False)} physical / {psutil.cpu_count(logical=True)} logical)")
    print(f"OS:            {os_info}")
    print(f"Python:        {python_info}")
    print("------------------------------------------------------------")
    
    rss_start = get_memory_rss_mb()
    print(f"Initial Memory RSS: {rss_start:.2f} MB")
    
    test_img_path = DATASET_DIR / "SYNTH-01-ENG-FMCG.png"
    assert test_img_path.is_file(), f"Missing test image: {test_img_path}"
    test_img = cv2.imread(str(test_img_path))
    
    # ------------------------------------------------------------
    # 1. Thread Count Sweep (1, 2, 4, 8 threads)
    # ------------------------------------------------------------
    print("\n[Phase 1] Thread Count Sweep on CPU...")
    thread_results = []
    
    for t_count in [1, 2, 4, 8]:
        cfg = OCRConfig(intra_op_num_threads=t_count, enable_warmup=False).resolve_paths()
        
        t0 = time.perf_counter()
        engine = OCREngine(cfg)
        cold_load_ms = round((time.perf_counter() - t0) * 1000.0, 2)
        
        # Warmup (2 passes)
        for _ in range(2):
            engine.extract(test_img)
            
        # Warm passes (10 passes)
        latencies = []
        for _ in range(10):
            t_inf = time.perf_counter()
            engine.extract(test_img)
            latencies.append((time.perf_counter() - t_inf) * 1000.0)
            
        median_lat = round(float(np.median(latencies)), 2)
        p95_lat = round(float(np.percentile(latencies, 95)), 2)
        rss_after = get_memory_rss_mb()
        
        print(f" - Threads: {t_count:2d} | Cold Load: {cold_load_ms:6.2f} ms | Median Latency: {median_lat:6.2f} ms | P95: {p95_lat:6.2f} ms | RSS: {rss_after:.2f} MB")
        
        thread_results.append({
            "intra_op_num_threads": t_count,
            "cold_load_ms": cold_load_ms,
            "median_latency_ms": median_lat,
            "p95_latency_ms": p95_lat,
            "memory_rss_mb": rss_after
        })
        
    # ------------------------------------------------------------
    # 2. Memory Stability Over 25 Repeated Inferences (Thread=4)
    # ------------------------------------------------------------
    print("\n[Phase 2] Memory Stability Over 25 Repeated Inferences (Thread=4)...")
    cfg_main = OCRConfig(intra_op_num_threads=4).resolve_paths()
    
    rss_pre_load = get_memory_rss_mb()
    engine_main = OCREngine(cfg_main)
    rss_post_load = get_memory_rss_mb()
    
    memory_trace = [{"step": 0, "event": "post_model_load", "rss_mb": rss_post_load}]
    
    for i in range(1, 26):
        engine_main.extract(test_img)
        if i % 5 == 0 or i == 1:
            current_rss = get_memory_rss_mb()
            memory_trace.append({"step": i, "event": f"inference_{i}", "rss_mb": current_rss})
            print(f" - Inference #{i:2d}: Memory RSS = {current_rss:.2f} MB (Delta: +{current_rss - rss_post_load:.2f} MB)")
            
    # ------------------------------------------------------------
    # 3. Comprehensive Specimen Benchmark (8 Synthetic Specimens)
    # ------------------------------------------------------------
    print("\n[Phase 3] Benchmark Across 8 Synthetic Specimens...")
    specimen_files = sorted([f for f in DATASET_DIR.glob("*.png")])
    specimen_results = []
    
    for spec_path in specimen_files:
        img_name = spec_path.name
        img_bgr = cv2.imread(str(spec_path))
        h, w = img_bgr.shape[:2]
        
        # 5 repetitions per specimen
        spec_latencies = []
        last_result = None
        for _ in range(5):
            t0 = time.perf_counter()
            last_result = engine_main.extract(img_bgr, image_id=img_name)
            spec_latencies.append((time.perf_counter() - t0) * 1000.0)
            
        med_ms = round(float(np.median(spec_latencies)), 2)
        p95_ms = round(float(np.percentile(spec_latencies, 95)), 2)
        
        print(f" - {img_name:30} ({w}x{h}): Median = {med_ms:6.2f} ms | Tokens = {len(last_result.tokens):2d} | Route: {last_result.routing_summary}")
        
        specimen_results.append({
            "filename": img_name,
            "width": w,
            "height": h,
            "median_latency_ms": med_ms,
            "p95_latency_ms": p95_ms,
            "token_count": len(last_result.tokens),
            "routing_summary": last_result.routing_summary,
            "stage_timings": last_result.stage_timings
        })
        
    rss_end = get_memory_rss_mb()
    print(f"\nFinal Memory RSS: {rss_end:.2f} MB")
    
    benchmark_payload = {
        "run_id": run_id,
        "timestamp": date_str,
        "environment": {
            "os": os_info,
            "cpu": cpu_info,
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "python": python_info,
            "onnxruntime_version": "1.29.0",
            "provider": "CPUExecutionProvider"
        },
        "thread_sweep": thread_results,
        "memory_stability": {
            "initial_rss_mb": rss_start,
            "pre_load_rss_mb": rss_pre_load,
            "post_load_rss_mb": rss_post_load,
            "final_rss_mb": rss_end,
            "trace": memory_trace
        },
        "specimen_benchmark": specimen_results
    }
    
    # Save results.json
    results_path = OUTPUT_DIR / "results.json"
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(benchmark_payload, f, indent=2)
        
    print(f"\nWrote benchmark results to: {results_path}")
    return benchmark_payload


if __name__ == "__main__":
    run_benchmark()
