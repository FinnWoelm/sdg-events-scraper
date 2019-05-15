from hash_maker import HashMaker
from spider_runner import SpiderRunner

class EventContentHasher:

    __content_hash = None

    def __init__(self, url, content_tag):
        self.url            = url
        self.content_tag    = content_tag
        self.init_spider()

    # Initializer the web crawler/spider
    def init_spider(self):
        self.spider = SpiderRunner('css_tag_content',
                                   url=self.url,
                                   css_tag=self.content_tag)

    # Return the web content as MD5 hash
    def content_hash(self):
        self.__content_hash = self.__content_hash or self.__generate_content_hash()
        return self.__content_hash

    # Generate the content hash from the web content
    def __generate_content_hash(self):
        return HashMaker.md5_hash_from_text(self.__web_content())

    # Perform the scrape
    def __web_content(self):
        return self.spider.results()[0]['content'].encode('utf-8')


# Example
# hasher = EventContentHasher(url='https://17ziele.de/artikel/detail/festival-der-taten.html', content_tag='div.item__content__inner')
# print(hasher.content_hash())
