import glob
import re
from datetime import datetime

import fitz

PATH = '../input/vtb'
FILENAMES = glob.glob(PATH + '/*.pdf')


def get_transactions():
    transactions = []

    for filename in FILENAMES:
        file = fitz.open(filename)
        pat_date = re.compile(r'(\d{2}\.\d{2}\.\d{4})')
        pat_time = re.compile(r'(\d{2}:\d{2}:\d{2})')
        pat_sum = re.compile(r'(\d+\sRUB)')
        num_fields = 7
        idx_transfer_date = 2

        for page in file:
            rows = page.get_text().split('\n')
            i = 0

            while i < len(rows) - 1:
                date, time = rows[i], rows[i + 1]
                trans_date, trans_time = None, None

                if pat_date.search(date) and pat_time.search(time) and len(date) == 10 and len(time) == 8:
                    trans_date, trans_time = date, time
                elif pat_date.search(date) and pat_sum.search(time):
                    i -= idx_transfer_date
                else:
                    i += 1
                    continue

                transfer_date, card_sum, debit, credit, text = rows[i + idx_transfer_date:i + num_fields]
                next_col = i + num_fields

                while next_col < len(rows) - 2 and not (pat_date.search(rows[next_col]) and len(rows[next_col]) == 10):
                    text = ' '.join((text, rows[next_col]))
                    next_col += 1

                transaction = {
                    'bank': 'VTB',
                    'trans_datetime': datetime.strptime(
                        ' '.join((trans_date, trans_time)),
                        '%d.%m.%Y %H:%M:%S') if trans_date is not None else None,
                    'transfer_datetime': datetime.strptime(transfer_date, '%d.%m.%Y'),
                    'card_sum': float(card_sum.replace(' RUB', '')),
                    'debit': float(debit),
                    'credit': float(credit),
                    'text': text[1:].replace(' Спасибо, что Вы с нами! Всегда Ваш, Банк ВТБ (ПАО)', '').strip()
                }

                transactions.append(transaction)

                i = next_col

    return transactions


if __name__ == '__main__':
    print(get_transactions())
