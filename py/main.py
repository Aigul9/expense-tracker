import logging

import sber
import sber_account
import sovcom
import tinkoff
import vtb
from connect import session, SberTransaction, SberAccountTransaction, SovcomTransaction, TinkoffTransaction, VTBTransaction

from sqlalchemy.dialects.postgresql import insert

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)s:%(funcName)s()',
)

logger = logging.getLogger(__name__)


transactions = {
    'sber': (sber.get_transactions(), SberTransaction),
    'sber_account': (sber_account.get_transactions(), SberAccountTransaction),
    'sovcom': (sovcom.get_transactions(), SovcomTransaction),
    'tinkoff': (tinkoff.get_transactions(), TinkoffTransaction),
    'vtb': (vtb.get_transactions(), VTBTransaction)
}

for _, (source_transactions, TransactionClass) in transactions.items():
    for transaction in source_transactions:
        logger.debug(transaction)
        session.execute(insert(TransactionClass).values(transaction).on_conflict_do_nothing())
        session.commit()

session.close()
