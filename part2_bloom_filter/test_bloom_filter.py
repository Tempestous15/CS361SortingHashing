def test_k_indices(bf, test_items):
    """
    Tests if the Bloom filter generates exactly 'k' indices 
    and ensures they are within the bounds of the bit array.
    """
    expected_k = bf.hash_count
    print(f"\n--- Testing Hash Indices ---")
    print(f"Expected number of indices (k): {expected_k}")
    print(f"Bit array size (m): {bf.size}")
    print("-" * 30)

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
            
    print("-" * 30)
    if all_passed:
        print("SUCCESS: The Bloom filter correctly returns 'k' valid indices!")
    else:
        print("FAILURE: Check your index generation logic.")
    print("-" * 30 + "\n")

def test_determinism(bf, test_items, num_trials=5):
    """
    Tests if the Bloom filter generates the exact same indices 
    for the exact same input across multiple calls.
    """
    print(f"\n--- Testing Hash Determinism ---")
    print(f"Number of trials per item: {num_trials}")
    print("-" * 30)

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

    print("-" * 30)
    if all_passed:
        print("SUCCESS: The hash function is perfectly deterministic!")
    else:
        print("FAILURE: The hash function returned different indices for the same input.")
    print("-" * 30 + "\n")

def test_collision_resistance(bf, num_items=10000):
    """
    Tests that a large number of different inputs generate 
    different sets of indices (testing for total hash collisions).
    """
    print(f"\n--- Testing Hash Collision Resistance ---")
    print(f"Generating {num_items} unique items...")
    
    unique_index_sets = set()
    collisions = 0
    
    for i in range(num_items):
        # Generate a unique string for every iteration
        item = f"unique_test_string_{i}"
        
        # Get indices and convert the list to a tuple. 
        # We must use a tuple because Python sets require immutable/hashable elements.
        indices = tuple(bf.get_hash_indices(item))
        
        # If the exact tuple of indices is already in our set, we hit a collision
        if indices in unique_index_sets:
            collisions += 1
        else:
            unique_index_sets.add(indices)
            
    collision_rate = (collisions / num_items) * 100
    
    print(f"Total items tested: {num_items}")
    print(f"Unique index sets generated: {len(unique_index_sets)}")
    print(f"Exact tuple collisions detected: {collisions}")
    print(f"Collision rate: {collision_rate:.4f}%")
    
    # We expect 0 exact tuple collisions for a well-distributed hash
    # over a bit array sized for 100k items.
    passed = (collisions == 0)
    
    print("-" * 30)
    if passed:
        print(f"SUCCESS: All {num_items} items produced a unique signature of indices!")
    else:
        print("WARNING: Some items produced the exact same indices. This increases false positive rates.")
    print("-" * 30 + "\n")