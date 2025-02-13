import datetime
import os
import re
import csv
import json
import sqlite3
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


class DatabaseManager:
    def __init__(self, db_name="news_feed.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        """Creates separate tables for News, Private Ads, and Events."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS News (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT UNIQUE,
                city TEXT,
                publish_date TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS PrivateAd (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT UNIQUE,
                expiration_date TEXT,
                days_left INTEGER,
                publish_date TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Event (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT UNIQUE,
                location TEXT,
                event_date TEXT,
                days_until_event INTEGER,
                publish_date TEXT
            )
        """)
        self.connection.commit()

    def insert_record(self, table_name, record_data):
        """Inserts a new record into the database, avoiding duplicates."""
        placeholders = ", ".join(["?"] * len(record_data))
        query = f"INSERT OR IGNORE INTO {table_name} VALUES (NULL, {placeholders})"

        self.cursor.execute(query, record_data)
        self.connection.commit()

    def close_connection(self):
        self.connection.close()


class Record:
    def __init__(self, text):
        self.text = text
        self.publish_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def save_to_db(self, db_manager):
        raise NotImplementedError("Subclass must implement save_to_db method.")


class News(Record):
    def __init__(self, text, city):
        super().__init__(text)
        self.city = city

    def save_to_db(self, db_manager):
        db_manager.insert_record("News", (self.text, self.city, self.publish_date))


class PrivateAd(Record):
    def __init__(self, text, expiration_date):
        super().__init__(text)
        self.expiration_date = datetime.datetime.strptime(expiration_date, '%Y-%m-%d')
        self.days_left = (self.expiration_date - datetime.datetime.now()).days

    def save_to_db(self, db_manager):
        db_manager.insert_record("PrivateAd", (self.text, self.expiration_date.strftime('%Y-%m-%d'), self.days_left, self.publish_date))


class Event(Record):
    def __init__(self, text, location, event_date):
        super().__init__(text)
        self.location = location
        self.event_date = datetime.datetime.strptime(event_date, '%Y-%m-%d')
        self.days_until_event = (self.event_date - datetime.datetime.now()).days

    def save_to_db(self, db_manager):
        db_manager.insert_record("Event", (self.text, self.location, self.event_date.strftime('%Y-%m-%d'), self.days_until_event, self.publish_date))


class XMLLoader:
    def __init__(self, db_manager, default_folder="data"):
        self.db_manager = db_manager
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

            obj.save_to_db(self.db_manager)

        os.remove(xml_file_path)
        print(f"XML file {xml_file_path} processed and removed.")


if __name__ == "__main__":
    db_manager = DatabaseManager()
    xml_loader = XMLLoader(db_manager)

    while True:
        print("1. Add News manually")
        print("2. Add Private Ad manually")
        print("3. Add Event manually")
        print("4. Load records from XML")
        print("5. Exit")
        choice = input("Enter choice (1-5): ")

        if choice == '1':
            text = input("Enter news text: ")
            city = input("Enter city: ")
            news = News(text, city)
            news.save_to_db(db_manager)
            print("News added successfully.")

        elif choice == '2':
            text = input("Enter ad text: ")
            exp_date = input("Enter expiration date (YYYY-MM-DD): ")
            ad = PrivateAd(text, exp_date)
            ad.save_to_db(db_manager)
            print("Private Ad added successfully.")

        elif choice == '3':
            text = input("Enter event text: ")
            location = input("Enter location: ")
            event_date = input("Enter event date (YYYY-MM-DD): ")
            event = Event(text, location, event_date)
            event.save_to_db(db_manager)
            print("Event added successfully.")

        elif choice == '4':
            xml_file = input("Enter XML file path (or press Enter for default): ") or None
            xml_loader.load_from_xml(xml_file)

        elif choice == '5':
            db_manager.close_connection()
            print("Exiting...")
            break

        else:
            print("Invalid choice!")
