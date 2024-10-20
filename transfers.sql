--v_sber
CREATE OR REPLACE VIEW v_sber AS
SELECT sber.bank,
    sber.trans_id,
    sber.trans_datetime,
    sber.debit,
    sber.credit,
    sber.category,
        CASE
            WHEN (sber.category = ANY (ARRAY['Перевод с карты', 'Перевод на карту', 'Прочие операции'])) AND (sber.text ~~ '%2222%' OR sber.text ~~ '%1111%' OR sber.text ~~ '%3333%') AND NOT sber.text ~~ '%перация%по%карте%2222%' AND NOT sber.text ~~ '%перация%по%карте%1111%' AND NOT sber.text ~~ '%перация%по%счету%3333%' THEN 'Перевод себе'
            WHEN sber.text ~~ '%1111%перация%по%карте%2222%' THEN 'Перевод себе'
            WHEN sber.text ~~ '%3333%перация%по%карте%2222%' THEN 'Перевод себе'
            WHEN sber.text ~~ '%2222%перация%по%карте%1111%' THEN 'Перевод себе'
            WHEN sber.text ~~ '%3333%перация%по%карте%1111%' THEN 'Перевод себе'
            WHEN sber.text ~~ '%2222%перация%по%счету%3333%' THEN 'Перевод себе'
            WHEN sber.text ~~ '%1111%перация%по%счету%3333%' THEN 'Перевод себе'
            WHEN lower(sber.text::text) ~~ '%vklad%' AND credit in (99999) THEN 'Расход'
            WHEN lower(sber.text) ~~ '%vklad%' THEN 'Перевод себе'
            WHEN sber.category = 'Прочие операции' AND (lower(sber.text) ~~ '%тиньк%' OR lower(sber.text) ~~ '%tink%' OR lower(sber.text) ~~ '%т-банк%') AND (EXISTS ( SELECT 1
               FROM tinkoff
              WHERE date(sber.trans_datetime) = date(tinkoff.trans_datetime) AND (sber.credit > 0 AND sber.credit = tinkoff.debit AND (tinkoff.category = ANY (ARRAY['Переводы', 'Пополнения'])) OR sber.debit > 0 AND sber.debit = tinkoff.credit AND tinkoff.category = 'Переводы'))) THEN 'Перевод себе'
            WHEN sber.category = 'Прочие операции' AND (lower(sber.text) ~~ '%совком%' OR lower(sber.text) ~~ '%coвком%' OR lower(sber.text) ~~ '%sovcom%') AND (EXISTS ( SELECT 1
               FROM sovcom
              WHERE date(sber.trans_datetime) = date(sovcom.trans_datetime) AND (sber.credit > 0 AND sber.credit = sovcom.debit OR sber.debit > 0 AND sber.debit = sovcom.credit) AND sovcom.category = 'Переводы')) THEN 'Перевод себе'
            WHEN sber.category = 'Прочие операции' AND (lower(sber.text) ~~ '%втб%' OR lower(sber.text) ~~ '%vtb%' OR lower(sber.text) ~~ '%vb24%') AND (EXISTS ( SELECT 1
               FROM vtb
              WHERE date(sber.trans_datetime) = date(vtb.trans_datetime) AND (sber.credit > 0 AND sber.credit = vtb.debit OR sber.debit > 0 AND sber.debit = vtb.credit))) THEN 'Перевод себе'
            WHEN sber.debit > 0 THEN 'Поступление'
            WHEN sber.credit > 0 THEN 'Расход'
            ELSE NULL
        END AS trans_type,
    sber.text,
    sber.load_date
FROM sber;


--v_sovcom
CREATE OR REPLACE VIEW v_sovcom AS
SELECT sovcom.bank,
    sovcom.trans_id,
    sovcom.trans_datetime,
    sovcom.debit,
    sovcom.credit,
    sovcom.category,
        CASE
            WHEN sovcom.category = 'Переводы' AND sovcom.text ~~ 'Зачисление перевода денежных средств%9999999999%' THEN 'Перевод себе'
            WHEN sovcom.category = 'Переводы' AND sovcom.text ~~ 'Перевод согласно распоряжения%' AND ((EXISTS ( SELECT 1
               FROM sber
              WHERE date(sovcom.trans_datetime) = date(sber.trans_datetime) AND sovcom.credit = sber.debit AND (sber.category = ANY (ARRAY['Переводы на карту', 'Прочие операции'])))) OR (EXISTS ( SELECT 1
               FROM tinkoff
              WHERE date(sovcom.trans_datetime) = date(tinkoff.trans_datetime) AND sovcom.credit = tinkoff.debit AND (tinkoff.category = ANY (ARRAY['Переводы', 'Пополнения']))))) THEN 'Перевод себе'
            WHEN sovcom.debit > 0 THEN 'Поступление'
            WHEN sovcom.credit > 0 THEN 'Расход'
            ELSE NULL
        END AS trans_type,
    sovcom.text,
    sovcom.load_date
FROM sovcom;


--v_tinkoff
CREATE OR REPLACE VIEW v_tinkoff AS
SELECT tinkoff.bank,
    tinkoff.trans_id,
    tinkoff.trans_datetime,
    tinkoff.debit,
    tinkoff.credit,
    tinkoff.category,
        CASE
            WHEN tinkoff.status <> 'OK' THEN 'Failed'
            WHEN (tinkoff.category = ANY (ARRAY['Переводы', 'Пополнения'])) AND (tinkoff.text = ANY (ARRAY['Перевод между счетами', 'Имя Ф.'])) THEN 'Перевод себе'
            WHEN tinkoff.debit > 0 THEN 'Поступление'
            WHEN tinkoff.credit > 0 THEN 'Расход'
            ELSE NULL
        END AS trans_type,
    tinkoff.text,
    tinkoff.load_date
FROM tinkoff;


--v_vtb
CREATE OR REPLACE VIEW v_vtb AS
SELECT vtb.bank,
    vtb.trans_id,
    vtb.trans_datetime,
    vtb.debit,
    vtb.credit,
    vtb.category,
        CASE
            WHEN vtb.debit > 0 THEN 'Поступление'
            WHEN vtb.credit > 0 THEN 'Расход'
            ELSE NULL
        END AS trans_type,
    vtb.text,
    null::date as load_date
FROM vtb;


--v_transactions
CREATE OR REPLACE VIEW v_transactions AS
SELECT v_sber.bank,
    v_sber.trans_datetime,
    v_sber.debit,
    v_sber.credit,
    v_sber.category,
    v_sber.trans_type,
    v_sber.text,
    v_sber.trans_id
FROM v_sber
UNION ALL
SELECT v_tinkoff.bank,
    v_tinkoff.trans_datetime,
    v_tinkoff.debit,
    v_tinkoff.credit,
    v_tinkoff.category,
    v_tinkoff.trans_type,
    v_tinkoff.text,
    v_tinkoff.trans_id
FROM v_tinkoff
UNION ALL
SELECT v_sovcom.bank,
    v_sovcom.trans_datetime,
    v_sovcom.debit,
    v_sovcom.credit,
    v_sovcom.category,
    v_sovcom.trans_type,
    v_sovcom.text,
    v_sovcom.trans_id
FROM v_sovcom
UNION ALL
SELECT v_vtb.bank,
    v_vtb.trans_datetime,
    v_vtb.debit,
    v_vtb.credit,
    v_vtb.category,
    v_vtb.trans_type,
    v_vtb.text,
    v_vtb.trans_id
FROM v_vtb;