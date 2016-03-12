import requests
import robotparser
import urlparse
from bs4 import BeautifulSoup
import re


_ROOT_ = 'http://lyle.smu.edu/~fmoore/'

class Crawler:

    def clean_url(self, url) :
        """
        This method removes the base url
        EX. http://lyle.smu.edu/~fmoore/schedule.htm => schedule.htm
        """
        link = re.compile(_ROOT_).sub('', url)
        return re.compile('\.\.').sub('', link)

    def fetch(self, url) :
        """
        This method will fetch the contents of the page.
        """
        r = requests.get(urlparse.urljoin(_ROOT_, self.clean_url(url)))
        return r.text

    def extract_urls(self, text) :
        """
        This method will take the contents of a page and extract all of the URLs on it
        """
        urls = []
        soup = BeautifulSoup(text, 'html.parser')
        for atag in soup.find_all('a'):
            # get all links within the page
            urls.append(atag.get('href'))
        return urls

    def external_link(self, url) :
        """
        This method will check if the URL is an external link outside the root domain
        """
        if re.compile('.+lyle.smu.edu/~fmoore/.+').match(url):
            return False
        elif re.compile('mailto:').match(url) :
            return True
        else :
            if requests.get(_ROOT_ + url).status_code == 200 :
                return False
            else :
                return True

    def jpeg_link(self, url) :
        """
        This method will check if the link is a JPEG
        """
        if re.compile('.*.jpg').match(url):
            return True
        else :
            return False

    def broken_link(self, url) :
        """
        This method will check if the link is broken.
        """
        if requests.get(_ROOT_ + self.clean_url(url)).status_code == 200 :
            return False
        else :
            return True



    def crawl(self) :
        """
        This is the main worker method. It will parse the urls, add the words to
        the index, get the next links, and continue looping through the queue.
        """

        parser = robotparser.RobotFileParser()
        parser.set_url(urlparse.urljoin(_ROOT_, 'robots.txt'))
        parser.read()

        # Add _ROOT_ url to queue
        urlqueue = [_ROOT_]

        # visited, external, jpeg, and broken links
        visited, external, jpeg, broken = [], [], [], []

        while urlqueue :
            # get flast element in urlqueue
            url = urlqueue.pop(-1)
            print url

            # check if we can fetch the page first
            if parser.can_fetch('*', urlparse.urljoin('/', url)) :
                # fetch the page
                page = self.fetch(url)

                # add page to visited links
                visited.append(url)

                # get urls from page
                new_urls = self.extract_urls(page)
                for new_url in new_urls :
                    # check if we have already visited it or are going to
                    if new_url not in visited and new_url not in urlqueue and new_url not in jpeg :
                        # check if it is an external link
                        if self.external_link(new_url) :
                            external.append(new_url)
                        elif self.jpeg_link(new_url) :
                            jpeg.append(new_url)
                        elif self.broken_link(new_url) :
                            broken.append(new_url)
                        else :
                            urlqueue.append(new_url)
        

        # print self.broken_link('http://lyle.smu.edu/~fmoore/misc/urlexample1.htm')

                ####################### ADD TO INDEX HERE #######################

            # end if
        # end while
        print 'VISITED'
        print visited
        print
        print 'EXTERNAL'
        print external
        print
        print 'JPEG'
        print jpeg
        print
        print 'BROKEN'
        print broken
        print

    # end crawl method
# end crawler class


###########    Main method    ###########
if __name__ == "__main__":
    crawler = Crawler()
    crawler.crawl()

#########################################
