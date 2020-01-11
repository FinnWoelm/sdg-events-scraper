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
        # return content hash only if URL and content tag are set
        if self.url and self.content_tag:
            self.__content_hash = (self.__content_hash or
                                   self.__generate_content_hash())
            return self.__content_hash

    # Generate the content hash from the web content
    def __generate_content_hash(self):
        content = self.__web_content()

        if content:
            return HashMaker.md5_hash_from_text(self.__web_content())

    # Perform the scrape
    def __web_content(self):
        return self.spider.results()[0]['content'].encode('utf-8')


# Call this script to hash the contents of a given URL and content tag
if __name__ == "__main__":
    url = raw_input("URL: ")
    content_tag = raw_input("CSS tag: ")
    hasher = EventContentHasher(str(url), str(content_tag))
    print("Generating content ID...")
    print("CID: " + hasher.content_hash())
