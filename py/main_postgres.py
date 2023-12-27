import logging

from sqlalchemy.dialects.postgresql import insert

from connect import session, SberTransaction, SovcomTransaction, TinkoffTransaction, VTBTransaction
from py.banks.sber import get_sber_transactions
from py.banks.sovcom import get_sovcom_transactions
from py.banks.tinkoff import get_tinkoff_transactions_txt
from py.banks.vtb import get_vtb_transactions

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)s:%(funcName)s()',
)
logger = logging.getLogger(__name__)


# def load_transaction(Model, trans):
#     new_transaction = Model(
#         *trans.values()
#     )
#     session.merge(new_transaction)


sber_transactions = get_sber_transactions()
sovcom_transactions = get_sovcom_transactions()
tinkoff_transactions = get_tinkoff_transactions_txt()
vtb_transactions = get_vtb_transactions()

for transaction in sber_transactions:
    logger.debug(transaction)
    session.execute(insert(SberTransaction).values(transaction).on_conflict_do_nothing())
    session.commit()

for transaction in sovcom_transactions:
    logger.debug(transaction)
    session.execute(insert(SovcomTransaction).values(transaction).on_conflict_do_nothing())
    session.commit()

for transaction in tinkoff_transactions:
    logger.debug(transaction)
    session.execute(insert(TinkoffTransaction).values(transaction).on_conflict_do_nothing())
    session.commit()

for transaction in vtb_transactions:
    logger.debug(transaction)
    session.execute(insert(VTBTransaction).values(transaction).on_conflict_do_nothing())
    session.commit()
    session.commit()

session.close()
