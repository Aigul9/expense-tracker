import logging

from connect import session, SberTransaction, SovcomTransaction, TinkoffTransaction, VTBTransaction
from sber import get_sber_transactions
from sovcom import get_sovcom_transactions
from tinkoff import get_tinkoff_transactions_txt
from vtb import get_vtb_transactions

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)s:%(funcName)s()',
)
logger = logging.getLogger(__name__)


def load_transaction(Model, trans):
    new_transaction = Model(
        *trans.values()
    )
    session.merge(new_transaction)


sber_transactions = get_sber_transactions()
sovcom_transactions = get_sovcom_transactions()
tinkoff_transactions = get_tinkoff_transactions_txt()
vtb_transactions = get_vtb_transactions()

# for transaction in sber_transactions:
#     logger.debug(transaction)
#     load_transaction(SberTransaction, transaction)
#     session.commit()

# for transaction in sovcom_transactions:
#     logger.debug(transaction)
#     load_transaction(SovcomTransaction, transaction)
#     session.commit()

for transaction in tinkoff_transactions:
    logger.debug(transaction)
    load_transaction(TinkoffTransaction, transaction)
    session.commit()

# for transaction in vtb_transactions:
#     logger.debug(transaction)
#     load_transaction(VTBTransaction, transaction)
#     session.commit()

session.close()
