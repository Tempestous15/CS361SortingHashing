# ----------------------------------------------------------
# File:          test_merge_sort.py
# Description:   Three way merge sort benchmark, sizes 2²⁰–2³⁰, integers vs floats, exclude I/O time
# Author:        Rick Garcia
# Email:         rickwgarcia@unm.edu
# Date:          2026-04-02
# ----------------------------------------------------------

import time
import random
from three_way_merge import merge_sort

print(f"{'Size':>12}  {'Int (s)':>10}  {'Float (s)':>10}")
print("-" * 38)

for exp in range(20, 31):
    n = 2 ** exp

    int_data   = [random.randint(0, n) for _ in range(n)]
    float_data = [random.uniform(0.0, float(n)) for _ in range(n)]

    # Integers
    arr = int_data[:]
    t0 = time.perf_counter()
    merge_sort(arr, 0, n - 1)
    int_time = time.perf_counter() - t0

    # Floats
    arr = float_data[:]
    t0 = time.perf_counter()
    merge_sort(arr, 0, n - 1)
    float_time = time.perf_counter() - t0

    print(f"{n:>12,}  {int_time:>10.4f}  {float_time:>10.4f}")
