import glob
import re
from datetime import datetime
from unidecode import unidecode

import fitz


PATH = '../input/sber/account'
FILENAMES = glob.glob(PATH + '/*.pdf')


def get_transactions():
    transactions = []

    for filename in FILENAMES:
        file = fitz.open(filename)
        pat_date = re.compile(r'(\d{2}\.\d{2}\.\d{4})')
        num_fields = 6

        for page in file:
            rows = page.get_text().split('\n')
            i = 0  # start row id

            while i < len(rows) - 1:

                print(i)

                if rows[i] == 'Продолжение на следующей странице'\
                        or 'Дергунова К. А.' in rows[i]:
                    break

                date = rows[i][:10]

                if pat_date.search(date):
                    trans_date, category, account, text, trans_sum_str, income_balance_str = rows[i:i + num_fields]
                    print(rows[i:i + num_fields])
                    trans_sum_str = unidecode(trans_sum_str).replace(' ', '').replace(',', '.')

                    try:
                        trans_sum = float(trans_sum_str)
                    except ValueError:
                        i += 1
                        continue

                    income_balance_str = unidecode(income_balance_str).replace(' ', '').replace(',', '.')
                    income_balance = float(income_balance_str)

                    debit = trans_sum if trans_sum_str[0] == '+' else 0
                    credit = trans_sum if trans_sum_str[0] != '+' else 0

                    transaction = {
                        'bank': 'Sber',
                        'trans_datetime': datetime.strptime(trans_date, '%d.%m.%Y'),
                        'category': category,
                        'account': account,
                        'income_balance': income_balance,
                        'debit': debit,
                        'credit': -credit,
                        'text': text
                    }

                    transactions.append(transaction)
                    i += num_fields
                else:
                    i += 1

    return transactions


if __name__ == '__main__':
    print(get_transactions())
