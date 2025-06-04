from datetime import date

from decouple import config
from sqlalchemy import create_engine, Date, Float, Integer, MetaData, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema
from sqlalchemy import Column, String, DateTime


db_name = config('POSTGRES_DB')
db_user = config('POSTGRES_USER')
db_pass = config('POSTGRES_PASSWORD')
db_host = config('POSTGRES_HOST')
db_port = config('POSTGRES_PORT')
db_schema = config('POSTGRES_SCHEMA')

db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
engine = create_engine(db_string)
Session = sessionmaker(bind=engine)

if not engine.dialect.has_schema(engine, db_schema):
    engine.execute(CreateSchema(db_schema))

metadata_obj = MetaData(schema=db_schema)
Base = declarative_base(metadata=metadata_obj)


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
    load_date = Column(Date, default=date.today())
    __table_args__ = (
        UniqueConstraint(
            'bank',
            'trans_datetime',
            'auth_code',
            'category',
            'debit',
            'credit'
        ),
    )

    def __init__(self, bank, trans_datetime, transfer_datetime, auth_code, category, debit, credit, text):
        self.bank = bank
        self.trans_datetime = trans_datetime
        self.transfer_datetime = transfer_datetime
        self.auth_code = auth_code
        self.category = category
        self.debit = debit
        self.credit = credit
        self.text = text


class SberAccountTransaction(Base):
    __tablename__ = 'sber_account'
    trans_id = Column(Integer, primary_key=True)
    bank = Column(String)
    trans_datetime = Column(DateTime)
    category = Column(String)
    account = Column(String)
    income_balance = Column(Float)
    debit = Column(Float)
    credit = Column(Float)
    text = Column(String)
    load_date = Column(Date, default=date.today())
    __table_args__ = (
        UniqueConstraint(
            'bank',
            'trans_datetime',
            'category',
            'account',
            'income_balance',
            'debit',
            'credit'
        ),
    )

    def __init__(self, bank, trans_datetime, category, account, income_balance, debit, credit, text):
        self.bank = bank
        self.trans_datetime = trans_datetime
        self.category = category
        self.account = account
        self.income_balance = income_balance
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
    load_date = Column(Date, default=date.today())
    __table_args__ = (
        UniqueConstraint(
            'bank',
            'trans_datetime',
            'account',
            'income_balance',
            'debit',
            'credit'
        ),
    )

    def __init__(self, bank, trans_datetime, account, income_balance, debit, credit, text):
        self.bank = bank
        self.trans_datetime = trans_datetime
        self.account = account
        self.income_balance = income_balance
        self.debit = debit
        self.credit = credit
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
    load_date = Column(Date, default=date.today())
    __table_args__ = (
        UniqueConstraint(
            'bank',
            'trans_datetime',
            'pan',
            'status',
            'debit',
            'credit',
            'trans_currency',
            'pay_sum',
            'pay_currency',
            'category',
            'mcc'
        ),
    )

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
    __table_args__ = (
        UniqueConstraint(
            'bank',
            'trans_datetime',
            'card_sum',
            'debit',
            'credit'
        ),
    )

    def __init__(self, bank, trans_datetime, transfer_datetime, card_sum, debit, credit, text):
        self.bank = bank
        self.trans_datetime = trans_datetime
        self.transfer_datetime = transfer_datetime
        self.card_sum = card_sum
        self.debit = debit
        self.credit = credit
        self.text = text


Base.metadata.create_all(engine)
session = Session()
session.commit()
