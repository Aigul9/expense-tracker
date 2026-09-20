import glob
from datetime import datetime

import numpy as np
import pandas as pd


PATH = '../input/tinkoff'


def get_transactions():
    filenames = glob.glob(PATH + '/*.csv')
    transactions = []

    for filename in filenames:
        df = (
            pd.read_csv(filename, header=0, delimiter=';')
            .replace('nan', np.nan)
            .replace({pd.NaT: None})
            .fillna('')
        )

        print(df)

        for _, row in df.iterrows():
            (
                account_name, pan, trans_datetime, trans_sum, trans_currency,
                pay_sum, pay_currency, status, category, my_category,
                mcc, text, message, rounding, sum_with_rounding,
                bonus, is_accounted
            ) = row
            trans_sum = float(trans_sum.replace(',', '.'))
            pay_sum = float(pay_sum.replace(',', '.'))
            rounding = float(rounding.replace(',', '.'))
            sum_with_rounding = float(sum_with_rounding.replace(',', '.'))
            bonus = float(bonus.replace(',', '.'))

            transaction = {
                'bank': 'Tinkoff',
                'trans_datetime': datetime.strptime(trans_datetime, '%d.%m.%Y %H:%M:%S'),
                'pan': pan,
                'status': status,
                'debit': trans_sum if trans_sum > 0 else 0,
                'credit': -trans_sum if trans_sum < 0 else 0,
                'trans_currency': trans_currency,
                'pay_sum': pay_sum,
                'pay_currency': pay_currency,
                'cashback': bonus,
                'category': category,
                'mcc': str(mcc).replace('.0', ''),
                'text': text,
                'bonus': bonus,
                'rounding': rounding,
                'sum_with_rounding': sum_with_rounding
            }

            transactions.append(transaction)

    return transactions


if __name__ == '__main__':
    print(get_transactions())
