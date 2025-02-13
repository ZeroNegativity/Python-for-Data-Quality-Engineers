import random
import string

def generate_random_dicts():
    """
    Generates a list of random dictionaries.

    Each dictionary will have:
        - A random number of keys (letters from 'a' to 'z').
        - Random integer values between 0 and 100.
        - The number of dictionaries in the list will be between 2 and 10.

    Returns:
        list: A list of randomly generated dictionaries.

    Example Output:
        [{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]
    """
    num_dicts = random.randint(2, 10)  # Random number of dictionaries (between 2 and 10)
    list_of_dicts = []  # Initialize an empty list to store dictionaries

    for _ in range(num_dicts):
        num_keys = random.randint(1, 5)  # Each dictionary has 1 to 5 keys
        keys = random.sample(string.ascii_lowercase, num_keys)  # Random unique letters as keys
        values = [random.randint(0, 100) for _ in range(num_keys)]  # Random values between 0 and 100
        list_of_dicts.append(dict(zip(keys, values)))  # Create dictionary and add to the list

    return list_of_dicts

def merge_dicts(list_of_dicts):
    """
    Merges a list of dictionaries into a single dictionary.

    If the same key appears in multiple dictionaries:
        - The maximum value is taken.
        - The key is renamed as 'key_index_N' where N is the dictionary index that contained the max value.

    Args:
        list_of_dicts (list): List of dictionaries to merge.

    Returns:
        dict: A merged dictionary with updated key names.

    Example Input:
        [{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]

    Example Output:
        {'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}
    """
    merged_dict = {}  # Dictionary to store the merged results
    key_tracker = {}  # Dictionary to track which dict index had the max value

    for index, d in enumerate(list_of_dicts, start=1):  # Loop through each dictionary with index
        for key, value in d.items():  # Loop through key-value pairs
            if key not in merged_dict or value > merged_dict[key]:  # If new max value found
                merged_dict[key] = value  # Store the max value
                key_tracker[key] = index  # Track which dictionary had this max value

    # Renaming keys based on max value dictionary index
    final_dict = {f"{k}_{key_tracker[k]}" if list_of_dicts.count(k) > 1 else k: v 
                  for k, v in merged_dict.items()}

    return final_dict

if __name__ == "__main__":
    # Step 1: Generate a random list of dictionaries
    random_dicts = generate_random_dicts()
    print("Generated List of Dictionaries:", random_dicts)

    # Step 2: Merge dictionaries according to rules
    merged_result = merge_dicts(random_dicts)
    print("Merged Dictionary:", merged_result)

    # Run doctests (if needed)
    import doctest
    doctest.testmod()
