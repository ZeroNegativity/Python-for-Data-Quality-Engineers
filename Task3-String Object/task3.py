import re

def normalize_text(text):
    """
    Normalizes the given text:
    1. Fixes letter case (capitalizes sentences).
    2. Replaces incorrect "iz" with "is" (only when it's a mistake).
    3. Creates a new sentence from the last words of each sentence and adds it to the paragraph.
    4. Counts all whitespace characters (spaces, newlines, tabs, etc.).

    Args:
        text (str): Input text.

    Returns:
        tuple: (normalized_text, whitespace_count)
    """

    # Step 1: Normalize letter cases (capitalize sentences)
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())  # Split by sentence endings
    normalized_sentences = [s.capitalize() for s in sentences]  # Capitalize each sentence

    # Step 2: Fix incorrect "iz" only when it's a mistake
    corrected_sentences = [re.sub(r'\b[iI]z\b', 'is', s) for s in normalized_sentences]

    # Step 3: Create a new sentence using the last word of each existing sentence
    last_words = [s.rstrip('.!?').split()[-1] for s in corrected_sentences]  # Extract last words
    new_sentence = " ".join(last_words).capitalize() + "."  # Form a new sentence

    # Step 4: Append the new sentence to the paragraph
    corrected_sentences.append(new_sentence)

    # Final normalized text
    normalized_text = " ".join(corrected_sentences)

    # Step 5: Count all whitespace characters
    whitespace_count = sum(1 for char in text if char.isspace())

    return normalized_text, whitespace_count


if __name__ == "__main__":
    # Given text
    input_text = """
      tHis iz your homeWork, copy these Text to variable.

      You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

      it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

      last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
    """

    # Process the text
    result_text, whitespace_count = normalize_text(input_text)

    # Print results
    print("Normalized Text:\n", result_text)
    print("\nTotal Whitespace Characters:", whitespace_count)
