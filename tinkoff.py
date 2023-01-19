import glob
import PyPDF2
import pytz
import re
from datetime import datetime

PATH = 'input/tinkoff'


def get_tinkoff_transactions():
    filenames = glob.glob(PATH + '/*.pdf')
    transactions = []
    for filename in filenames:
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
                        transaction = {
                            'bank': 'Tinkoff',
                            'trans_datetime': datetime.strptime(row[trans_datetime], '%d.%m.%Y %H:%M').astimezone(
                                pytz.UTC),
                            'transfer_datetime': datetime.strptime(row[transfer_date], '%d.%m.%Y').astimezone(pytz.UTC),
                            'debit': trans_sum if trans_sum > 0 else 0,
                            'credit': -trans_sum if trans_sum < 0 else 0,
                            'card_sum': card_sum,
                            'text': text
                        }
                        if transaction not in transactions:
                            transactions.append(transaction)

    return transactions


def get_tinkoff_transactions_txt():
    filenames = glob.glob(PATH + '/*.txt')
    transactions = []
    for filename in filenames:
        with open(filename, 'r', encoding='UTF-16') as file:
            next(file)
            for line in file:
                line = line.rstrip().split('\t')
                trans_datetime, transfer_datetime, pan, status, \
                trans_sum, trans_currency, pay_sum, pay_currency, \
                cashback, category, mcc, text, bonus, rounding, sum_with_rounding = line
                trans_sum = float(trans_sum.replace(',', '.'))
                pay_sum = float(pay_sum.replace(',', '.'))
                transaction = {
                    'bank': 'Tinkoff',
                    'trans_datetime': datetime.strptime(trans_datetime, '%d.%m.%Y %H:%M:%S').astimezone(
                                pytz.UTC),
                    'transfer_datetime': None if transfer_datetime == ''
                    else datetime.strptime(transfer_datetime, '%d.%m.%Y').astimezone(pytz.UTC),
                    'pan': pan,
                    'status': status,
                    'debit': trans_sum if trans_sum > 0 else 0,
                    'credit': -trans_sum if trans_sum < 0 else 0,
                    'trans_currency': trans_currency,
                    'pay_sum': pay_sum,
                    'pay_currency': pay_currency,
                    'cashback': cashback,
                    'category': category,
                    'mcc': mcc,
                    'text': text,
                    'bonus': float(bonus.replace(',', '.')),
                    'rounding': float(rounding.replace(',', '.')),
                    'sum_with_rounding': float(sum_with_rounding.replace(',', '.'))
                }
                if transaction not in transactions:
                    transactions.append(transaction)
    return transactions


if __name__ == '__main__':
    # print(get_tinkoff_transactions())
    get_tinkoff_transactions_txt()
