import glob
from datetime import datetime

import numpy as np
import pandas as pd


PATH = '../input/tinkoff'


def get_transactions():
    filenames = glob.glob(PATH + '/*.xls')
    transactions = []

    for filename in filenames:
        df = pd.read_excel(filename, sheet_name='Отчет по операциям', header=0).replace('nan', np.nan).fillna('')

        for _, row in df.iterrows():
            (
                trans_datetime, transfer_datetime, pan, status,
                trans_sum, trans_currency, pay_sum, pay_currency,
                cashback, category, mcc, text, bonus, rounding, sum_with_rounding
            ) = row
            trans_sum = float(trans_sum)
            pay_sum = float(pay_sum)

            transaction = {
                'bank': 'Tinkoff',
                'trans_datetime': datetime.strptime(trans_datetime, '%d.%m.%Y %H:%M:%S'),
                'transfer_datetime': None if transfer_datetime == ''
                else datetime.strptime(transfer_datetime, '%d.%m.%Y'),
                'pan': pan,
                'status': status,
                'debit': trans_sum if trans_sum > 0 else 0,
                'credit': -trans_sum if trans_sum < 0 else 0,
                'trans_currency': trans_currency,
                'pay_sum': pay_sum,
                'pay_currency': pay_currency,
                'cashback': str(cashback),
                'category': category,
                'mcc': str(mcc).replace('.0', ''),
                'text': text,
                'bonus': float(bonus),
                'rounding': float(rounding),
                'sum_with_rounding': float(sum_with_rounding)
            }

            transactions.append(transaction)

    return transactions


if __name__ == '__main__':
    print(get_transactions())
