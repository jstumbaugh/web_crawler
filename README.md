## CSE 5337 Web Crawler Project
A web crawler and idexer using python.

## Used Software
This project has been developed on a mid-2012 Macbook Pro running OS X Yosemite (10.10.5).


## Installation
You can clone this repository to gain access to the code of the project.

```
git clone https://github.com/jstumbaugh/web_crawler.git
```

## Execution
To excute the project:
```
~/webcrawler/$ python crawler.py $PAGES_TO_CRAWL
```
where $PAGES_TO_CRAWL is a number of the pages you wish to have the web crawler crawl.


## Query engine
When executed, the web crawler will also execute a query engine to search for words in the domain http://lyle.smu.edu/~fmoore/. The output is as follows:
```
#################################################################
################ Jason and Nicoles' Web Crawler #################
#################################################################

Please enter a query to search the lyle.smu.edu/~fmoore domain.
Search will display top 5 results or all results that query is found on.
Type 'quit' to exit the search engine
> moore smu
  Score:      Document:
   2.346721    http://lyle.smu.edu/~fmoore/
   1.079181    http://lyle.smu.edu/~fmoore/schedule.htm

> Bob Ewell where Scout
Bob Ewell where Scout not found in domain.

> three year story
  Score:      Document:
   1.938249    http://lyle.smu.edu/~fmoore/misc/mockingbird4.html
   1.938249    http://lyle.smu.edu/~fmoore/misc/mockingbird1.html
   1.381049    http://lyle.smu.edu/~fmoore/misc/mockingbird2.html
   0.778151    http://lyle.smu.edu/~fmoore/misc/mockingbird5.html

> Atticus to defend Maycomb
  Score:      Document:
   2.790898    http://lyle.smu.edu/~fmoore/misc/mockingbird4.html
   2.132079    http://lyle.smu.edu/~fmoore/misc/mockingbird1.html
   1.534323    http://lyle.smu.edu/~fmoore/misc/mockingbird2.html
   1.480892    http://lyle.smu.edu/~fmoore/misc/mockingbird3.html
   1.480892    http://lyle.smu.edu/~fmoore/misc/mockingbird5.html

> project example teams
  Score:      Document:
   2.701308    http://lyle.smu.edu/~fmoore/schedule.htm
   1.991195    http://lyle.smu.edu/~fmoore/misc/projectteams.htm
   1.289668    http://lyle.smu.edu/~fmoore/misc/excel-examples.html
   1.289668    http://lyle.smu.edu/~fmoore/misc/urlexample1.htm
   1.289668    http://lyle.smu.edu/~fmoore/misc/k-means.htm
```

## Dependencies

### Python 2.7

### BeautifulSoup

### Requests

### sklearn

### scipy
