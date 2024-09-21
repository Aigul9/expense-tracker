import glob
import re
from datetime import datetime
from unidecode import unidecode

import fitz


PATH = '../input/sber'
FILENAMES = glob.glob(PATH + '/*.pdf')


def get_transactions():
    transactions = []

    for filename in FILENAMES:
        file = fitz.open(filename)
        pat_date = re.compile(r'(\d{2}.\d{2}.\d{4})')
        pat_time = re.compile(r'(\d{2}:\d{2})')
        num_fields = 8

        for page in file:
            rows = page.get_text().split('\n')
            i = 11

            while i < len(rows) - 1:

                if rows[i] == 'Продолжение на следующей странице'\
                        or 'Дергунова К. А.' in rows[i]:
                    break

                date = rows[i][:10]
                time = rows[i + 1][:5]

                if pat_date.search(date) and pat_time.search(time):
                    trans_date, trans_time, auth_code, category, trans_sum_str, _, transfer_date, text = rows[i:i + num_fields]

                    trans_sum_str = unidecode(trans_sum_str).replace(' ', '').replace(',', '.')
                    trans_sum = float(trans_sum_str)

                    debit = trans_sum if trans_sum_str[0] == '+' else 0
                    credit = trans_sum if trans_sum_str[0] != '+' else 0

                    transaction = {
                        'bank': 'Sber',
                        'trans_datetime': datetime.strptime(' '.join((trans_date, trans_time)),
                                                            '%d.%m.%Y %H:%M'),
                        'transfer_datetime': datetime.strptime(transfer_date, '%d.%m.%Y'),
                        'auth_code': auth_code,
                        'category': category,
                        'debit': debit,
                        'credit': credit,
                        'text': text
                    }

                    transactions.append(transaction)
                    i += num_fields
                else:
                    if len(transactions) != 0:
                        transactions[-1]['text'] += ' ' + rows[i]
                    i += 1

    return transactions


if __name__ == '__main__':
    print(get_transactions())
