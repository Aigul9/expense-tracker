--v_sber
SELECT sber.bank,
    sber.trans_datetime,
    sber.debit,
    sber.credit,
    sber.category,
        CASE
            WHEN (sber.category::text = ANY (ARRAY['Перевод с карты'::character varying::text, 'Перевод на карту'::character varying::text, 'Прочие операции'::character varying::text])) AND (sber.text::text ~~ '%2222%'::text OR sber.text::text ~~ '%1111%'::text OR sber.text::text ~~ '%3333%'::text) AND NOT sber.text::text ~~ '%перация%по%карте%2222%'::text AND NOT sber.text::text ~~ '%перация%по%карте%1111%'::text AND NOT sber.text::text ~~ '%перация%по%счету%3333%'::text THEN 'Перевод себе'::text
            WHEN sber.text::text ~~ '%1111%перация%по%карте%2222%'::text THEN 'Перевод себе'::text
            WHEN sber.text::text ~~ '%3333%перация%по%карте%2222%'::text THEN 'Перевод себе'::text
            WHEN sber.text::text ~~ '%2222%перация%по%карте%1111%'::text THEN 'Перевод себе'::text
            WHEN sber.text::text ~~ '%3333%перация%по%карте%1111%'::text THEN 'Перевод себе'::text
            WHEN sber.text::text ~~ '%2222%перация%по%карте%3333%'::text THEN 'Перевод себе'::text
            WHEN sber.text::text ~~ '%1111%перация%по%карте%3333%'::text THEN 'Перевод себе'::text
            WHEN lower(sber.text::text) ~~ '%vklad%'::text THEN 'Перевод себе'::text
            WHEN sber.category::text = 'Прочие операции'::text AND (lower(sber.text::text) ~~ '%тиньк%'::text OR lower(sber.text::text) ~~ '%tink%'::text) AND (EXISTS ( SELECT 1
               FROM tinkoff
              WHERE date(sber.trans_datetime) = date(tinkoff.trans_datetime) AND (sber.credit > 0::double precision AND sber.credit = tinkoff.debit AND (tinkoff.category::text = ANY (ARRAY['Переводы'::character varying::text, 'Пополнения'::character varying::text])) OR sber.debit > 0::double precision AND sber.debit = tinkoff.credit AND tinkoff.category::text = 'Переводы'::text))) THEN 'Перевод себе'::text
            WHEN sber.category::text = 'Прочие операции'::text AND (lower(sber.text::text) ~~ '%совком%'::text OR lower(sber.text::text) ~~ '%sovcom%'::text) AND (EXISTS ( SELECT 1
               FROM sovcom
              WHERE date(sber.trans_datetime) = date(sovcom.trans_datetime) AND (sber.credit > 0::double precision AND sber.credit = sovcom.debit OR sber.debit > 0::double precision AND sber.debit = sovcom.credit) AND sovcom.category::text = 'Переводы'::text)) THEN 'Перевод себе'::text
            WHEN sber.category::text = 'Прочие операции'::text AND (lower(sber.text::text) ~~ '%втб%'::text OR lower(sber.text::text) ~~ '%vtb%'::text OR lower(sber.text::text) ~~ '%vb24%'::text) AND (EXISTS ( SELECT 1
               FROM vtb
              WHERE date(sber.trans_datetime) = date(vtb.trans_datetime) AND (sber.credit > 0::double precision AND sber.credit = vtb.debit OR sber.debit > 0::double precision AND sber.debit = vtb.credit))) THEN 'Перевод себе'::text
            WHEN sber.debit > 0::double precision THEN 'Поступление'::text
            WHEN sber.credit > 0::double precision THEN 'Расход'::text
            ELSE NULL::text
        END AS trans_type,
    sber.text,
    sber.trans_id
FROM sber;


--v_sovcom
SELECT sovcom.bank,
    sovcom.trans_datetime,
    sovcom.debit,
    sovcom.credit,
    sovcom.category,
        CASE
            WHEN sovcom.category::text = 'Переводы'::text AND sovcom.text::text ~~ 'Зачисление перевода денежных средств%9999999999%'::text THEN 'Перевод себе'::text
            WHEN sovcom.category::text = 'Переводы'::text AND sovcom.text::text ~~ 'Перевод согласно распоряжения%'::text AND ((EXISTS ( SELECT 1
               FROM sber
              WHERE date(sovcom.trans_datetime) = date(sber.trans_datetime) AND sovcom.credit = sber.debit AND (sber.category::text = ANY (ARRAY['Переводы на карту'::character varying::text, 'Прочие операции'::character varying::text])))) OR (EXISTS ( SELECT 1
               FROM tinkoff
              WHERE date(sovcom.trans_datetime) = date(tinkoff.trans_datetime) AND sovcom.credit = tinkoff.debit AND (tinkoff.category::text = ANY (ARRAY['Переводы'::character varying::text, 'Пополнения'::character varying::text]))))) THEN 'Перевод себе'::text
            WHEN sovcom.debit > 0::double precision THEN 'Поступление'::text
            WHEN sovcom.credit > 0::double precision THEN 'Расход'::text
            ELSE NULL::text
        END AS trans_type,
    sovcom.text,
    sovcom.trans_id
FROM sovcom;


--v_tinkoff
SELECT tinkoff.bank,
    tinkoff.trans_datetime,
    tinkoff.debit,
    tinkoff.credit,
    tinkoff.category,
        CASE
            WHEN tinkoff.status::text <> 'OK'::text THEN 'Failed'::text
            WHEN (tinkoff.category::text = ANY (ARRAY['Переводы'::character varying::text, 'Пополнения'::character varying::text])) AND (tinkoff.text::text = ANY (ARRAY['Перевод между счетами'::character varying::text, 'Имя Ф.'::character varying::text])) THEN 'Перевод себе'::text
            WHEN tinkoff.debit > 0::double precision THEN 'Поступление'::text
            WHEN tinkoff.credit > 0::double precision THEN 'Расход'::text
            ELSE NULL::text
        END AS trans_type,
    tinkoff.text,
    tinkoff.trans_id
FROM tinkoff;


--v_vtb
SELECT vtb.bank,
    vtb.trans_datetime,
    vtb.debit,
    vtb.credit,
    vtb.category,
        CASE
            WHEN vtb.debit > 0::double precision THEN 'Поступление'::text
            WHEN vtb.credit > 0::double precision THEN 'Расход'::text
            ELSE NULL::text
        END AS trans_type,
    vtb.text,
    vtb.trans_id
FROM vtb;


--v_transactions
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