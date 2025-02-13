import datetime
import os
import re
import csv
import json
import xml.etree.ElementTree as ET


def normalize_text(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    normalized_sentences = [s.capitalize() for s in sentences]
    corrected_sentences = [re.sub(r'\b[iI]z\b', 'is', s) for s in normalized_sentences]
    last_words = [s.rstrip('.!?').split()[-1] for s in corrected_sentences]
    new_sentence = " ".join(last_words).capitalize() + "."
    corrected_sentences.append(new_sentence)
    normalized_text = " ".join(corrected_sentences)
    whitespace_count = sum(1 for char in text if char.isspace())

    return normalized_text, whitespace_count


class Record:
    def __init__(self, text):
        self.text = text
        self.publish_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def save_to_file(self, file_name):
        raise NotImplementedError("Subclass must implement save_to_file method.")


class News(Record):
    def __init__(self, text, city):
        super().__init__(text)
        self.city = city

    def save_to_file(self, file_name):
        with open(file_name, 'a') as file:
            file.write(f"{self.publish_date} {self.city} {self.text}\n")


class PrivateAd(Record):
    def __init__(self, text, expiration_date):
        super().__init__(text)
        self.expiration_date = datetime.datetime.strptime(expiration_date, '%Y-%m-%d')
        self.days_left = (self.expiration_date - datetime.datetime.now()).days

    def save_to_file(self, file_name):
        with open(file_name, 'a') as file:
            file.write(f"{self.publish_date} {self.text} Days left: {self.days_left}\n")


class Event(Record):
    def __init__(self, text, location, event_date):
        super().__init__(text)
        self.location = location
        self.event_date = datetime.datetime.strptime(event_date, '%Y-%m-%d')
        self.days_until_event = (self.event_date - datetime.datetime.now()).days

    def save_to_file(self, file_name):
        with open(file_name, 'a') as file:
            file.write(f"{self.publish_date} {self.location} {self.text} Days until event: {self.days_until_event}\n")


class NewsFeed:
    def __init__(self, file_name="news_feed.txt", word_count_file="word-count.csv", letter_count_file="letter-count.csv"):
        self.file_name = file_name
        self.word_count_file = word_count_file
        self.letter_count_file = letter_count_file

    def update_word_count(self, text):
        words = text.lower().split()
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1

        with open(self.word_count_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Word", "Count"])
            for word, count in word_count.items():
                writer.writerow([word, count])

    def update_letter_count(self, text):
        letters = [char for char in text if char.isalpha()]
        total_letters = len(letters)
        uppercase_count = sum(1 for char in letters if char.isupper())
        uppercase_percentage = (uppercase_count / total_letters) * 100 if total_letters else 0

        with open(self.letter_count_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Letter", "Count_All", "Count_Uppercase", "Percentage"])
            writer.writerow([text, total_letters, uppercase_count, uppercase_percentage])

    def load_from_json(self, json_file_path):
        if not os.path.exists(json_file_path):
            print("The specified file does not exist.")
            return

        with open(json_file_path, 'r') as file:
            records_data = json.load(file)

        for record_data in records_data:
            record_type = record_data.get("type")
            text = record_data.get("text")

            if record_type == "news":
                record = News(text, record_data.get("city"))
            elif record_type == "private_ad":
                record = PrivateAd(text, record_data.get("expiration_date"))
            elif record_type == "event":
                record = Event(text, record_data.get("location"), record_data.get("event_date"))
            else:
                print(f"Unknown record type: {record_type}")
                continue

            record.save_to_file(self.file_name)
            self.update_word_count(record.text)
            self.update_letter_count(record.text)

        os.remove(json_file_path)
        print(f"File {json_file_path} processed and removed.")


class XMLLoader:
    def __init__(self, news_feed, default_folder="data"):
        self.news_feed = news_feed
        self.default_folder = default_folder

    def load_from_xml(self, xml_file_path=None):
        if xml_file_path is None:
            xml_file_path = os.path.join(self.default_folder, "records.xml")

        if not os.path.exists(xml_file_path):
            print("The specified XML file does not exist.")
            return

        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        for record in root.findall("record"):
            record_type = record.get("type")
            text = record.find("text").text.strip()

            if record_type == "news":
                city = record.find("city").text.strip()
                obj = News(text, city)
            elif record_type == "private_ad":
                expiration_date = record.find("expiration_date").text.strip()
                obj = PrivateAd(text, expiration_date)
            elif record_type == "event":
                location = record.find("location").text.strip()
                event_date = record.find("event_date").text.strip()
                obj = Event(text, location, event_date)
            else:
                print(f"Unknown record type: {record_type}")
                continue

            obj.save_to_file(self.news_feed.file_name)
            self.news_feed.update_word_count(obj.text)
            self.news_feed.update_letter_count(obj.text)

        os.remove(xml_file_path)
        print(f"XML file {xml_file_path} processed and removed.")


if __name__ == "__main__":
    news_feed = NewsFeed()
    xml_loader = XMLLoader(news_feed)

    while True:
        print("1. Add record manually")
        print("2. Load records from JSON")
        print("3. Load records from XML")
        choice = input("Enter choice (1/2/3): ")

        if choice == '1':
            news_feed.add_record()
        elif choice == '2':
            json_file = input("Enter JSON file path (or press Enter for default): ") or "data/records.json"
            news_feed.load_from_json(json_file)
        elif choice == '3':
            xml_file = input("Enter XML file path (or press Enter for default): ") or None
            xml_loader.load_from_xml(xml_file)
        else:
            print("Invalid choice!")
