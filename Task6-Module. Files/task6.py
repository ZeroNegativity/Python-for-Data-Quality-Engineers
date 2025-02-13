import datetime
import os
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


class FileRecordProcessor:
    """
    Class to process records from a file. Handles normalization and saving records to the feed.
    """
    def __init__(self, input_file=None, output_file="news_feed.txt"):
        self.input_file = input_file if input_file else "default_folder/input_file.txt"
        self.output_file = output_file

    def process_file(self):
        """
        Process the input file, normalize text, and add records to the output file.
        """
        if not os.path.exists(self.input_file):
            print(f"File {self.input_file} does not exist.")
            return

        with open(self.input_file, 'r') as file:
            lines = file.readlines()

        for line in lines:
            # Example format: "News|text|city"
            parts = line.strip().split('|')
            record_type = parts[0].strip()
            text = parts[1].strip()

            # Normalize the text from Homework 3
            normalized_text, _ = normalize_text(text)

            if record_type == "News" and len(parts) == 3:
                city = parts[2].strip()
                record = News(normalized_text, city)
            elif record_type == "PrivateAd" and len(parts) == 3:
                expiration_date = parts[2].strip()
                record = PrivateAd(normalized_text, expiration_date)
            elif record_type == "Event" and len(parts) == 4:
                location = parts[2].strip()
                event_date = parts[3].strip()
                record = Event(normalized_text, location, event_date)
            else:
                print(f"Invalid record format for: {line}")
                continue

            # Save the record to file
            record.save_to_file(self.output_file)

        # After processing, remove the file
        os.remove(self.input_file)
        print(f"File {self.input_file} processed and removed.")


class NewsFeed:
    """
    Manages the process of adding different types of records to the news feed.
    """
    def __init__(self, file_name="news_feed.txt"):
        self.file_name = file_name

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
        print("Record added successfully!")


if __name__ == "__main__":
    # Example of user interface for adding records
    news_feed = NewsFeed()
    while True:
        news_feed.add_record()
        more = input("Do you want to add another record? (yes/no): ")
        if more.lower() != 'yes':
            break

    # Example of processing records from a file
    file_processor = FileRecordProcessor(input_file="records.txt")
    file_processor.process_file()
