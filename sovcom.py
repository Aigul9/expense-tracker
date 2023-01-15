from bs4 import BeautifulSoup

path = 'input/sovcombank/statement.html'
with open(path, 'r', encoding='UTF-8') as file:
    soup = BeautifulSoup(file, 'html.parser')
    table = soup.find_all('table')[1]
    trs = table.find_all('tr')[1:]
    for tr in trs:
        tds = tr.find_all('td')
        for td in tds:
            print(td.find('p').get_text())
