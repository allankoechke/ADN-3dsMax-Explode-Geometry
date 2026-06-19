# Explode Geometry — Logging Performance Benchmark Results

> **Status:** Awaiting manual execution inside 3ds Max

## Test Environment

| Parameter | Value |
|-----------|-------|
| 3ds Max Version | _TODO: fill in after running_ |
| Python Version | _TODO: fill in after running_ |
| OS | Windows 11 |
| Test Mesh | Cone (radius1=50, radius2=0, height=100, heightsegs=10, capsegs=5, sides=32) |

## How to Run

1. Open 3ds Max
2. Open the Python listener (MaxScript > Python Listener)
3. Execute:
   ```python
   exec(open(r"<repo_path>/perf/runner.py").read())
   ```
4. Copy the timing table from the Listener output below

## Results

_Paste the output of `runner.py` here after executing inside 3ds Max._

| Variant | Explode Type | Time (s) |
|---------|-------------|----------|
| print (baseline) | TriMesh | — |
| print (baseline) | MNMesh | — |
| errors_only | TriMesh | — |
| errors_only | MNMesh | — |
| devnull | TriMesh | — |
| devnull | MNMesh | — |
| logger_all (DEBUG) | TriMesh | — |
| logger_all (DEBUG) | MNMesh | — |
| logger_info (INFO) | TriMesh | — |
| logger_info (INFO) | MNMesh | — |
| noprint | TriMesh | — |
| noprint | MNMesh | — |

## Analysis

_Fill in after collecting results:_

- **Expected**: `logger_info` and `noprint` should be measurably faster than `print` baseline
- **Key metric**: Speedup ratio of `logger_info` vs `print` for TriMesh path (the per-face hotspot)
