#!/usr/bin/python
import os

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer

from yzwspiderfork.yzw.spiders import subjects, schools


def startup():
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'yzwspiderfork.yzw.settings')
    settings = get_project_settings()

    info_list = ['SSDM',
                 'LOG_LEVEL',
                 'SSDM',
                 'MLDM',
                 'YJXKDM',
                 'MYSQL']
    for key, value in settings.items():
        if key in info_list:
            print('%10s\t\t%s' % (key, value))

    configure_logging(settings)
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(subjects.SubjectsSpider)
        yield runner.crawl(schools.SchoolsSpider)
        reactor.stop()

    crawl()
    reactor.run()


if __name__ == '__main__':
    startup()
