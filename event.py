from event_content_hasher import EventContentHasher

class Event:
    # Parameters
    id = None
    title = None
    date = None
    description = None
    url = None
    source = None
    location = None

    # Content Hashing
    content_tag = None
    content_hash_in_database = None
    content_hash_in_source = None

    def __init__(self, **arguments):
        self.id             = arguments.pop('id', None)
        self.title    = arguments.pop('title', None)
        self.date    = arguments.pop('date', None)
        self.description    = arguments.pop('description', None)
        self.url    = arguments.pop('url', None)
        self.source    = arguments.pop('source', None)
        self.location    = arguments.pop('location', None)
        self.content_tag                = arguments.pop('content_tag', None)
        self.content_hash_in_database   = arguments.pop('content_hash_in_database', None)
        self.content_hash_in_source     = None

    def missing_content_tag(self):
        return not self.content_tag

    def missing_content_hash_in_database(self):
        return not self.content_hash_in_database

    def needs_update(self):
        self.content_hash_in_source = (self.content_hash_in_source or
                                       self.get_content_hash_in_source())

        return (self.content_hash_in_database is None or
                self.content_hash_in_source is None or
                self.content_hash_in_database != self.content_hash_in_source)

    def get_content_hash_in_source(self):
        hasher = EventContentHasher(url=self.url,
                                    content_tag=self.content_tag)
        return hasher.content_hash()
