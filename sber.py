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
        num_fields = 7
        for page in file:
            rows = page.get_text().split('\n')
            i = 0
            while i < len(rows) - 1:
                date = rows[i][:10]
                time = rows[i + 1][:5]
                if pat_date.search(date) and pat_time.search(time):
                    trans_date, trans_time, transfer_date, auth_code, category, text = rows[i:i + num_fields - 1]
                    try:
                        trans_sum_str = unidecode(rows[i + num_fields - 1]).replace(' ', '').replace(',', '.')
                        trans_sum = float(trans_sum_str)
                    except ValueError:
                        text += rows[i + num_fields - 1]
                        trans_sum_str = unidecode(rows[i + num_fields]).replace(' ', '').replace(',', '.')
                        trans_sum = float(trans_sum_str)
                        i += 1
                    transactions.append({
                        'bank': 'Sber',
                        'trans_datetime': datetime.strptime(' '.join((trans_date, trans_time)),
                                                            '%d.%m.%Y %H:%M').astimezone(pytz.UTC),
                        'transfer_datetime': datetime.strptime(transfer_date, '%d.%m.%Y').astimezone(pytz.UTC),
                        'auth_code': auth_code,
                        'category': category,
                        'debit': trans_sum if trans_sum_str[0] == '+' else 0,
                        'credit': trans_sum if trans_sum_str[0] != '+' else 0,
                        'text': text
                    })
                    i += num_fields
                else:
                    i += 1

    return transactions


if __name__ == '__main__':
    print(get_sber_transactions())
