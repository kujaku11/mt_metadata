#!/usr/bin/env python3
"""
Script to test phases validation multiple times to check for inconsistencies
"""
import sys
import threading
import time

import numpy as np

from mt_metadata.timeseries.filters import FrequencyResponseTableFilter


def test_single_run(run_id="test"):
    """Test phases validation in a single run"""
    try:
        fap = FrequencyResponseTableFilter(
            frequencies=np.array([0.001, 0.01, 0.1, 1.0, 10.0]),
            amplitudes=np.array([1e-3, 1e-2, 1e-1, 1.0, 10.0]),
            phases=np.array([-90, -45, 0, 45, 90]),
            instrument_type="example_instrument",
            units_in="Volt",
            units_out="nanoTesla",
            name="example_fap",
        )

        # Try to set invalid phases
        try:
            fap.phases = "invalid"
            return f"Run {run_id}: FAIL - No exception raised"
        except TypeError as e:
            return f"Run {run_id}: PASS - TypeError raised: {str(e)[:50]}..."
        except Exception as e:
            return f"Run {run_id}: FAIL - Wrong exception: {type(e).__name__}: {str(e)[:50]}..."

    except Exception as e:
        return f"Run {run_id}: ERROR - Failed to create filter: {type(e).__name__}: {e}"


def test_sequential_runs(num_runs=20):
    """Test multiple sequential runs"""
    print(f"Running {num_runs} sequential tests...")
    results = []
    for i in range(num_runs):
        result = test_single_run(i + 1)
        results.append(result)
        print(result)
        time.sleep(0.01)  # Small delay

    passes = sum(1 for r in results if "PASS" in r)
    print(f"\nSequential results: {passes}/{num_runs} passed")
    return passes == num_runs


def test_concurrent_runs(num_threads=10):
    """Test multiple concurrent runs"""
    print(f"\nRunning {num_threads} concurrent tests...")
    results = []
    threads = []

    def worker(thread_id):
        result = test_single_run(f"T{thread_id}")
        results.append(result)
        print(result)

    # Start all threads
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i + 1,))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    passes = sum(1 for r in results if "PASS" in r)
    print(f"\nConcurrent results: {passes}/{num_threads} passed")
    return passes == num_threads


if __name__ == "__main__":
    print("Testing phases validation consistency...")

    # Test sequential runs
    sequential_success = test_sequential_runs()

    # Test concurrent runs
    concurrent_success = test_concurrent_runs()

    if sequential_success and concurrent_success:
        print("\n✓ All tests passed - validation appears consistent")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed - validation appears inconsistent")
        sys.exit(1)
