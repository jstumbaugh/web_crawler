# import scrapy
import requests
import robotparser
import urlparse
from bs4 import BeautifulSoup
import re


ROOT = 'http://lyle.smu.edu/~fmoore/'

class Crawler:
    """
    TODO
    comments
    """

    def clean_url(self, url):
        """
        this method removes the base url and mailto: links
        """
        baseurl = re.compile(ROOT)
        mailto = re.compile('mailto:')
        return mailto.sub('', baseurl.sub('', url))

    def external_link(self, link):
        """
        This method will check if the url is an external link
        """
        # pattern = re.compile(ROOT)
        if re.compile(ROOT).match(url):
            return True
        else:
            return False


    def crawl(self):
        """
        This is the main worker method. It will parse the urls, add the words to
        the index, get the next links, and continue looping through the queue.
        """

        parser = robotparser.RobotFileParser()
        parser.set_url(urlparse.urljoin(ROOT, 'robots.txt'))
        parser.read()

        # Add root url to queue
        queue = [requests.get(ROOT)]

        # visited links
        visited = []

        # external links
        external = []

        # finds the links in the page
        soup = BeautifulSoup(queue.pop(0).text, 'html.parser')
        for atag in soup.find_all('a'):
            # get all links within the page
            link = atag.get('href')

            # check if we can access the link
            if parser.can_fetch('*', urlparse.urljoin('/', link)):
                # clean the link
                clean_link = self.clean_url(link)
                # check if in queue or visited links
                if clean_link in visited:
                    continue
                if clean_link in queue:
                    continue
                # else not in queue, get text and links on page
                if external_link(clean_link):
                    print "external link"
                    external.append(clean_link)
                    continue
                r = requests.get(urlparse(urljoin(ROOT, clean_link)))
                # print r.text
                # print
                """
                WORKING ON EXTERNAL LINKS RIGHT NOW
                """




###########    Main method    ###########
if __name__ == "__main__":
    crawler = Crawler()
    crawler.crawl()

#########################################
