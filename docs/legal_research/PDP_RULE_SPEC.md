# Principal Display Panel (PDP) Rule Specification

**Source:** Rule 7
**Definition:** 
- Rectangular package: Entire one side (H x W).
- Cylindrical package: 40% of height x circumference.
- Other shapes: 40% of total surface area.

**Engineering Reality:** 
- A 2D image cannot fully determine 3D capacity or unseen surface area. 
- MetroLens will use visible bounding box area as a heuristic proxy for PDP size to index into the Font Height table, but this is an ENGINEERING INFERENCE.
