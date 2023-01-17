import glob
import pytz
from bs4 import BeautifulSoup
from datetime import datetime


PATH = 'input/sovcombank'
FILENAMES = glob.glob(PATH + '/*.html')


def get_sovcom_transactions():
    transactions = []
    for filename in FILENAMES:
        with open(filename, 'r', encoding='UTF-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            table = soup.find_all('table')[1]
            trs = table.find_all('tr')[1:]
            for tr in trs:
                tds = tr.find_all('td')
                transactions.append({
                    'bank': 'Sovcom',
                    'trans_datetime': datetime.strptime(tds[0].find('p').get_text(), '%d.%m.%y').astimezone(pytz.UTC),
                    'account': tds[1].find('p').get_text(),
                    'income_balance': float(tds[2].find('p').get_text().replace(',', '')),
                    'debit': float(tds[3].find('p').get_text().replace(',', '')),
                    'credit': float(tds[4].find('p').get_text().replace(',', '')),
                    'text': tds[5].find('p').get_text()
                })

    return transactions


if __name__ == '__main__':
    print(get_sovcom_transactions())
