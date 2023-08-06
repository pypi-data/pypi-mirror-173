# About
---

Wscrape is a package that allows you to quickly scrape things off a website. Other utils have been added for debugging. Check [Pyutils-cr](https://pypi.org/project/pyutils-cr/) for more debugging/info on the other functions included.

# Examples
---

Scrape information on Cars off Wikipedia
```py
import requests
from bs4 import BeautifulSoup
from wscrape import Scrape

#variable=input("What word would you like to search: ")
url = "https://en.wikipedia.org/wiki/Cars_(film)"
f = Scrape()
f.qresult(f.page_content(url))
y = f.relems("i","lang","la")
print(y.text)

#Returns content of provided tags
```

Retrieve content from a website
```py
import wscrape.scrape.misc as req

print(req.rcontent("abcdefg.com"))

#Returns string
```

Scan the website for a specific element
```py
import wscrape.etc.misc.scan_elems as scan_elem

print(scan_elem("https://en.wikipedia.org/wiki/Cars_(film)", "i", "lang", "la")

#Returns Bool
```
[Github](https://github.com/GoodMusic8596/wscrape)