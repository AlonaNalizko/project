from urllib.request import urlopen
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html"

page = urlopen(URL)

bs = BeautifulSoup(page.read(), "html.parser")
allBooks = bs.findAll("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

allDescriptions = []

def get_description(book):
    url = "https://books.toscrape.com/catalogue/" + book.find("a")["href"].split("../../../")[1]
    page = urlopen(url)
    soup = BeautifulSoup(page.read(), "html.parser")

    data = soup.find('article', class_="product_page")
    title = data.find('div', class_="col-sm-6 product_main").h1.text

    return (data.contents[7].text, title)
for book in allBooks:
    allDescriptions.append(get_description(book))

def get_shotrest_description(descriptions):
    shortest_description = descriptions[0][0]
    title_we_need = ""
    for description, title in descriptions:
        if len(description) < len(shortest_description):
            shortest_description = description
            title_we_need = title
    return title_we_need

answer = get_shotrest_description(allDescriptions)

print(answer)
