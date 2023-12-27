import logging
from decouple import config
from pymongo import MongoClient
from py.banks.sber import get_sber_transactions
from py.banks.sovcom import get_sovcom_transactions
from py.banks.tinkoff import get_tinkoff_transactions_txt

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)s:%(funcName)s()',
)
logger = logging.getLogger(__name__)

client = MongoClient(config('URI'))
db = client[config('DB_NAME')]
coll = db[config('COLL_NAME')]
logger.info('Connected')


def upsert(transactions):
    for trans in transactions:
        logger.debug(trans)
        coll.update_one(trans, {'$setOnInsert': trans}, upsert=True)


sber_transactions = get_sber_transactions()
upsert(sber_transactions)
# coll.delete_many({'bank': 'Sovcom'})
sovcom_transactions = get_sovcom_transactions()
upsert(sovcom_transactions)
tinkoff_transactions = get_tinkoff_transactions_txt()
upsert(tinkoff_transactions)
# vtb_transactions = get_vtb_transactions()
# upsert(vtb_transactions)

client.close()
