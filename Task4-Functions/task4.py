import random
import string
import re

def generate_random_dicts():
    """
    Generates a list of random dictionaries.

    Returns:
        list: A list of dictionaries where each dictionary has a random number of keys (letters) 
              and random values (0-100).
    """
    num_dicts = random.randint(2, 10)
    list_of_dicts = []
    
    for _ in range(num_dicts):
        num_keys = random.randint(1, 5)
        keys = random.sample(string.ascii_lowercase, num_keys)
        values = [random.randint(0, 100) for _ in range(num_keys)]
        list_of_dicts.append(dict(zip(keys, values)))
    
    return list_of_dicts

def merge_dicts(list_of_dicts):
    """
    Merges a list of dictionaries based on given rules.

    Args:
        list_of_dicts (list): List of dictionaries to merge.

    Returns:
        dict: A merged dictionary with updated key names.
    """
    merged_dict = {}
    key_tracker = {}
    
    for index, d in enumerate(list_of_dicts, start=1):
        for key, value in d.items():
            if key not in merged_dict or value > merged_dict[key]:
                merged_dict[key] = value
                key_tracker[key] = index
    
    final_dict = {f"{k}_{key_tracker[k]}" if sum(1 for d in list_of_dicts if k in d) > 1 else k: v 
                  for k, v in merged_dict.items()}
    
    return final_dict

def normalize_text(text):
    """
    Normalizes text by fixing letter cases, correcting "iz" typos, 
    generating a summary sentence, and counting whitespace characters.

    Args:
        text (str): Input text.

    Returns:
        tuple: (normalized_text, whitespace_count)
    """
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    normalized_sentences = [s.capitalize() for s in sentences]
    corrected_sentences = [re.sub(r'\b[iI]z\b', 'is', s) for s in normalized_sentences]
    last_words = [s.rstrip('.!?').split()[-1] for s in corrected_sentences]
    new_sentence = " ".join(last_words).capitalize() + "."
    corrected_sentences.append(new_sentence)
    normalized_text = " ".join(corrected_sentences)
    whitespace_count = sum(1 for char in text if char.isspace())
    
    return normalized_text, whitespace_count

if __name__ == "__main__":
    random_dicts = generate_random_dicts()
    print("Generated List of Dictionaries:", random_dicts)
    
    merged_result = merge_dicts(random_dicts)
    print("Merged Dictionary:", merged_result)
    
    input_text = """
      tHis iz your homeWork, copy these Text to variable.
      You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.
      it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.
      last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
    """
    
    result_text, whitespace_count = normalize_text(input_text)
    print("Normalized Text:\n", result_text)
    print("\nTotal Whitespace Characters:", whitespace_count)
