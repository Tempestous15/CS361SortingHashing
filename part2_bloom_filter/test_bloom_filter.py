import time

def test_k_indices(bf, test_items):
    """
    Tests if the Bloom filter generates exactly 'k' indices 
    and ensures they are within the bounds of the bit array.
    """
    expected_k = bf.hash_count
    print(f"\n--- Testing Hash Indices ---")
    print(f"Expected number of indices (k): {expected_k}")
    print(f"Bit array size (m): {bf.size}")

    all_passed = True

    for item in test_items:
        # Get the indices for the test item
        indices = bf.get_hash_indices(item)
        actual_k = len(indices)
        
        # 1. Test if it returns exactly k indices
        is_correct_length = (actual_k == expected_k)
        
        # 2. Test if all indices are within bounds (0 to size - 1)
        are_in_bounds = all(0 <= idx < bf.size for idx in indices)
        
        print(f"Item: '{item}'")
        print(f"  Returned {actual_k} indices: {'PASS' if is_correct_length else 'FAIL'}")
        print(f"  All indices in bounds: {'PASS' if are_in_bounds else 'FAIL'}")
        
        # If you want to see the actual indices, uncomment the next line:
        # print(f"  Indices: {indices}") 
        
        if not is_correct_length or not are_in_bounds:
            all_passed = False
            
    if all_passed:
        print("SUCCESS: The Bloom filter correctly returns 'k' valid indices!")
    else:
        print("FAILURE: Check your index generation logic.")
    print("-" * 30)

def test_determinism(bf, test_items, num_trials=5):
    """
    Tests if the Bloom filter generates the exact same indices 
    for the exact same input across multiple calls.
    """
    print(f"\n--- Testing Hash Determinism ---")
    print(f"Number of trials per item: {num_trials}")

    all_passed = True

    for item in test_items:
        # 1. Get the baseline indices from the first run
        baseline_indices = bf.get_hash_indices(item)
        is_deterministic = True
        
        # 2. Run it several more times to ensure it matches the baseline
        for _ in range(num_trials - 1):
            current_indices = bf.get_hash_indices(item)
            
            # If the lists don't match exactly in content and order, it fails
            if current_indices != baseline_indices:
                is_deterministic = False
                break
        
        print(f"Item: '{item}'")
        print(f"  Consistent indices across {num_trials} runs: {'PASS' if is_deterministic else 'FAIL'}")
        
        if not is_deterministic:
            all_passed = False   

    if all_passed:
        print("SUCCESS: The hash function is perfectly deterministic!")
    else:
        print("FAILURE: The hash function returned different indices for the same input.")
    print("-" * 30)

def test_false_positive_rate(bf, num_checks=100000):
    print(f"\n--- Testing Hash False Positive Rate ---")
    false_positives = 0
    print(f"Checking {num_checks} random strings against the password filter...")
    
    for i in range(num_checks):
        # Create a string that is highly unlikely to be in the password list
        unseen_item = f"random_test_hash_{i}_xyz"
        if bf.check(unseen_item):
            false_positives += 1
            
    actual_error_rate = (false_positives / num_checks)
    print(f"Actual False Positive Rate: {actual_error_rate * 100:.4f}%")
    print("-" * 30)


def test_query_time(bf, test_items):
        """
        Tests how long it takes to check 'n' items in the Bloom filter
        and calculates the average time per query.
        
        :param test_items: The number items to check.
        """
        print(f"\n--- Testing Query Time ---")
        print(f"Testing {len(test_items)} queries...")
        
        # Start performance counter
        start_time = time.perf_counter()
        
        for item in test_items:
            bf.check(item)
            
        # Stop the counter
        end_time = time.perf_counter()
        
        # Calculate results
        total_time = end_time - start_time
        average_time = total_time / len(test_items)
        
        print(f"Total time for {len(test_items)} queries: {total_time:.6f} seconds")
        print(f"Average time per query:     {average_time:.8f} seconds")
        print(f"Estimated queries per sec:  {int(1 / average_time):,}\n")