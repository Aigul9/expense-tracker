from decouple import config
from sqlalchemy import create_engine, Float, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime


db_name = config('POSTGRES_DB')
db_user = config('POSTGRES_USER')
db_pass = config('POSTGRES_PASSWORD')
db_host = config('POSTGRES_HOST')
db_port = config('POSTGRES_PORT')

db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)
Session = sessionmaker(bind=db)
Base = declarative_base()


class SberTransaction(Base):
    __tablename__ = 'sber'
    trans_id = Column(Integer, primary_key=True)
    bank = Column(String)
    trans_datetime = Column(DateTime)
    transfer_datetime = Column(DateTime)
    auth_code = Column(String)
    category = Column(String)
    debit = Column(Float)
    credit = Column(Float)
    text = Column(String)

    def __init__(self, bank, trans_datetime, transfer_datetime, auth_code, category, debit, credit, text):
        self.bank = bank
        self.trans_datetime = trans_datetime
        self.transfer_datetime = transfer_datetime
        self.auth_code = auth_code
        self.category = category
        self.debit = debit
        self.credit = credit
        self.text = text


class SovcomTransaction(Base):
    __tablename__ = 'sovcom'
    trans_id = Column(Integer, primary_key=True)
    bank = Column(String)
    trans_datetime = Column(DateTime)
    account = Column(String)
    income_balance = Column(Float)
    debit = Column(Float)
    credit = Column(Float)
    text = Column(String)

    def __init__(self, bank, trans_datetime, account, income_balance, debit, credit, text):
        self.bank = bank
        self.trans_datetime = trans_datetime
        self.account = account
        self.income_balance = income_balance
        self.debit = debit
        self.credit = credit
        self.text = text


class TinkoffTransactionMobile(Base):
    __tablename__ = 'tinkoff_mobile'
    trans_id = Column(Integer, primary_key=True)
    bank = Column(String)
    trans_datetime = Column(DateTime)
    transfer_datetime = Column(DateTime)
    debit = Column(Float)
    credit = Column(Float)
    card_sum = Column(Float)
    text = Column(String)

    def __init__(self, bank, trans_datetime, transfer_datetime, debit, credit, card_sum, text):
        self.bank = bank
        self.trans_datetime = trans_datetime
        self.transfer_datetime = transfer_datetime
        self.debit = debit
        self.credit = credit
        self.card_sum = card_sum
        self.text = text


class TinkoffTransaction(Base):
    __tablename__ = 'tinkoff'
    trans_id = Column(Integer, primary_key=True)
    bank = Column(String)
    trans_datetime = Column(DateTime)
    transfer_datetime = Column(DateTime)
    pan = Column(String)
    status = Column(String)
    debit = Column(Float)
    credit = Column(Float)
    trans_currency = Column(String)
    pay_sum = Column(Float)
    pay_currency = Column(String)
    cashback = Column(String)
    category = Column(String)
    mcc = Column(String)
    text = Column(String)
    bonus = Column(Float)
    rounding = Column(Float)
    sum_with_rounding = Column(Float)

    def __init__(self, bank, trans_datetime, transfer_datetime, pan, status, debit, credit,
                 trans_currency, pay_sum, pay_currency, cashback, category, mcc, text,
                 bonus, rounding, sum_with_rounding):
        self.bank = bank
        self.trans_datetime = trans_datetime
        self.transfer_datetime = transfer_datetime
        self.pan = pan
        self.status = status
        self.debit = debit
        self.credit = credit
        self.trans_currency = trans_currency
        self.pay_sum = pay_sum
        self.pay_currency = pay_currency
        self.cashback = cashback
        self.category = category
        self.mcc = mcc
        self.text = text
        self.bonus = bonus
        self.rounding = rounding
        self.sum_with_rounding = sum_with_rounding


class VTBTransaction(Base):
    __tablename__ = 'vtb'
    trans_id = Column(Integer, primary_key=True)
    bank = Column(String)
    trans_datetime = Column(DateTime)
    transfer_datetime = Column(DateTime)
    card_sum = Column(Float)
    debit = Column(Float)
    credit = Column(Float)
    text = Column(String)

    def __init__(self, bank, trans_datetime, transfer_datetime, card_sum, debit, credit, text):
        self.bank = bank
        self.trans_datetime = trans_datetime
        self.transfer_datetime = transfer_datetime
        self.card_sum = card_sum
        self.debit = debit
        self.credit = credit
        self.text = text


Base.metadata.create_all(db)
session = Session()
session.commit()
