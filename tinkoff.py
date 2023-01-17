import glob
import PyPDF2
import pytz
import re
from datetime import datetime

PATH = 'input/tinkoff'
FILENAMES = glob.glob(PATH + '/*.pdf')


def get_tinkoff_transactions():
    transactions = []
    for filename in FILENAMES:
        with open(filename, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            pat_date = re.compile(r'(\d{2}.\d{2}.\d{4})')
            trans_datetime = slice(16)
            transfer_date = slice(17, 27)
            last_date_idx = 27
            for i in range(num_pages):
                page = reader.pages[i]
                for row in page.extract_text().split('\n'):
                    date = row[:10]
                    if pat_date.search(date):
                        trans_sum, card_sum, text = [line.strip() for line in row[last_date_idx:].split('₽')]
                        trans_sum = float(trans_sum.replace(' ', '').replace(',', '.'))
                        card_sum = float(card_sum.replace(' ', '').replace(',', '.'))
                        transactions.append({
                            'bank': 'Tinkoff',
                            'trans_datetime': datetime.strptime(row[trans_datetime], '%d.%m.%Y %H:%M').astimezone(pytz.UTC),
                            'transfer_datetime': datetime.strptime(row[transfer_date], '%d.%m.%Y').astimezone(pytz.UTC),
                            'debit': trans_sum if trans_sum > 0 else 0,
                            'credit': -trans_sum if trans_sum < 0 else 0,
                            'card_sum': card_sum,
                            'text': text
                        })
    return transactions


if __name__ == '__main__':
    print(get_tinkoff_transactions())
