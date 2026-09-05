import os
import re

replacements = [
    (r'(?i)Rule 9 Table 1', r'Rule 7(4) Table'),
    (r'(?i)Rule 9 font table', r'Rule 7(4) font table'),
    (r'(?i)Rule 6\(1\)\(h\) country of origin', r'Rule 6(1)(aa) country of origin'),
    (r'(?i)\bper 100g\b', r'per g or kg'),
    (r'(?i)1%\s*statutory tolerance', r'engineering calculation band'),
    (r'(?i)statutory benefit-of-doubt', r'Measurement Uncertainty Review Band'),
    (r'(?i)0\.10mm statutory', r'0.10mm engineering'),
    (r'(?i)\bForm A\b', r'Inspection Assessment Report'),
    (r'(?i)court-admissible', r'supporting inspection evidence'),
    (r'(?i)prima facie evidentiary', r'supporting inspection evidence'),
    (r'(?i)prima facie', r'supporting'),
    (r'(?i)100% compliant', r'potentially compliant'),
    (r'(?i)statutory certificate', r'Assessment Report'),
    (r'(?i)automatic penalty', r'potential non-compliance flag'),
    (r'(?i)automatic Improvement Notice', r'draft Improvement Notice content'),
    (r'(?i)live eMaap integration', r'offline workflow capability'),
    (r'(?i)official eMaap API', r'eMaap compatible schema'),
    (r'(?i)\bTable II\b', r'Rule 7(4) Table'),
    (r'(?i)zero distortion', r'minimized distortion'),
    (r'(?i)zero error', r'reduced error'),
    (r'(?i)100% deterministic', r'high-confidence deterministic'),
    (r'(?i)100% accuracy', r'high accuracy'),
    (r'(?i)2\.5 seconds', r'[DYNAMIC MEASURED VALUE] seconds'),
    (r'(?i)1\.15 mm', r'[DYNAMIC MEASURED VALUE] mm'),
    (r'(?i)74\.5 cm[2²]', r'[DYNAMIC MEASURED VALUE] cm²'),
    (r'(?i)74\.5', r'[DYNAMIC MEASURED VALUE]')
]

docs_dir = r'C:\Users\kunal\Desktop\MetroLens\docs'
skip_dirs = ['legal_research']

for root, dirs, files in os.walk(docs_dir):
    # skip legal_research since we just built it and intentionally mention terms there to report their removal
    if any(sd in root for sd in skip_dirs):
        continue
    
    for file in files:
        if file.endswith('.md'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            for old, new in replacements:
                new_content = re.sub(old, new, new_content)
                
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Updated {file}')
