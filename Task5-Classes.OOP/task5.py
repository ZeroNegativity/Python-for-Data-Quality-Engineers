import datetime
import os


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
    news_feed = NewsFeed()
    while True:
        news_feed.add_record()
        more = input("Do you want to add another record? (yes/no): ")
        if more.lower() != 'yes':
            break
