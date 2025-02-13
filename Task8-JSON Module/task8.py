import datetime
import os
import re
import csv
import json


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


class Record:
    """
    Base class for a record in the news feed.
    Each record will have a common structure to be published to a text file.
    """
    def __init__(self, text):
        self.text = text
        self.publish_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def save_to_file(self, file_name):
        """
        Save the record to a text file with the special format.
        Args:
            file_name (str): The name of the file to save the record.
        """
        raise NotImplementedError("Subclass must implement save_to_file method.")


class News(Record):
    """
    News record type class with city as input.
    The publish date is automatically calculated.
    """
    def __init__(self, text, city):
        super().__init__(text)
        self.city = city

    def save_to_file(self, file_name):
        """
        Save the News record to the file in the specified format.
        Format: [Publish Date] [City] [Text]
        """
        with open(file_name, 'a') as file:
            file.write(f"{self.publish_date} {self.city} {self.text}\n")


class PrivateAd(Record):
    """
    Private Ad record type class with expiration date as input.
    The days left are calculated during publishing.
    """
    def __init__(self, text, expiration_date):
        super().__init__(text)
        self.expiration_date = datetime.datetime.strptime(expiration_date, '%Y-%m-%d')
        self.days_left = (self.expiration_date - datetime.datetime.now()).days

    def save_to_file(self, file_name):
        """
        Save the Private Ad record to the file in the specified format.
        Format: [Publish Date] [Text] [Days Left]
        """
        with open(file_name, 'a') as file:
            file.write(f"{self.publish_date} {self.text} Days left: {self.days_left}\n")


class Event(Record):
    """
    Event record type with date and location. Includes unique publishing rules.
    The publish date is automatically calculated.
    """
    def __init__(self, text, location, event_date):
        super().__init__(text)
        self.location = location
        self.event_date = datetime.datetime.strptime(event_date, '%Y-%m-%d')
        self.days_until_event = (self.event_date - datetime.datetime.now()).days

    def save_to_file(self, file_name):
        """
        Save the Event record to the file in the specified format.
        Format: [Publish Date] [Location] [Text] [Days Until Event]
        """
        with open(file_name, 'a') as file:
            file.write(f"{self.publish_date} {self.location} {self.text} Days until event: {self.days_until_event}\n")


class NewsFeed:
    """
    Manages the process of adding different types of records to the news feed.
    """
    def __init__(self, file_name="news_feed.txt", word_count_file="word-count.csv", letter_count_file="letter-count.csv"):
        self.file_name = file_name
        self.word_count_file = word_count_file
        self.letter_count_file = letter_count_file

    def update_word_count(self, text):
        """
        Update the word count CSV with the frequency of words in the record (lowercased).
        """
        words = text.lower().split()
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1

        # Write or rewrite word-count CSV
        with open(self.word_count_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Word", "Count"])
            for word, count in word_count.items():
                writer.writerow([word, count])

    def update_letter_count(self, text):
        """
        Update the letter count CSV with details about the record's letter usage.
        """
        # Remove spaces and count letters
        letters = [char for char in text if char.isalpha()]
        total_letters = len(letters)
        uppercase_count = sum(1 for char in letters if char.isupper())
        uppercase_percentage = (uppercase_count / total_letters) * 100 if total_letters else 0

        # Write or rewrite letter-count CSV
        with open(self.letter_count_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Letter", "Count_All", "Count_Uppercase", "Percentage"])
            writer.writerow([text, total_letters, uppercase_count, uppercase_percentage])

    def add_record(self):
        """
        Allow the user to select the type of record to add and collect input.
        """
        print("Select record type:")
        print("1. News")
        print("2. Private Ad")
        print("3. Event")
        choice = input("Enter choice (1/2/3): ")

        if choice == '1':
            text = input("Enter news text: ")
            city = input("Enter city: ")
            record = News(text, city)
        elif choice == '2':
            text = input("Enter private ad text: ")
            expiration_date = input("Enter expiration date (YYYY-MM-DD): ")
            record = PrivateAd(text, expiration_date)
        elif choice == '3':
            text = input("Enter event text: ")
            location = input("Enter event location: ")
            event_date = input("Enter event date (YYYY-MM-DD): ")
            record = Event(text, location, event_date)
        else:
            print("Invalid choice!")
            return

        # Save record to file
        record.save_to_file(self.file_name)

        # Update CSV files
        self.update_word_count(record.text)
        self.update_letter_count(record.text)
        print("Record added successfully!")

    def load_from_json(self, json_file_path):
        """
        Load records from a JSON file.
        """
        if not os.path.exists(json_file_path):
            print("The specified file does not exist.")
            return

        with open(json_file_path, 'r') as file:
            records_data = json.load(file)

        for record_data in records_data:
            record_type = record_data.get("type")
            text = record_data.get("text")

            if record_type == "news":
                city = record_data.get("city")
                record = News(text, city)
            elif record_type == "private_ad":
                expiration_date = record_data.get("expiration_date")
                record = PrivateAd(text, expiration_date)
            elif record_type == "event":
                location = record_data.get("location")
                event_date = record_data.get("event_date")
                record = Event(text, location, event_date)
            else:
                print(f"Unknown record type: {record_type}")
                continue

            # Save record to file
            record.save_to_file(self.file_name)

            # Update CSV files
            self.update_word_count(record.text)
            self.update_letter_count(record.text)

        # Remove the file if processed successfully
        os.remove(json_file_path)
        print(f"File {json_file_path} processed and removed.")


if __name__ == "__main__":
    # Example of user interface for adding records or loading from JSON
    news_feed = NewsFeed()
    while True:
        print("1. Add record manually")
        print("2. Load records from JSON")
        choice = input("Enter choice (1/2): ")

        if choice == '1':
            news_feed
            news_feed.add_record()
        elif choice == '2':
            json_file_path = input("Enter the path of the JSON file: ")
            news_feed.load_from_json(json_file_path)
        else:
            print("Invalid choice. Exiting...")
            break
