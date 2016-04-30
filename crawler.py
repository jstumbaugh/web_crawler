import requests, robotparser, urlparse, re, os, string, sys, operator
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
from time import localtime, strftime
from stemmer import PorterStemmer
from collections import Counter
from math import log10

_ROOT_ = 'http://lyle.smu.edu/~fmoore/'

class MLStripper(HTMLParser):
    """
    Author: Nicole

    This class removes the HTML tags from raw HTML text.
    http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
    """
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    """
    Author: Nicole

    This class removes the HTML tags from raw HTML text.
    http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
    """
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class Crawler:

    def __init__(self):
    	"""
    	Author: Nicole

    	This method declares the list stopwords, dictionaries all_words and
    	all_words_freq, as well as the PorterStemmer object.
    	"""
        self.stopwords = []
        self.p = PorterStemmer()
        self.all_words = {}
        self.all_words_freq = {}
        self.tfidf = {}

    def clean_url(self, url) :
        """
        Author: Jason

        This method removes the base url
        EX. http://lyle.smu.edu/~fmoore/schedule.htm => schedule.htm
        """
        url = re.compile(_ROOT_).sub('', url)
        url = re.compile('http://lyle.smu.edu/~fmoore').sub('', url)
        url = re.compile('index.*').sub('', url)
        url = re.compile('.*.gif').sub('', url)
        return re.compile('\.\./').sub('', url)

    def fetch(self, url) :
        """
        Author: Jason

        This method will fetch the contents of the page.
        """
        r = requests.get(urlparse.urljoin(_ROOT_, self.clean_url(url)))
        return r.text

    def extract_urls(self, text) :
        """
        Author: Jason

        This method will take the contents of a page and extract all of the URLs on it
        """
        urls = []
        soup = BeautifulSoup(text, 'html.parser')
        for atag in soup.find_all('a'):
            urls.append(atag.get('href'))
        for img in soup.find_all('img'):
            urls.append(img.get('src'))
        return urls

    def external_link(self, url) :
        """
        Author: Jason

        This method will check if the URL is an external link outside the root domain
        """
        if url :
            url = re.compile('https*://').sub('', url)
            if re.compile('.*lyle.smu.edu/~fmoore.*').match(url) :
                return False
            elif re.compile('www.*').match(url) :
                return True
            elif re.compile('java-source.*').match(url) :
                return True
            elif re.compile('.*smu.edu.*').match(url) :
                return True
            elif re.compile('.*.aspx').match(url) :
                return True
            elif re.compile('mailto:').match(url) :
                return True
            elif re.compile('.*.xlsx').match(url) :
                return False
            elif requests.get(_ROOT_ + url).status_code == 200 :
                return False
            elif self.jpeg_link(url) :
                return False
            else :
                return True
        else :
            return True

    def jpeg_link(self, url) :
        """
        Author: Jason

        This method will check if the link is a JPEG
        """
        return True if re.compile('.*.jpg').match(url) else False

    def broken_link(self, url) :
        """
        Author: Jason

        This method will check if the link is broken.
        """
        return False if requests.get(_ROOT_ + self.clean_url(url)).status_code == 200 else True

    def excel_link(self,url) :
        """
        Author: Jason

        This method will check if the link is an excel file.
        """
        return True if re.compile('.*.xlsx').match(url) else False

    def add_root_to_links(self, urls) :
        """
        Author: Jason

        This method will add the root URL to all of the links for visual apperance
        """
        new_urls = [_ROOT_ + re.compile('http://lyle.smu.edu/~fmoore/').sub('', link) for link in urls]
        # del new_urls[-1] # http://lyle.smu.edu/~fmoore//
        # del new_urls[-1] # http://lyle.smu.edu/~fmoore/#
        return new_urls

    def remove_extra_whitespace(self, text) :
        """
        Author: Nicole

        This method removes more than one white space between words.
        """
        p = re.compile(r'\s+')
        return p.sub(' ', text)

    def remove_punctuation(self, text) :
        """
        Author: Nicole

        This method uses regex to remove the punctuation in text.
        http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
        """
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def load_stop_words(self, file) :
        """
        Author: Nicole

        This method stores the list of stopwords from a file to the class
        variable list self.stopwords.
        """
        self.stopwords = [line.rstrip('\n') for line in open(file)]

    def prepare_text(self, text) :
        """
        Author: Nicole

        This method prepares the raw HTML text for it to be indexed by lowering
        the letters, removing the HTML tags, removing the punctuation, removing
        the extra white space, changing the list to ASCII from unicode, removing
        the stop words, and stemming each word.
        """
        text = strip_tags(text.lower())
        text = self.remove_punctuation(text)
        text = self.remove_extra_whitespace(text)
        text = [word.encode('UTF8') for word in text.split()]
        text = [word for word in text if word not in self.stopwords]
        text = self.p.stem_word(text)
        return text

    def index(self, url, doc_words) :
        """
        Author: Nicole

        This method indexes all the words in a document and keeps track of
        the frequency of a word in overall documents and overall occurrences.
        """
        for key in doc_words :
            if key not in self.all_words:
                self.all_words[key] = [(url, doc_words[key])]
                self.all_words_freq[key] = [1, doc_words[key]]
            else:
                self.all_words[key].append((url, doc_words[key]))
                self.all_words_freq[key][0] += 1
                self.all_words_freq[key][1] += doc_words[key]

    def calTFIDF(self, word, visited) :
        """
        Author: Nicole

        This method will calculate the TF-IDF for a given word.

        1 + log(number of times word appears in a document) * log(total documents/ how many documents the word appears in)
        """
        for i in self.all_words[word] :
            #return i[1] * log10(len(visited)/self.all_words_freq[word][0])
            return (1 + log10(i[1])) * log10(len(visited)/self.all_words_freq[word][0])

    def write_output(self, visited, external, jpeg, broken, dictionary) :
        """
        Author: Jason and Nicole but mostly Jason except for lines 211 - 213

        This method will write the output of the crawler and the 20 most common words to output.txt
        """
        dictionary = sorted(dictionary.items(), key=lambda e: e[1][1], reverse=True)[:20]

        f = open('output.txt', 'w')
        f.write('Output of Jason and Nicole\'s web crawler.\n')
        f.write('Current Time: ')
        f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()))
        f.write('\n\n')

        # Visited links
        f.write('Visted Links: (' + str(len(visited)) + ' total)\n')
        for link in visited :
            f.write(link + '\n')
        f.write('\n')

        # External links
        f.write('External Links: (' + str(len(external)) + ' total)\n')
        for link in external :
            f.write(link + '\n')
        f.write('\n')

        # JPEG links
        f.write('JPEG Links: (' + str(len(jpeg)) + ' total)\n')
        for link in jpeg :
            f.write(link + '\n')
        f.write('\n')

        # Broken links
        f.write('Broken Links: (' + str(len(broken)) + ' total)\n')
        for link in broken :
            f.write(link + '\n')
        f.write('\n')

        # Term Frequency
        f.write('Top 20 Most Common Words with Document Frequency\n')
        for i in dictionary:
            f.write('The term ' + i[0] + ' occurs ' + str(i[1][1]) + ' times in ' + str(i[1][0]) + ' documents.\n')

        f.close()

    def clean_external_links(self, external) :
        """
        Author: Jason

        This method will cremove the non links from the external links
        """
        urls = []
        for link in external :
            if link == None :
                return urls
            else :
                urls.append(link)
        return urls

    def query_engine(self):
        """
        Author: Jason

        This method will be the main query handler.
        self.all_words format: [('spring'), [('url', 3), ('other_page', 4)] ]
                                   word         tuples(url, frequency)
        """
        print "#################################################################"
        print "################ Jason and Nicoles' Web Crawler #################"
        print "#################################################################"
        print
        print "Please enter a query to search the lyle.smu.edu/~fmoore domain."
        print "Type 'quit' to exit the search engine"
        user_input = ""
        while True :
            user_input = raw_input("> ")
            if user_input == "quit" or user_input == "Quit" or user_input == "QUIT":
                break
            words = self.p.stem_word(re.sub("[^\w]", " ",  user_input).split())
            common_docs = []
            for word in words :
                info = self.all_words.get(word)
                if info :
                    for tup in info :
                        if tup[0] not in common_docs:
                            common_docs.append(tup[0])
            print common_docs
        return


    def crawl(self, pages_to_index) :
        """
        Author: Jason and Nicole

        This is the main worker method. It will parse the urls, add the words to
        the index, get the next links, and continue looping through the queue until
        the number of pages to index is met.
        """

        parser = robotparser.RobotFileParser()
        parser.set_url(urlparse.urljoin(_ROOT_, 'robots.txt'))
        parser.read()

        # Add _ROOT_ url to queue
        urlqueue = [_ROOT_]

        # visited, external, jpeg, and broken links
        visited, external, jpeg, broken = [], [], [], []

        # pages indexd
        pages_indexed = 0

        while urlqueue:
            # get flast element in urlqueue
            url = urlqueue.pop(-1)
            if self.clean_url(url) in visited:
                continue

            # check if we can fetch the page first
            if parser.can_fetch('*', urlparse.urljoin('/', url)) :

                # remove the / at the beginning of the string
                url = re.compile('^/').sub('',url)

                # fetch the page
                page = self.fetch(url)

                # add page to visited links
                visited.append(self.clean_url(url))

                # get urls from page
                new_urls = self.extract_urls(page)

                for new_url in new_urls :
                    # check if we have already visited it or are going to
                    if new_url not in visited and new_url not in urlqueue and new_url not in jpeg and new_url not in broken and new_url not in external :
                        if self.external_link(new_url) :
                            external.append(new_url)
                        elif self.jpeg_link(new_url) :
                            jpeg.append(new_url)
                        elif self.excel_link(new_url) :
                            visited.append(new_url)
                        elif self.broken_link(new_url) :
                            broken.append(new_url)
                        else :
                            urlqueue.append(new_url)

                # checks to see if url is parsable aka .html, .htm, .txt
                # if yes, then parse and index; if no, pass
                filename, file_extension = os.path.splitext(url)
                if not (file_extension == ".pdf" or file_extension == ".pptx") :
                    pagetext = requests.get(_ROOT_ + self.clean_url(url))
                    pagetext = pagetext.text
                    cleantext = self.prepare_text(pagetext)
                    doc_words = Counter(cleantext)
                    self.index(url, doc_words)

                # increment the pages indexed
                pages_indexed += 1
                if int(pages_indexed) >= int(pages_to_index):
                    break
            # end if
        # end while

        # clean the links for visual appearance
        visited = set(self.add_root_to_links(visited))
        jpeg = self.add_root_to_links(jpeg)
        broken = self.add_root_to_links(broken)
        external = self.clean_external_links(external)

        # write to output file
        self.write_output(visited, external, jpeg, broken, self.all_words_freq)

        # query engine prepare_text
        self.query_engine()

    # end crawl method
# end crawler class


###########    Main method    ###########
if __name__ == "__main__":
    crawler = Crawler()
    crawler.load_stop_words('stopwords.txt')
    # if an argument is passed in, use it to crawl
    # else use 100 to get all the pages in the domain
    if len(sys.argv) == 2 :
        crawler.crawl(sys.argv[1])
    else :
        crawler.crawl(30)

#########################################
