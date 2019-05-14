# -*- coding: utf-8 -*-
import scrapy


class Gpf2030AgendaSpider(scrapy.Spider):
    name = 'gpf_2030agenda'
    allowed_domains = ['2030agenda.de']
    start_urls = ['https://www.2030agenda.de/de/2030agenda/events']

    def parse(self, response):
        # Follow event links
        for event_link in response.css('.view-events .views-row .views-field-title a'):
            yield response.follow(event_link, self.parse_event_page)

    def parse_event_page(self, response):
        def strip_text(text):
          return text.strip()

        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def extract_all_with_css(query):
            stripped = map(strip_text, response.css(query).getall())
            return u'\n'.join(stripped)

        yield {
            'title': extract_with_css('.content .page-title *::text'),
            'date': extract_with_css('.content .field--name-field-datum-und-uhrzeit *::text'),
            'location': extract_with_css('.content .field--name-field-ort::text'),
            'link': response.request.url,
            'description': extract_all_with_css('.content .field--name-body.field--type-text-with-summary *::text'),
            'source': self.name
        }
