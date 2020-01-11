from spider_runner import SpiderRunner
from event import Event
import pprint

class EventsListing:
    # Parameters
    url             = None
    source          = None
    event_tag       = None
    event_title_tag = None
    event_date_tag  = None
    event_url_tag   = None
    next_page_tag   = None

    # Internal
    __spider = None
    __events = None

    def __init__(self, url, source, **arguments):
        self.url    = url
        self.source    = source
        self.event_tag = arguments.pop('event_tag', None)
        self.event_title_tag = arguments.pop('event_title_tag', None)
        self.event_date_tag = arguments.pop('event_date_tag', None)
        self.event_url_tag = arguments.pop('event_url_tag', None)
        self.next_page_tag = arguments.pop('next_page_tag', None)
        self.__init_spider()

    # Initialize an instance of Event from the event returned by spider
    @staticmethod
    def initialize_event_from_spider(event_from_spider):
        event = Event(title=event_from_spider['title'],
                      date=event_from_spider['date'],
                      url=event_from_spider['url'],
                      source=event_from_spider['source'])

        event.generate_id()

        return event

    # Return events of the listing
    def events(self):
        self.__events = self.__events or self.__fetch_events()

        return self.__events

    def __init_spider(self):
        self.__spider = SpiderRunner('events_listing',
                                     url=self.url,
                                     source=self.source,
                                     event_tag=self.event_tag,
                                     event_title_tag=self.event_title_tag,
                                     event_date_tag=self.event_date_tag,
                                     event_url_tag=self.event_url_tag,
                                     next_page_tag=self.next_page_tag)

    def __fetch_events(self):
        return map(EventsListing.initialize_event_from_spider,
                   self.__spider.results())


# Call this script to hash the contents of a given URL and content tag
if __name__ == "__main__":
    listing = EventsListing(
        url='https://www.engagement-global.de/suche.html?keywords=agenda+2030&se_c=event',
        source='engagement-global',
        event_tag='.mod_searchext_result_item',
        event_title_tag='h3::text',
        event_date_tag=None,
        event_url_tag='.url',
        next_page_tag='.pagination .next')

    print(str(len(listing.events())) + ' Events:')
    for event in listing.events():
        print(str(event.id) + ", " + str(event.url))
