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
        num_fields = 7

        for page in file:
            rows = page.get_text().split('\n')
            is_debit_card = 1 if 'дебетовой карты' in ''.join(rows).lower() else 0
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

                    if is_debit_card:
                        debit = trans_sum if trans_sum_str[0] == '+' else 0
                        credit = trans_sum if trans_sum_str[0] != '+' else 0
                    else:
                        debit = trans_sum if trans_sum_str[0] != '-' else 0
                        credit = abs(trans_sum) if trans_sum_str[0] == '-' else 0

                    transaction = {
                        'bank': 'Sber',
                        'trans_datetime': datetime.strptime(' '.join((trans_date, trans_time)),
                                                            '%d.%m.%Y %H:%M'),
                        'transfer_datetime': datetime.strptime(transfer_date, '%d.%m.%Y'),
                        'auth_code': auth_code,
                        'category': category if is_debit_card else text,
                        'debit': debit,
                        'credit': credit,
                        'text': text if is_debit_card else category
                    }

                    transactions.append(transaction)
                    i += num_fields

                else:
                    i += 1

    return transactions


if __name__ == '__main__':
    print(get_transactions())
