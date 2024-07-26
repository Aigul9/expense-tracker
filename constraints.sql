ALTER TABLE sber
ADD CONSTRAINT unique_sber
UNIQUE (bank, trans_datetime, auth_code, debit, credit);

ALTER TABLE sovcom
ADD CONSTRAINT unique_sovcom
UNIQUE (bank, trans_datetime, account, income_balance, debit, credit, text);

ALTER TABLE tinkoff
ADD CONSTRAINT unique_tinkoff
UNIQUE (bank, trans_datetime, debit, credit, category, mcc);


select * from sber
where load_date is not null
order by load_date desc;

