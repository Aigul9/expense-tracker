import PyPDF2
import re

path = 'input/tinkoff/5-3DJEIVPWC_20230115.pdf'
with open(path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    num_pages = len(reader.pages)
    pat_date = re.compile(r'(\d{2}.\d{2}.\d{4})')
    DATETIME = slice(16)
    DATE = slice(17, 27)
    last_idx = 27
    print(len(reader.pages))
    for i in range(num_pages):
        page = reader.pages[i]
        for row in page.extract_text().split('\n'):
            date = row[:10]
            if pat_date.search(date):
                # print(row)
                print(row[DATETIME], row[DATE])
                op_sum, card_sum, text = [line.strip() for line in row[last_idx:].split('₽')]
                print(op_sum, card_sum, text)

# named tuple
# fields save into page class

