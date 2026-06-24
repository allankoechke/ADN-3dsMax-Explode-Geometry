"""
Benchmarking runner for Explode Geometry logging variants.

Run inside 3ds Max Python listener:
    exec(open(r"<repo_path>/perf/runner.py").read())

Creates a standard test cone and measures wall-clock time for each variant's
convert_to_triangle_faces() and convert_to_mnmesh_faces() functions.
"""

import importlib
import os
import sys
import time

import pymxs

rt = pymxs.runtime

PERF_DIR = os.path.dirname(os.path.abspath(__file__))
if PERF_DIR not in sys.path:
    sys.path.insert(0, PERF_DIR)

VARIANTS = [
    ("print", "explode_geometry_print"),
    ("errors_only", "explode_geometry_errors_only"),
    ("logger_all", "explode_geometry_logger_all"),
    ("logger_info", "explode_geometry_logger_info"),
    ("noprint", "explode_geometry_noprint"),
    ("devnull", "explode_geometry_devnull"),
]

CONE_PARAMS = dict(radius1=300, radius2=0, height=500, heightsegs=100, capsegs=50, sides=64)


def create_test_cone():
    return rt.Cone(**CONE_PARAMS)


def run_benchmark(variant_module, func_name):
    rt.resetMaxFile(rt.Name("noPrompt"))
    cone = create_test_cone()
    rt.select(cone)

    func = getattr(variant_module, func_name)

    start = time.perf_counter()
    func(cone)
    elapsed = time.perf_counter() - start

    return elapsed


def main():
    results = []

    for variant_name, module_name in VARIANTS:
        mod = importlib.import_module(module_name)
        importlib.reload(mod)

        for func_name, explode_type in [
            ("convert_to_triangle_faces", "TriMesh"),
            ("convert_to_mnmesh_faces", "MNMesh"),
        ]:
            elapsed = run_benchmark(mod, func_name)
            results.append((variant_name, explode_type, elapsed))

        if hasattr(mod, "restore_stdout"):
            mod.restore_stdout()

    rt.resetMaxFile(rt.Name("noPrompt"))

    # Reset stdout and stderr to ensure benchmark results are printed to the console
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    pymxs.print_("\n## Benchmark Results\n")
    pymxs.print_("Test mesh: Cone(radius1={radius1}, radius2={radius2}, height={height}, "
          "heightsegs={heightsegs}, capsegs={capsegs}, sides={sides})\n".format(**CONE_PARAMS))
    pymxs.print_("\n")
    pymxs.print_("| {:<14s} | {:<11s} | {}   |\n".format("Variant", "Explode Type", "Time (s)"))
    pymxs.print_("|-------------|-------------|----------|\n")
    for variant_name, explode_type, elapsed in results:
        pymxs.print_("| {:<14s} | {:<11s} | {:.4f}   |\n".format(variant_name, explode_type, elapsed))
    pymxs.print_("\n")


if __name__ == "__main__":
    main()
else:
    main()
