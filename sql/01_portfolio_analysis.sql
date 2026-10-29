-- Run after python scripts/analyse.py has created data/credit_risk.sqlite.
-- All rates are observed next-month payment-default incidence, not forecast PDs.
-- Credit limits are NT dollars, not exposure at default.

-- 01. Portfolio snapshot
SELECT COUNT(*) AS clients,
       SUM("default.payment.next.month") AS defaults,
       ROUND(100.0 * AVG("default.payment.next.month"), 2) AS default_rate_pct,
       ROUND(AVG(LIMIT_BAL), 0) AS mean_credit_limit_ntd
FROM credit_clients;

-- 02. Default incidence by September repayment code (preserves raw -2 and 0)
SELECT PAY_0 AS september_repayment_code,
       COUNT(*) AS clients,
       SUM("default.payment.next.month") AS defaults,
       ROUND(100.0 * AVG("default.payment.next.month"), 2) AS default_rate_pct
FROM credit_clients
GROUP BY PAY_0
ORDER BY PAY_0;

-- 03. Default incidence by credit-limit band
SELECT limit_band AS credit_limit_band,
       COUNT(*) AS clients,
       SUM("default.payment.next.month") AS defaults,
       ROUND(100.0 * AVG("default.payment.next.month"), 2) AS default_rate_pct
FROM credit_clients
GROUP BY limit_band
ORDER BY MIN(LIMIT_BAL);

-- 04. Risk incidence by age band -- descriptive only; fairness review needed
SELECT age_band,
       COUNT(*) AS clients,
       SUM("default.payment.next.month") AS defaults,
       ROUND(100.0 * AVG("default.payment.next.month"), 2) AS default_rate_pct
FROM credit_clients
GROUP BY age_band
ORDER BY MIN(AGE);

-- 05. Data quality: unknown undocumented categorical codes
SELECT
       SUM(CASE WHEN EDUCATION IN (0,5,6) THEN 1 ELSE 0 END) AS undocumented_education,
       SUM(CASE WHEN MARRIAGE = 0 THEN 1 ELSE 0 END) AS undocumented_marital,
       SUM(CASE WHEN PAY_0 IN (-2,0) THEN 1 ELSE 0 END) AS undocumented_repayment_sep,
       SUM(CASE WHEN BILL_AMT1 < 0 THEN 1 ELSE 0 END) AS negative_september_bills
FROM credit_clients;
