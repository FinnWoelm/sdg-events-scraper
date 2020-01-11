# -*- coding: utf-8 -*-
import scrapy

# TODO: Refactor print statements into callback methods
#       page_parsed_callback=method
#       next_page_callback=method

class EventsListingSpider(scrapy.Spider):
    name = 'events_listing'
    page_count = 1

    def start_requests(self):
        print 'Parsing ' + self.url + '...'

        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        # Appends default_selector (such as ' *::text') to the query, unless
        # the query already has a selector set
        def format_query(query, default_selector):
            is_exact_query = '::' in query

            if is_exact_query:
                return query
            else:
                return query + default_selector


        def strip_text(text):
          return text.strip()

        def extract_href_from(css_object, query):
            if not query:
                return None

            full_query = format_query(query, ' *::attr(href)')

            url = css_object.css(full_query).get(default='').strip()

            if url:
                url = response.urljoin(url)

            return url

        def extract_text_from(css_object, query):
            if not query:
                return None

            full_query = format_query(query, ' *::text')

            stripped = map(strip_text, css_object.css(full_query).getall())
            return u'\n'.join(stripped).strip().encode('utf-8')

        # Parse each event listing
        events = response.css(self.event_tag)

        for event in events:
            yield {
                'title':    extract_text_from(event, self.event_title_tag),
                'date':     extract_text_from(event, self.event_date_tag),
                'url':      extract_href_from(event, self.event_url_tag),
                'source':   self.source
            }

        print "Found " + str(len(events)) + " events."

        if self.next_page_tag:
            next_page = extract_href_from(response, self.next_page_tag)

            # Go to next page
            if next_page:
                self.page_count += 1
                print "Parsing page " + str(self.page_count) + "..."
                yield response.follow(next_page, callback=self.parse)
