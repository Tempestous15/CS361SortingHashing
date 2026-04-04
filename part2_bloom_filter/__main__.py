from importlib import resources
import test_cases
from bloom_filter import bloom_filter
from test_bloom_filter import (
    test_k_indices, 
    test_determinism, 
    test_false_positive_rate, 
    test_query_time
)

if __name__ == "__main__":
    INPUT_FILE_PATH = resources.files(test_cases).joinpath('1MPasswords.txt')
    acceptable_error_rate = 0.01   # 1% error rate
    bf = bloom_filter(INPUT_FILE_PATH, acceptable_error_rate)
    
    sample_items = [
        "00000019C61335B410967582B2024D78A8A59D68",
        "apple",
        "banana",
        "a_very_long_password_string_1234567890"
    ]

    # Proof tests for bloom_filter
    
    test_k_indices(bf, sample_items)
    test_determinism(bf, sample_items, 100)
    test_false_positive_rate(bf, 100000)

    # Query time test for bloom_filter
    test_items = []
    try:
        with INPUT_FILE_PATH.open('r', encoding='utf-8') as infile:
            
            for _, line in enumerate(infile):
                test_items.append(line)
                    
    except FileNotFoundError:
        print(f"Error: The file '{INPUT_FILE_PATH}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    test_query_time(bf, test_items)

    print("Done!")