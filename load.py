from connect import session\
    # , SberTransaction, SovcomTransaction, TinkoffTransaction, VTBTransaction


def load_transaction(Model, transaction):
    new_transaction = Model(
        *transaction.values()
    )
    session.add(new_transaction)

# def load_sber_transaction(transaction):
#     new_transaction = SberTransaction(
#         *transaction.values()
#     )
#     session.add(new_transaction)


# def load_sovcom_transaction(transaction):
#     new_transaction = SovcomTransaction(
#         *transaction.values()
#     )
#     session.add(new_transaction)
#
#
# def load_tinkoff_transaction(transaction):
#     new_transaction = TinkoffTransaction(
#         *transaction.values()
#     )
#     session.add(new_transaction)
#
#
# def load_vtb_transaction(transaction):
#     new_transaction = VTBTransaction(
#         *transaction.values()
#     )
#     session.add(new_transaction)
