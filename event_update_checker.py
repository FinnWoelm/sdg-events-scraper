from hash_maker import HashMaker
from spider_runner import SpiderRunner

from event_content_hasher import EventContentHasher

class EventUpdateChecker:

    current_content_hash = None

    def __init__(self, url, content_tag, content_hash):
        self.url                    = url
        self.content_tag            = content_tag
        self.previous_content_hash  = content_hash
        self.event_content_hasher   = EventContentHasher(url=url,
                                                         content_tag=content_tag)
        self.init_spider()

    # Initializer the web crawler/spider
    def init_spider(self):
        self.spider = SpiderRunner('css_tag_content',
                                   url=self.url,
                                   css_tag=self.content_tag)

    # Check if the event has been updated
    def check(self):
        self.current_content_hash = self.__generate_content_hash()

    # Return true if the event was updated. Otherwise false
    def wasUpdated(self):
        if self.current_content_hash is None:
            self.check()
        return self.current_content_hash != self.previous_content_hash

    def __generate_content_hash(self):
        return self.event_content_hasher.content_hash()

# Example
# checker = EventUpdateChecker(content_hash='abc', url='https://17ziele.de/artikel/detail/festival-der-taten.html', content_tag='div.item__content__inner')
# checker.check()
# print(checker.current_content_hash)
