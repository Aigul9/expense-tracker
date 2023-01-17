import fitz
import glob
import pytz
import re
from datetime import datetime
from unidecode import unidecode


PATH = 'input/sber'
FILENAMES = glob.glob(PATH + '/*.pdf')


def get_sber_transactions():
    transactions = []
    for filename in FILENAMES:
        file = fitz.open(filename)
        pat_date = re.compile(r'(\d{2}.\d{2}.\d{4})')
        pat_time = re.compile(r'(\d{2}:\d{2})')
        for page in file:
            rows = page.get_text().split('\n')
            i = 0
            while i < len(rows) - 1:
                date = rows[i][:10]
                time = rows[i + 1][:5]
                if pat_date.search(date) and pat_time.search(time):
                    trans_date = rows[i]
                    trans_time = rows[i + 1]
                    transfer_date = rows[i + 2]
                    auth_code = rows[i + 3]
                    category = rows[i + 4]
                    text = rows[i + 5]
                    try:
                        trans_sum_str = unidecode(rows[i + 6]).replace(' ', '').replace(',', '.')
                        trans_sum = float(trans_sum_str)
                    except ValueError:
                        text += rows[i + 6]
                        trans_sum_str = unidecode(rows[i + 7]).replace(' ', '').replace(',', '.')
                        trans_sum = float(trans_sum_str)
                        i += 1
                    transactions.append({
                        'bank': 'Sber',
                        'trans_datetime': datetime.strptime(' '.join((trans_date, trans_time)), '%d.%m.%Y %H:%M').astimezone(pytz.UTC),
                        'transfer_datetime': datetime.strptime(transfer_date, '%d.%m.%Y').astimezone(pytz.UTC),
                        'auth_code': auth_code,
                        'category': category,
                        'text': text,
                        'debit': trans_sum if trans_sum_str[0] == '+' else 0,
                        'credit': trans_sum if trans_sum_str[0] != '+' else 0
                    })
                    i += 7
                else:
                    i += 1
    return transactions


if __name__ == '__main__':
    print(get_sber_transactions())
