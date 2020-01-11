import csv
from google_sheets_data_loader import GoogleSheetsDataLoader
from event import Event
from events_listing import EventsListing

class EventsListingsChecker:

    database_sheet_id               = "1NxjKdgT6du_XhVYHF3sP1JhXm8R1JRZ_EPYFhf_-tBA"
    database_tab_id_for_listings    = "1925444285"
    database_tab_id_for_events      = "432768265"
    events_listings                 = None
    events_in_listings              = None
    events_in_database              = None
    __new_events                    = None

    # Initialize an instance of EventsListing from the listing in database
    @staticmethod
    def initialize_events_listing_from_database(listing_in_database):
        listing = EventsListing(source=listing_in_database['Name'],
                                url=listing_in_database['URL'],
                                event_tag=listing_in_database["Event Tag"],
                                event_title_tag=listing_in_database['Event Title Tag'],
                                event_date_tag=listing_in_database['Event Date Tag'],
                                event_url_tag=listing_in_database['Event URL Tag'],
                                next_page_tag=listing_in_database['Next Page Tag'])

        return listing

    # Initialize an instance of Event from the event in database
    @staticmethod
    def initialize_event_from_database(event_in_database):
        event = Event(id=event_in_database['UID'])

        return event

    # Load the events listings from Google sheets
    def load_events_listings_from_database(self):
        loader = GoogleSheetsDataLoader(id=self.database_sheet_id,
                                        tab=self.database_tab_id_for_listings)
        listings_in_database = loader.to_dictionary()

        self.events_listings = map(EventsListingsChecker.initialize_events_listing_from_database,
                                   listings_in_database)

    # Load the events from Google sheets
    def load_events_from_database(self):
        loader = GoogleSheetsDataLoader(id=self.database_sheet_id,
                                        tab=self.database_tab_id_for_events)
        events_in_database = loader.to_dictionary()

        self.events_in_database = map(EventsListingsChecker.initialize_event_from_database,
                                      events_in_database)

    # Return a list of new events that were found in the listings, but are not
    # yet in the database
    def new_events(self):
        if not self.__new_events:
            # Diff the IDs of existing events with the IDs of new events
            event_ids_in_listings = [event.id for event in self.events_in_listings]
            event_ids_in_database = [event.id for event in self.events_in_database]
            new_event_ids = list(set(event_ids_in_listings) - set(event_ids_in_database))
            self.__new_events = list(filter(lambda event: event.id in new_event_ids, self.events_in_listings))

        return self.__new_events

    # Load the events listings from Google sheets
    def scrape_listings(self):
        # List comprehension: https://stackoverflow.com/a/952952/6451879
        self.events_in_listings = [event for listing in self.events_listings for event in listing.events()]

# Call this script to check for new, untracked events
if __name__ == "__main__":
    "Loading events listings from Google sheet..."
    checker = EventsListingsChecker()
    checker.load_events_listings_from_database()
    print("Fetched " + str(len(checker.events_listings)) + " listings.")

    do_not_continue = raw_input("Scrape listings? Type anything to abort: ")

    if do_not_continue:
        print("Aborting...")
        exit()

    checker.scrape_listings()

    print("Scraping complete. Found " + str(len(checker.events_in_listings)) + " events in listings.")

    print("Loading existing events from Google sheet...")
    checker.load_events_from_database()
    print("Fetched " + str(len(checker.events_in_database)) + " events.")

    print("Comparing events in web listings to events in the database...")
    new_event_count = len(checker.new_events())
    print("There are " + str(new_event_count) + " new events:")

    for count, event in enumerate(checker.new_events(), start=1):
        print("*** Event #"+ str(count) + "/" + str(new_event_count) + " ***")
        print("ID: "     + str(event.id))
        print("URL: "    + str(event.url))
        print("Title: "  + str(event.title))
        print("Date: "   + str(event.date))
        print("Source: " + str(event.source))
        print("")

    output_file = 'output/new-events.csv'
    print("Writing new events to " + output_file + "...")
    with open(output_file, 'w') as csvFile:
        fields = ['id', 'title', 'start_date', 'start_time', 'end_date', 'end_time', 'location', 'url', 'source']
        writer = csv.DictWriter(csvFile, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(map(vars, checker.new_events()))

    csvFile.close()
    print("Done!")
