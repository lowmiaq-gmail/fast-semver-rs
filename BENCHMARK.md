# Benchmark Evidence

Local exact-artifact evidence on macOS arm64, Python 3.14. The immutable release workflow reruns and attaches raw samples; these values are not universal claims.

| Workload | Median speedup | Output |
|---|---:|---|
| Parse 20,000 versions | 1.72x | identical SHA256 |
| Compare 20,000 versions | 1.32x | identical SHA256 |
| Match 20,000 versions | 1.40x | identical SHA256 |
| Google OSV normalize | 1.21x | identical SHA256 |
| Google OSV sort | 1.15x | identical SHA256 |

The microbenchmark used 15 alternating Oracle/Candidate pairs. The frozen Google OSV `semver_index` consumer used 12 alternating pairs and its applicable unit suite passed three tests for both implementations. Raw local JSON is intentionally not committed because the release workflow attaches evidence tied to the exact release artifact and source commit.
