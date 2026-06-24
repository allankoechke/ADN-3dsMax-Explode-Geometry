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
Test mesh: Cone(radius1=300, radius2=0, height=500, heightsegs=100, capsegs=50, sides=64)

### Round I
| Variant        | Explode Type | Time (s)   |
|-------------|-------------|----------|
| print          | TriMesh     | 1015.5132   |
| print          | MNMesh      | 513.8827   |
| errors_only    | TriMesh     | 10.3010   |
| errors_only    | MNMesh      | 70.2645   |
| logger_all     | TriMesh     | 958.9389   |
| logger_all     | MNMesh      | 493.1808   |
| logger_info    | TriMesh     | 11.9884   |
| logger_info    | MNMesh      | 73.9633   |
| noprint        | TriMesh     | 10.4835   |
| noprint        | MNMesh      | 73.6788   |
| devnull        | TriMesh     | 13.6254   |
| devnull        | MNMesh      | 74.8291   |

### Round II

| Variant        | Explode Type | Time (s)   |
|-------------|-------------|----------|
| print          | TriMesh     | 1077.8989   |
| print          | MNMesh      | 559.9293   |
| errors_only    | TriMesh     | 12.5386   |
| errors_only    | MNMesh      | 83.7304   |
| logger_all     | TriMesh     | 1004.9832   |
| logger_all     | MNMesh      | 530.6878   |
| logger_info    | TriMesh     | 14.7921   |
| logger_info    | MNMesh      | 91.1383   |
| noprint        | TriMesh     | 14.0522   |
| noprint        | MNMesh      | 88.8824   |
| devnull        | TriMesh     | 16.0924   |
| devnull        | MNMesh      | 92.7313   |


## Analysis

_Fill in after collecting results:_

- **Expected**: `logger_info` and `noprint` should be measurably faster than `print` baseline
- **Key metric**: Speedup ratio of `logger_info` vs `print` for TriMesh path (the per-face hotspot)
