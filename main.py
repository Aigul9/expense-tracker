import logging
from decouple import config
from pymongo import MongoClient

from banks.sovcom import get_sovcom_transactions
from banks.tinkoff import get_tinkoff_transactions

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)s:%(funcName)s()',
)
logger = logging.getLogger(__name__)

client = MongoClient(config('ATLAS_URI'))
db = client[config('DB_NAME')]
coll = db[config('COLL_NAME')]
logger.info('Connected')


def upsert(transactions):
    for trans in transactions:
        logger.debug(trans)
        coll.update_one(trans, {'$setOnInsert': trans}, upsert=True)


sber_transactions = get_sber_transactions()
upsert(sber_transactions)
sovcom_transactions = get_sovcom_transactions()
upsert(sovcom_transactions)
tinkoff_transactions = get_tinkoff_transactions()
upsert(tinkoff_transactions)

client.close()
