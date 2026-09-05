import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import psutil
import cv2
import numpy as np
from nirikshak_ocr.service import OCRService

print("=== MEMORY & CONCURRENCY AUDIT ===")

process = psutil.Process(os.getpid())

def get_mem_mb():
    return process.memory_info().rss / (1024 * 1024)

mem_initial = get_mem_mb()
print(f"Memory Initial:             {mem_initial:.2f} MB")

# Initialize Service
service = OCRService()
mem_after_init = get_mem_mb()
print(f"Memory After Service Init:  {mem_after_init:.2f} MB (Delta: +{mem_after_init - mem_initial:.2f} MB)")

# Warmup pass
service.warmup()
mem_after_warmup = get_mem_mb()
print(f"Memory After Warmup:        {mem_after_warmup:.2f} MB (Delta: +{mem_after_warmup - mem_after_init:.2f} MB)")

# Load sample image
img = cv2.imread("data/synthetic/regression/SYNTH-01-ENG-FMCG.png")

# Run 40 repeated inferences to audit memory growth
print("Running 40 repeated inference cycles...")
latencies = []
for i in range(40):
    t0 = time.perf_counter()
    res = service.extract(img, image_id=f"mem_test_{i}")
    latencies.append((time.perf_counter() - t0) * 1000.0)

mem_final = get_mem_mb()
print(f"Memory After 40 Calls:      {mem_final:.2f} MB (Delta vs Warmup: {mem_final - mem_after_warmup:+.2f} MB)")
print(f"Latency over 40 calls: Median={np.median(latencies):.2f} ms, P95={np.percentile(latencies, 95):.2f} ms")

# Concurrency Audit: 2, 4, 8 threads
print("\n--- Concurrency Stress Audit ---")
for num_threads in [2, 4, 8]:
    total_calls = num_threads * 5
    print(f"Testing {num_threads} concurrent threads ({total_calls} total tasks)...")
    
    t_start = time.perf_counter()
    errors = []
    token_counts = []
    
    def worker_task(idx):
        try:
            r = service.extract(img, image_id=f"thread_{idx}")
            return len(r.tokens)
        except Exception as e:
            return e

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(worker_task, i) for i in range(total_calls)]
        for f in as_completed(futures):
            res = f.result()
            if isinstance(res, Exception):
                errors.append(res)
            else:
                token_counts.append(res)
                
    t_elapsed = time.perf_counter() - t_start
    print(f"  Threads={num_threads}: Elapsed={t_elapsed:.2f}s | Success={len(token_counts)}/{total_calls} | Errors={len(errors)}")
    assert len(errors) == 0, f"Errors encountered: {errors}"
    assert all(c == token_counts[0] for c in token_counts), "Output token counts inconsistent under concurrency!"
    print(f"  All {total_calls} calls returned identical token count ({token_counts[0]})")

mem_post_concurrency = get_mem_mb()
print(f"\nFinal Memory Post Concurrency: {mem_post_concurrency:.2f} MB")
print("=== MEMORY & CONCURRENCY AUDITS COMPLETE ===")
