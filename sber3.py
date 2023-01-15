import fitz
import re

from unidecode import unidecode

# проверять записи на дубликаты - upsert
doc = fitz.open('input/sber/2019.pdf')
pat_date = re.compile(r'(\d{2}.\d{2}.\d{4})')
res_list = []
for page in doc:
    page_list = page.get_text().split('\n')
    i = 0
    while i < len(page_list):
        date = page_list[i][:10]
        if pat_date.search(date):
            date_op = page_list[i]
            time_op = page_list[i + 1]
            date_proc = page_list[i + 2]
            auth_code = page_list[i + 3]
            category = page_list[i + 4]
            text = page_list[i + 5]
            amount = page_list[i + 6]  # с плюсом для пополнений, остальные без знака
            i += 7
            # replace spaces with '' and , with .
            res_list.append([date_op, time_op, date_proc, auth_code, category, text, unidecode(amount)])
        else:
            i += 1

print(res_list[:-2])
