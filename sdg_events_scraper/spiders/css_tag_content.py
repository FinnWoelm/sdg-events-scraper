# -*- coding: utf-8 -*-
import scrapy

# Returns the text content within a given CSS tag
class CssTagContentSpider(scrapy.Spider):
    name = 'css_tag_content'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        def strip_text(text):
          return text.strip()

        def extract_all_with_css(query):
            stripped = map(strip_text, response.css(query).getall())
            return u'\n'.join(stripped)

        content = extract_all_with_css(self.css_tag + ' *::text')

        yield {
            'url':     response.request.url,
            'css-tag': self.css_tag,
            'content': content
        }
