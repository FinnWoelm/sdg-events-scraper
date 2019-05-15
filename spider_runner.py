from twisted.internet import reactor
import scrapy
from scrapy import signals
from scrapy.utils.project import get_project_settings

from multiprocessing import Queue

from spider_runner_process import SpiderRunnerProcess

# Runs a given spider inside a sub-process
class SpiderRunner:

    __results = None

    def __init__(self, name, **arguments):
        self.name       = name
        self.arguments  = arguments

    # return the results of the spider
    def results(self):
        self.__results = self.__results or self.__run()
        return self.__results

    # run the spider
    def __run(self):
        queue = Queue()
        process = SpiderRunnerProcess(name=self.name,
                                      queue=queue,
                                      **self.arguments)
        process.start()
        process.join()
        return queue.get()
