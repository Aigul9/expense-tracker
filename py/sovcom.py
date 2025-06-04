import glob
import re
from datetime import datetime
from unidecode import unidecode

import fitz


PATH = '../input/sovcombank'
FILENAMES = glob.glob(PATH + '/*.pdf')


def get_transactions():
    transactions = []

    for filename in FILENAMES:
        file = fitz.open(filename)
        pat_date = re.compile(r'(\d{2}\.\d{2}\.\d{2})')
        num_fields = 6

        for page in file:
            rows = page.get_text().split('\n')
            i = 0  # first table row id

            while i < len(rows) - 1:

                date = rows[i][:8]

                if pat_date.search(date):
                    trans_date, account, income_balance, debit, credit, text = rows[i:i + num_fields]
                    print(rows[i:i + num_fields])

                    income_balance = unidecode(income_balance).replace(',', '')
                    income_balance = float(income_balance)

                    debit = unidecode(debit).replace(',', '')
                    debit = float(debit)

                    credit = unidecode(credit).replace(',', '')
                    credit = float(credit)

                    transaction = {
                        'bank': 'Sovcom',
                        'trans_datetime': datetime.strptime(trans_date, '%d.%m.%y'),
                        'account': account,
                        'income_balance': income_balance,
                        'debit': credit,
                        'credit': debit,
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
