from google_sheets_data_loader import GoogleSheetsDataLoader
from event import Event

class EventsUpdatesChecker:

    database_sheet_id       = "1NxjKdgT6du_XhVYHF3sP1JhXm8R1JRZ_EPYFhf_-tBA"
    database_tab_id         = "1036992308"
    __events_needing_update = None

    def __init__(self):
        self.events = []

    # Initialize an instance of Event from the event in database
    @staticmethod
    def initialize_event_from_database(event_in_database):
        event = Event(id=event_in_database['UID'],
                      url=event_in_database['URL'],
                      content_tag=event_in_database["Content\nTag"],
                      content_hash_in_database=event_in_database['CID'])

        return event

    # Load the events from Google sheets
    def load_events_from_database(self):
        loader = GoogleSheetsDataLoader(id=self.database_sheet_id,
                                        tab=self.database_tab_id)
        events_in_database = loader.to_dictionary()

        self.events = map(EventsUpdatesChecker.initialize_event_from_database,
                          events_in_database)

    # Return the events that do not have a content hash set in the database
    def events_without_content_hash(self):
        return list(filter(Event.missing_content_hash_in_database, self.events))

    # Return the events that do not have a content tag set
    def events_without_content_tag(self):
        return list(filter(Event.missing_content_tag, self.events))

    # Return the events needing updates
    def events_needing_update(self):
        self.__events_needing_update = (self.__events_needing_update or
                                        list(filter(Event.needs_update, self.events)))

        return self.__events_needing_update


# Call this script to check all events for updates
if __name__ == "__main__":
    "Loading events from Google sheet..."
    checker = EventsUpdatesChecker()
    checker.load_events_from_database()
    print("Fetched " + str(len(checker.events)) + " events...")

    print("Performing health check...")
    print("Events without CID: " + str(len(checker.events_without_content_hash())))
    for event in checker.events_without_content_hash():
        print("Event " + event.id + " missing CID")

    print("Events without content tag: " + str(len(checker.events_without_content_tag())))
    for event in checker.events_without_content_tag():
        print("Event " + event.id + " missing content tag")

    do_not_continue = raw_input("Continue? Type anything to abort: ")

    if do_not_continue:
        print("Aborting...")
        exit()

    events_needing_update_count = len(checker.events_needing_update())
    print("There are " + str(events_needing_update_count) + " events needing update:")

    for count, event in enumerate(checker.events_needing_update(), start=1):
        print("*** Event #"+ str(count) + "/" + str(events_needing_update_count) + " ***")
        print("ID: "      + str(event.id))
        print("URL: "     + str(event.url))
        print("New CID: " + str(event.content_hash_in_source))
        print("")
