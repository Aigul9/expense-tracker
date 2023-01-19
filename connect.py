from decouple import config
from sqlalchemy import create_engine, Float, Integer, Identity
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


class TinkoffTransaction(Base):
    __tablename__ = 'tinkoff'
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
