# Dataset & Benchmark Limitations

## Purpose
Documents sample size constraints, geographic biases, and category gaps in planned packaging datasets (as zero physical packaging datasets currently exist on disk).

## Identified Dataset Limitations
1. **Geographic Focus:** The planned physical retail collection pilot (`DS-RETAIL-PILOT-001`, planned target: 50 physical SKUs) will be sourced from national supermarkets in Delhi-NCR, India, and primarily captures major national FMCG brands.
2. **Category Representation:** Planned sampling focuses on dry food cartons, cylindrical cans/bottles, and stand-up pouches; currently excludes bulk agricultural sacks, industrial cement bags, and hazardous chemicals.
3. **Synthetic Domain Shift:** Synthetic procedural packaging layouts (`DS-SYNTH-001`, planned target: 1,000 configurations) provide exact geometric ground truth but lack complex specular glare, scratches, and micro-tears found in real retail field operations.
4. **Physical Absence Warning:** Zero physical image files or measurement logs are committed to disk (`data/raw/` and `data/synthetic/` contain only `.gitkeep`).
