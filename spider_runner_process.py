from billiard import Process
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scrapy.signalmanager import dispatcher

# Runs a spider inside a sub process and reports results back to main thread
class SpiderRunnerProcess(Process):
    def __init__(self, name, queue, **arguments):
        Process.__init__(self)
        self.name       = name
        self.queue      = queue
        self.arguments  = arguments
        self.results    = []

    def run(self):
        def crawler_results(signal, sender, item, response, spider):
            self.results.append(item)

        dispatcher.connect(crawler_results, signal=signals.item_passed)

        process = CrawlerProcess(get_project_settings())
        process.crawl(self.name, **self.arguments)
        process.start() # the script will block here until the crawling is finished

        # report results back to main thread
        self.queue.put(self.results)
