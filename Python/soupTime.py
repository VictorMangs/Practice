import requests
from bs4 import BeautifulSoup

def getClasses(soup):
    class_list =set()
    tags = {tag.name for tag in soup.find_all()}
    
    # iterate all tags
    for tag in tags:
    
        # find all element of tag
        for i in soup.find_all(tag):
    
            # if tag has attribute of class
            if i.has_attr( "class" ):
    
                if len(i['class']) != 0:
                    class_list.add(" ".join( i['class']))
    
    print(class_list)

URL = 'https://www.telegraph.co.uk/news/2023/05/25/chinese-df27-hypersonic-missile-us-aircraft-carriers/'
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
getClasses(soup)


