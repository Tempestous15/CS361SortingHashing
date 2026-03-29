"""
    Heavily inspired by the FNV hash function created by Glenn Fowler, Landon Curt Noll, and Kiem-Phong Vo
"""
import math
# from test_bloom_filter import test_k_indices
# from test_bloom_filter import test_determinism
from test_bloom_filter import test_collision_resistance

class bloom_filter:
    def __init__(self, hash_file, acceptable_error_rate):
        """
        Initialize the Bloom filter with a built-in Python bit array.
        """
        file_size = num_lines(hash_file)
        self.size = get_optimal_size(file_size, acceptable_error_rate)
        self.hash_count = get_optimal_hash_count(self.size, file_size)
        num_bytes = (self.size + 7) // 8 
        self.bit_array = bytearray(num_bytes)
        self.load(hash_file)
        
    def fnv1a_hash(self, item, seed):
        """
        A custom implementation of the 32-bit FNV-1a hash algorithm.
        """
        # Standard 32-bit FNV-1a parameters
        fnv_prime = 0x01000193       # 16777619
        offset_basis = 0x811c9dc5    # 2166136261
        
        # We append the 'seed' to the item so each of our k passes 
        # generates a completely different hash result.
        seeded_item = f"{item}:{seed}"
        
        hash_value = offset_basis
        
        # Process the string byte by byte
        for byte in seeded_item.encode('utf-8'):
            hash_value = hash_value ^ byte                    # XOR the byte into the bottom of the hash
            hash_value = (hash_value * fnv_prime) % (2**32)   # Multiply by prime and constrain to 32 bits
            
        return hash_value

    def get_hash_indices(self, item):
        """
        Generate 'k' distinct bit indices with a double hash
        Standard double hash formula:
            g_i(x) = (h_1(x) + i * h_2(x)) % m
        """
        # Generate two base hashes using different seeds
        h1 = self.fnv1a_hash(item, seed="A")
        h2 = self.fnv1a_hash(item, seed="B")
        
        indices = []
        for i in range(self.hash_count):
            # The linear combination creates a new index for each i
            index = (h1 + i * h2) % self.size
            indices.append(index)
            
        return indices

    def add(self, item):
        """
        Hash the item and set the corresponding bits to 1.
        """
        for index in self.get_hash_indices(item):
            # Find which byte the bit lives in
            byte_index = index // 8
            # Find which bit within that byte to flip
            bit_offset = index % 8
            # Use a bitmask (1 shifted by offset) to set the bit to 1
            self.bit_array[byte_index] |= (1 << bit_offset)

    def check(self, item):
        """
        Hash the item and check if all corresponding bits are 1.
        """
        for index in self.get_hash_indices(item):
            byte_index = index // 8
            bit_offset = index % 8
            # Check if the specific bit is 0 using bitwise AND
            if not (self.bit_array[byte_index] & (1 << bit_offset)):
                # Return false if confident bit doesn't exist
                return False
                
        return True # Probably in the set
    
    def load(self, file_path):
        """
        Load given file into hash
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as infile:
                
                for file_size, line in enumerate(infile):
                    self.add(line.strip())
                    
            print(f"Success! {file_size + 1} lines have been hashed.")
        
        except FileNotFoundError:
            print(f"Error: The file '{INPUT_FILE_PATH}' was not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
                
        return True # Probably in the set
    
def num_lines(file_path):
    num_lines = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as infile:
            
            for line in enumerate(infile):
                num_lines = num_lines + 1
                
            print(f"{num_lines} lines have been counted.")
    
    except FileNotFoundError:
        print(f"Error: The file '{INPUT_FILE_PATH}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return num_lines
    
def get_optimal_size(n, p):
    """
    Calculate the optimal bit array size (m).
    :param n: Expected number of items.
    :param p: Acceptable false positive probability (e.g., 0.01).
    :return: Integer size of the bit array.
    """
    m = -(n * math.log(p)) / (math.log(2) ** 2)
    print(f"Optimal bit array size: {m}")
    return int(math.ceil(m))

def get_optimal_hash_count(m, n):
    """
    Calculate the optimal number of hash functions (k).
    :param m: Size of the bit array.
    :param n: Expected number of items.
    :return: Integer number of hash functions.
    """
    k = (m / n) * math.log(2)
    print(f"Optimal hash count: {k}")
    return int(math.ceil(k))



if __name__ == "__main__":
    INPUT_FILE_PATH = 'part2_bloom_filter\\test_cases\\1MPasswords.txt'
    acceptable_error_rate = 0.01   # 1% error rate
    bf = bloom_filter(INPUT_FILE_PATH, acceptable_error_rate)
    # Check for items
    
    print(f"'00000019C61335B410967582B2024D78A8A59D68' present?  {bf.check('00000019C61335B410967582B2024D78A8A59D68')}")     # Output: True
    print(f"'0000001C5111E4CE5FCCE9C259739925AAA5C819' present?  {bf.check('0000001C5111E4CE5FCCE9C259739925AAA5C819')}")     # Output: True
    print(f"'000189600E9A1042C7B5ED1C2A84704B099F978E' present?  {bf.check('000189600E9A1042C7B5ED1C2A84704B099F978E')}")     # Output: True
    print(f"'000000005AD76SD555C1D6D771DE417A4B87E4B4' present?  {bf.check('000000005AD76SD555C1D6D771DE417A4B87E4B4')}")     # Output: False

    sample_items = [
        "00000019C61335B410967582B2024D78A8A59D68",
        "apple",
        "banana",
        "a_very_long_password_string_1234567890"
    ]
    # test_k_indices(bf, sample_items)
    # test_determinism(bf, sample_items, 10)
    test_collision_resistance(bf, 100000)


    