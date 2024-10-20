--update categories
select * from sovcom
where load_date = '2024-10-20';

--number of new transactions
select bank, count(1)
from v_transactions
group by bank
where load_date = '2024-10-20';

--check duplicated rows
select trans_datetime, auth_code, category, debit, credit, count(1)
from sber
group by trans_datetime, auth_code, category, debit, credit
having count(1) > 1
order by trans_datetime desc;

select trans_datetime, category, debit, credit, count(1)
from tinkoff
group by trans_datetime, category, debit, credit
having count(1) > 1
order by trans_datetime desc;

select trans_datetime, account, category, debit, credit, income_balance, count(1)
from sovcom
group by trans_datetime, account, category, debit, credit, income_balance
having count(1) > 1
order by trans_datetime desc;