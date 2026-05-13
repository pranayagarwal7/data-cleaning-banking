# 🏦 Retail Banking Dataset — Complete Practice Guide

---

## 1. SCHEMA OVERVIEW

### `branches` (50 rows)
| Column | Type | Notes |
|---|---|---|
| branch_id | VARCHAR | PK — format `BR001` |
| branch_name | VARCHAR | City + descriptor + "Branch" |
| city | VARCHAR | ⚠️ Inconsistent casing |
| state | VARCHAR | ⚠️ Invalid abbreviations injected |
| region | VARCHAR | Northeast / South / West / Midwest / Mountain |
| zip_code | VARCHAR | |
| phone | VARCHAR | ⚠️ Mixed formats |
| manager_name | VARCHAR | ⚠️ Mixed casing/spacing |
| open_since | VARCHAR | ⚠️ Mixed date formats |
| num_employees | INT/NULL | ⚠️ 5% nulls |
| is_active | MIXED | ⚠️ Yes/No/TRUE/FALSE/1/0/Active |

### `customers` (5,000 base + ~150 duplicates = 5,150 rows)
| Column | Type | Notes |
|---|---|---|
| customer_id | VARCHAR | PK — format `CUST000001` |
| first_name | VARCHAR | ⚠️ Mixed casing + trailing spaces |
| last_name | VARCHAR | ⚠️ Mixed casing + reversed names |
| date_of_birth | VARCHAR | ⚠️ Mixed formats + impossible future dates |
| gender | VARCHAR | ⚠️ M/Male/MALE/1/F/Female/0 |
| email | VARCHAR | ⚠️ Blank, N/A, missing @, ALLCAPS |
| phone | VARCHAR | ⚠️ 7+ format variants |
| address | VARCHAR | 5% null |
| city | VARCHAR | 4% null |
| state | VARCHAR | ⚠️ Invalid codes (ZZ, XX, 00) |
| zip_code | VARCHAR | ⚠️ 00000 injected |
| annual_income | MIXED | ⚠️ $, USD, comma-decimal, None |
| occupation | VARCHAR | 5% null |
| credit_score | MIXED | ⚠️ 9999/-1, "612 pts", None |
| customer_since | VARCHAR | ⚠️ Mixed date formats |
| branch_id | VARCHAR | FK → branches ⚠️ 4% null |
| is_high_risk | MIXED | ⚠️ Yes/TRUE/1/True/None |
| kyc_status | VARCHAR | ⚠️ Verified/VERIFIED/verified/pending |
| nationality | VARCHAR | 6% null |
| referral_source | VARCHAR | ⚠️ Online/online/ONLINE/N/A |

### `accounts` (8,000 rows)
| Column | Type | Notes |
|---|---|---|
| account_id | VARCHAR | PK — format `ACC1234567` |
| customer_id | VARCHAR | FK → customers ⚠️ 3% null |
| branch_id | VARCHAR | FK → branches ⚠️ 4% null |
| account_type | VARCHAR | ⚠️ 12+ variant spellings |
| account_status | VARCHAR | ⚠️ Active/ACTIVE/open/Open/N/A |
| open_date | VARCHAR | ⚠️ Mixed date formats |
| close_date | VARCHAR | 15% populated, rest null |
| balance | MIXED | ⚠️ Currency symbols, cents errors, negative savings |
| currency | VARCHAR | ⚠️ USD/usd/$/EUR/GBP mixed |
| interest_rate | FLOAT/NULL | 6% null |
| overdraft_limit | MIXED | 10% null |
| monthly_fee | FLOAT | |
| account_number | VARCHAR | 12-digit string |

### `transactions` (100,000 base + ~2,000 duplicates = 102,000 rows)
| Column | Type | Notes |
|---|---|---|
| transaction_id | VARCHAR | PK — format `TXN00000001` |
| account_id | VARCHAR | FK → accounts ⚠️ 2% null |
| transaction_type | VARCHAR | ⚠️ Typos: Withdrawl, Deposite, Tranfer |
| amount | MIXED | ⚠️ Currency symbols, outliers (up to $500K), negative deposits |
| currency | VARCHAR | ⚠️ Mixed casing + EUR/GBP |
| transaction_date | VARCHAR | ⚠️ 4 different date formats |
| transaction_timestamp | DATETIME/NULL | 6% null |
| merchant_name | VARCHAR | 60% populated |
| merchant_category | VARCHAR | ⚠️ Mixed casing |
| description | VARCHAR | ⚠️ Nulls and blank strings |
| balance_after | MIXED | ⚠️ Can be negative |
| channel | VARCHAR | ⚠️ Online/online/ONLINE/N/A |
| status | VARCHAR | ⚠️ completed/COMPLETED/NULL string |
| ip_address | VARCHAR | 20% null |
| device_type | VARCHAR | ⚠️ Mobile/mobile/MOBILE |

### `loans` (2,000 rows)
| Column | Type | Notes |
|---|---|---|
| loan_id | VARCHAR | PK — format `LOAN000001` |
| customer_id | VARCHAR | FK → customers ⚠️ 3% null |
| branch_id | VARCHAR | FK → branches ⚠️ 5% null |
| loan_type | VARCHAR | ⚠️ Personal/personal mixed |
| loan_amount | MIXED | ⚠️ Currency symbols, cents errors |
| approved_amount | MIXED | Should be ≤ loan_amount |
| outstanding_balance | MIXED | |
| interest_rate | FLOAT/NULL | 5% null |
| term_months | INT/NULL | 4% null |
| start_date | VARCHAR | ⚠️ Mixed date formats |
| end_date | VARCHAR | ⚠️ Mixed date formats |
| monthly_payment | MIXED | |
| loan_status | VARCHAR | ⚠️ 15+ variant spellings |
| collateral_type | VARCHAR | ⚠️ None/none/N/A mixed |
| purpose | VARCHAR | 10% null |
| days_past_due | INT/NULL | Populated for Defaulted/Delinquent |
| num_missed_payments | INT/NULL | |
| credit_score_at_origination | INT/NULL | 8% null |
| approved_by | VARCHAR | 10% null |

---

## 2. SQL PRACTICE QUESTIONS

### 🟢 Easy (1–6)

**Q1 — Basic Join + Filter**
List all customers along with their branch city and region. Only include customers who are assigned to an active branch.
```sql
SELECT c.customer_id, c.first_name, c.last_name, b.city, b.region
FROM customers c
JOIN branches b ON c.branch_id = b.branch_id
WHERE b.is_active IN ('Yes','TRUE','1','Active');
```

**Q2 — Aggregation**
Find the total number of accounts and average balance per account type.
```sql
SELECT account_type,
       COUNT(*)        AS total_accounts,
       AVG(CAST(balance AS DECIMAL(15,2))) AS avg_balance
FROM accounts
GROUP BY account_type
ORDER BY total_accounts DESC;
```

**Q3 — NULL Detection**
Find all accounts that have no linked customer_id (orphaned accounts).
```sql
SELECT * FROM accounts WHERE customer_id IS NULL;
```

**Q4 — Date Filter**
Find all transactions in 2023 where transaction_type is 'Deposit' and amount > 10000.
```sql
SELECT * FROM transactions
WHERE transaction_date LIKE '2023%'
  AND transaction_type = 'Deposit'
  AND CAST(amount AS DECIMAL) > 10000;
```

**Q5 — Multi-table Join**
Show each loan with the customer's full name, their credit score, and the branch city.
```sql
SELECT l.loan_id, c.first_name, c.last_name, c.credit_score,
       b.city, l.loan_amount, l.loan_status
FROM loans l
LEFT JOIN customers c ON l.customer_id = c.customer_id
LEFT JOIN branches b  ON l.branch_id   = b.branch_id;
```

**Q6 — Grouped Count**
How many customers were acquired per year (based on customer_since)?
```sql
SELECT YEAR(STR_TO_DATE(customer_since,'%Y-%m-%d')) AS year_acquired,
       COUNT(*) AS new_customers
FROM customers
WHERE customer_since REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
GROUP BY year_acquired
ORDER BY year_acquired;
```

---

### 🟡 Intermediate (7–14)

**Q7 — Duplicate Detection**
Find duplicate customer records (same customer_id appearing more than once).
```sql
SELECT customer_id, COUNT(*) AS occurrences
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY occurrences DESC;
```

**Q8 — Window Function: Running Balance**
For each account, calculate the running total of transaction amounts ordered by transaction_date.
```sql
SELECT account_id, transaction_id, transaction_date, amount,
       SUM(CAST(amount AS DECIMAL(15,2)))
           OVER (PARTITION BY account_id ORDER BY transaction_date) AS running_total
FROM transactions
WHERE amount NOT LIKE '%$%' AND amount NOT LIKE '%USD%'
ORDER BY account_id, transaction_date;
```

**Q9 — Ranking**
Rank customers within each branch by total loan amount (highest to lowest).
```sql
SELECT c.customer_id, c.first_name, c.last_name, b.city,
       SUM(CAST(l.loan_amount AS DECIMAL(15,2))) AS total_loans,
       RANK() OVER (PARTITION BY c.branch_id ORDER BY SUM(CAST(l.loan_amount AS DECIMAL)) DESC) AS branch_rank
FROM customers c
JOIN loans l ON c.customer_id = l.customer_id
JOIN branches b ON c.branch_id = b.branch_id
WHERE l.loan_amount NOT LIKE '%$%'
GROUP BY c.customer_id, c.first_name, c.last_name, b.city, c.branch_id;
```

**Q10 — CTE: High-Value Customers**
Using a CTE, identify customers who have total transaction volume > $50,000 AND at least one active loan.
```sql
WITH tx_summary AS (
    SELECT account_id, SUM(CAST(amount AS DECIMAL(15,2))) AS total_volume
    FROM transactions
    WHERE status IN ('Completed','completed','COMPLETED')
      AND amount NOT LIKE '%$%'
    GROUP BY account_id
    HAVING total_volume > 50000
),
active_loans AS (
    SELECT DISTINCT customer_id
    FROM loans
    WHERE LOWER(loan_status) IN ('active','open','current','in progress')
)
SELECT c.customer_id, c.first_name, c.last_name, tv.total_volume
FROM customers c
JOIN accounts a   ON c.customer_id = a.customer_id
JOIN tx_summary tv ON a.account_id = tv.account_id
JOIN active_loans al ON c.customer_id = al.customer_id;
```

**Q11 — Time-Series: Monthly Transaction Trends**
Show the month-over-month change in total transaction count for the past 3 years.
```sql
WITH monthly AS (
    SELECT DATE_FORMAT(STR_TO_DATE(transaction_date,'%Y-%m-%d'),'%Y-%m') AS month,
           COUNT(*) AS tx_count
    FROM transactions
    WHERE transaction_date REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
    GROUP BY month
)
SELECT month, tx_count,
       tx_count - LAG(tx_count) OVER (ORDER BY month) AS mom_change
FROM monthly
ORDER BY month;
```

**Q12 — Loan Default Analysis**
What percentage of loans per loan_type are in Defaulted or Delinquent status?
```sql
SELECT loan_type,
       COUNT(*) AS total_loans,
       SUM(CASE WHEN LOWER(loan_status) IN ('defaulted','default','bad debt','charged off',
                                             'delinquent','late','past due') THEN 1 ELSE 0 END) AS bad_loans,
       ROUND(100.0 * SUM(CASE WHEN LOWER(loan_status) IN ('defaulted','default','bad debt',
                               'charged off','delinquent','late','past due') THEN 1 ELSE 0 END) / COUNT(*), 2) AS default_rate_pct
FROM loans
GROUP BY loan_type
ORDER BY default_rate_pct DESC;
```

**Q13 — Customer Segmentation**
Segment customers into Bronze / Silver / Gold / Platinum based on total account balances.
```sql
WITH clean_balances AS (
    SELECT customer_id,
           SUM(CAST(balance AS DECIMAL(15,2))) AS total_balance
    FROM accounts
    WHERE balance NOT LIKE '%$%' AND balance NOT LIKE '%USD%' AND balance IS NOT NULL
    GROUP BY customer_id
)
SELECT customer_id, total_balance,
    CASE
        WHEN total_balance >= 100000 THEN 'Platinum'
        WHEN total_balance >= 25000  THEN 'Gold'
        WHEN total_balance >= 5000   THEN 'Silver'
        ELSE 'Bronze'
    END AS segment
FROM clean_balances
ORDER BY total_balance DESC;
```

**Q14 — Fraud Detection: Rapid Transactions**
Find accounts with more than 10 transactions on the same day (possible fraud indicator).
```sql
SELECT account_id, transaction_date, COUNT(*) AS tx_count
FROM transactions
WHERE transaction_date REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
GROUP BY account_id, transaction_date
HAVING COUNT(*) > 10
ORDER BY tx_count DESC;
```

---

### 🔴 Advanced (15–20)

**Q15 — CTE + Window: First and Last Transaction Per Account**
For each account, find the first transaction date, last transaction date, and total number of transactions.
```sql
WITH ranked AS (
    SELECT account_id, transaction_date, transaction_id,
           ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY transaction_date ASC)  AS rn_first,
           ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY transaction_date DESC) AS rn_last,
           COUNT(*) OVER (PARTITION BY account_id) AS total_txns
    FROM transactions
    WHERE transaction_date REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
)
SELECT account_id, total_txns,
       MAX(CASE WHEN rn_first = 1 THEN transaction_date END) AS first_tx_date,
       MAX(CASE WHEN rn_last  = 1 THEN transaction_date END) AS last_tx_date
FROM ranked
GROUP BY account_id, total_txns;
```

**Q16 — Overdraft Detection**
Find all checking accounts where the balance is negative and there are transactions
after the balance went negative (potential overdraft abuse).
```sql
WITH neg_balances AS (
    SELECT account_id, balance
    FROM accounts
    WHERE LOWER(account_type) IN ('checking','chequing','chk','current acct','check')
      AND CAST(balance AS DECIMAL(15,2)) < 0
)
SELECT nb.account_id, nb.balance, COUNT(t.transaction_id) AS tx_after_negative
FROM neg_balances nb
JOIN transactions t ON nb.account_id = t.account_id
WHERE LOWER(t.status) IN ('completed','complete')
GROUP BY nb.account_id, nb.balance
HAVING tx_after_negative > 0
ORDER BY tx_after_negative DESC;
```

**Q17 — Cross-table: Customers with No Transactions**
Find customers who have accounts but have made zero transactions (dormant customers).
```sql
SELECT c.customer_id, c.first_name, c.last_name, c.email,
       a.account_id, a.open_date
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
LEFT JOIN transactions t ON a.account_id = t.account_id
WHERE t.transaction_id IS NULL
ORDER BY c.customer_id;
```

**Q18 — Advanced Fraud: Large Outlier Transactions**
Flag transactions that are more than 3 standard deviations above the mean for their transaction type.
```sql
WITH stats AS (
    SELECT transaction_type,
           AVG(CAST(amount AS DECIMAL(15,2)))    AS avg_amount,
           STDDEV(CAST(amount AS DECIMAL(15,2))) AS std_amount
    FROM transactions
    WHERE amount NOT LIKE '%$%' AND amount NOT LIKE '%USD%' AND amount IS NOT NULL
    GROUP BY transaction_type
)
SELECT t.transaction_id, t.account_id, t.transaction_type,
       t.amount, t.transaction_date,
       ROUND((CAST(t.amount AS DECIMAL) - s.avg_amount) / s.std_amount, 2) AS z_score
FROM transactions t
JOIN stats s ON t.transaction_type = s.transaction_type
WHERE (CAST(t.amount AS DECIMAL) - s.avg_amount) / s.std_amount > 3
ORDER BY z_score DESC;
```

**Q19 — Cohort Analysis: Loan Approval by Credit Score Band**
Group loans by the credit score band at origination and show approval rate, average loan size, and default rate.
```sql
WITH banded AS (
    SELECT loan_id, loan_type, loan_amount, loan_status,
           CASE
               WHEN credit_score_at_origination >= 750 THEN 'Excellent (750+)'
               WHEN credit_score_at_origination >= 700 THEN 'Good (700-749)'
               WHEN credit_score_at_origination >= 650 THEN 'Fair (650-699)'
               WHEN credit_score_at_origination >= 600 THEN 'Poor (600-649)'
               ELSE 'Very Poor (<600)'
           END AS score_band
    FROM loans
    WHERE credit_score_at_origination IS NOT NULL
      AND credit_score_at_origination BETWEEN 300 AND 850
)
SELECT score_band,
       COUNT(*)   AS total_loans,
       ROUND(AVG(CAST(loan_amount AS DECIMAL(15,2))),2) AS avg_loan_size,
       SUM(CASE WHEN LOWER(loan_status) IN ('defaulted','delinquent','past due','bad debt') THEN 1 ELSE 0 END) AS defaults,
       ROUND(100.0 * SUM(CASE WHEN LOWER(loan_status) IN ('defaulted','delinquent','past due','bad debt') THEN 1 ELSE 0 END) / COUNT(*),2) AS default_pct
FROM banded
GROUP BY score_band
ORDER BY MIN(credit_score_at_origination) DESC;
```

**Q20 — Full Pipeline: Branch Performance Scorecard**
Build a branch scorecard showing: total customers, total deposits, total active loans,
average credit score, and number of high-risk customers.
```sql
WITH branch_customers AS (
    SELECT branch_id, COUNT(DISTINCT customer_id) AS total_customers,
           AVG(CASE WHEN credit_score REGEXP '^[0-9]+$' THEN CAST(credit_score AS UNSIGNED) END) AS avg_credit_score,
           SUM(CASE WHEN LOWER(is_high_risk) IN ('yes','true','1') THEN 1 ELSE 0 END) AS high_risk_count
    FROM customers
    GROUP BY branch_id
),
branch_deposits AS (
    SELECT a.branch_id,
           SUM(CASE WHEN LOWER(t.transaction_type) = 'deposit'
                     AND t.amount NOT LIKE '%$%'
                    THEN CAST(t.amount AS DECIMAL(15,2)) ELSE 0 END) AS total_deposits
    FROM accounts a
    JOIN transactions t ON a.account_id = t.account_id
    GROUP BY a.branch_id
),
branch_loans AS (
    SELECT branch_id, COUNT(*) AS active_loans
    FROM loans
    WHERE LOWER(loan_status) IN ('active','open','current')
    GROUP BY branch_id
)
SELECT b.branch_id, b.branch_name, b.city, b.region,
       COALESCE(bc.total_customers, 0)  AS total_customers,
       COALESCE(bd.total_deposits, 0)   AS total_deposits,
       COALESCE(bl.active_loans, 0)     AS active_loans,
       ROUND(bc.avg_credit_score, 0)    AS avg_credit_score,
       COALESCE(bc.high_risk_count, 0)  AS high_risk_customers
FROM branches b
LEFT JOIN branch_customers bc ON b.branch_id = bc.branch_id
LEFT JOIN branch_deposits  bd ON b.branch_id = bd.branch_id
LEFT JOIN branch_loans     bl ON b.branch_id = bl.branch_id
ORDER BY total_deposits DESC;
```

---

## 3. PYTHON / PANDAS CLEANING EXERCISES

### Exercise 1 — Standardize Names
```python
import pandas as pd

customers = pd.read_csv("customers.csv")

# Strip whitespace, title-case, handle reversed names
customers["first_name"] = customers["first_name"].str.strip().str.title()
customers["last_name"]  = customers["last_name"].str.strip().str.title()

# Flag reversed names (Last, First pattern) — no comma here, detect by
# checking if last_name contains a space (could be reversed full name)
customers["name_suspect"] = customers["last_name"].str.contains(r"\s", na=False)
print(customers[customers["name_suspect"]][["first_name","last_name"]].head(10))
```

### Exercise 2 — Normalize Date Columns
```python
from dateutil import parser

def safe_parse_date(val):
    if pd.isna(val) or str(val).strip() in ["", "NULL", "N/A"]:
        return pd.NaT
    try:
        return pd.to_datetime(parser.parse(str(val).strip(), dayfirst=False))
    except:
        return pd.NaT

customers["dob_clean"] = customers["date_of_birth"].apply(safe_parse_date)
customers["dob_clean"] = pd.to_datetime(customers["dob_clean"], errors="coerce")

# Flag impossible ages
today = pd.Timestamp("2024-01-01")
customers["age"] = ((today - customers["dob_clean"]).dt.days / 365.25).round(1)
customers["age_flag"] = (customers["age"] < 0) | (customers["age"] > 110)
print(f"Impossible ages found: {customers['age_flag'].sum()}")
```

### Exercise 3 — Clean Numeric Amount Columns
```python
import re

def clean_amount(val):
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    s = str(val).strip().replace(",", ".")
    s = re.sub(r"[^\d.\-]", "", s)   # remove $, USD, spaces
    try:
        return float(s)
    except:
        return None

accounts = pd.read_csv("accounts.csv")
accounts["balance_clean"] = accounts["balance"].apply(clean_amount)

# Detect cents errors (balance > 1,000,000 on a retail account)
accounts["cents_error_flag"] = accounts["balance_clean"] > 1_000_000
print(f"Possible cents errors: {accounts['cents_error_flag'].sum()}")

# Divide by 100 to correct cents errors
accounts.loc[accounts["cents_error_flag"], "balance_clean"] /= 100
```

### Exercise 4 — Remove Duplicate Customers
```python
# Identify and deduplicate
dupes = customers[customers.duplicated(subset=["customer_id"], keep=False)]
print(f"Total duplicate rows: {len(dupes)}")

# Keep first occurrence, flag rest
customers["is_duplicate"] = customers.duplicated(subset=["customer_id"], keep="first")
customers_clean = customers[~customers["is_duplicate"]].copy()
print(f"Clean customer count: {len(customers_clean)}")
```

### Exercise 5 — Standardize Credit Score
```python
def clean_credit_score(val):
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    s = str(val).strip().lower().replace("pts","").replace("points","").strip()
    try:
        score = int(float(s))
        return score if 300 <= score <= 850 else None   # invalid range → None
    except:
        return None

customers["credit_score_clean"] = customers["credit_score"].apply(clean_credit_score)
invalid = customers["credit_score"].notna() & customers["credit_score_clean"].isna()
print(f"Invalid credit scores cleaned: {invalid.sum()}")
```

### Exercise 6 — Normalize Phone Numbers
```python
def normalize_phone(val):
    if val is None or str(val).strip() in ["", "N/A", "000-000-0000"]:
        return None
    digits = re.sub(r"\D", "", str(val))
    if digits.startswith("1") and len(digits) == 11:
        digits = digits[1:]
    if len(digits) != 10:
        return None
    return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"

customers["phone_clean"] = customers["phone"].apply(normalize_phone)
nulled = customers["phone_clean"].isna().sum()
print(f"Unparseable phones set to null: {nulled}")
```

### Exercise 7 — Standardize Account Type
```python
ACCT_MAP = {
    r"check|chk|chequing|current": "Checking",
    r"sav|svgs":                    "Savings",
    r"biz|bus|buisness|business":   "Business",
    r"money\s*mkt|money\s*market|mm$": "Money Market",
}

def standardize_account_type(val):
    if pd.isna(val): return None
    v = str(val).strip().lower()
    for pattern, label in ACCT_MAP.items():
        if re.search(pattern, v):
            return label
    return str(val).strip().title()

accounts["account_type_clean"] = accounts["account_type"].apply(standardize_account_type)
print(accounts["account_type_clean"].value_counts())
```

### Exercise 8 — Detect Transactions Before Account Opening
```python
transactions = pd.read_csv("transactions.csv")
accounts = pd.read_csv("accounts.csv")

def safe_date(val):
    try: return pd.to_datetime(str(val).strip())
    except: return pd.NaT

transactions["tx_dt"]   = transactions["transaction_date"].apply(safe_date)
accounts["open_dt"]     = accounts["open_date"].apply(safe_date)

merged = transactions.merge(accounts[["account_id","open_dt"]], on="account_id", how="left")
time_paradox = merged[merged["tx_dt"] < merged["open_dt"]]
print(f"Transactions before account open date: {len(time_paradox)}")
```

### Exercise 9 — Detect Outlier Transactions with IQR
```python
transactions["amount_clean"] = transactions["amount"].apply(clean_amount)
tx_clean = transactions["amount_clean"].dropna()

Q1 = tx_clean.quantile(0.25)
Q3 = tx_clean.quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 3 * IQR
upper = Q3 + 3 * IQR

outliers = transactions[(transactions["amount_clean"] < lower) |
                         (transactions["amount_clean"] > upper)]
print(f"Outlier transactions: {len(outliers)}")
print(f"  Upper bound: ${upper:,.2f}")
print(outliers["amount_clean"].describe())
```

### Exercise 10 — Standardize Loan Status
```python
loans = pd.read_csv("loans.csv")

STATUS_MAP = {
    r"active|open|current|in progress":         "Active",
    r"paid|closed|completed":                   "Paid Off",
    r"default|bad debt|charged":                "Defaulted",
    r"delinquent|late|past due":                "Delinquent",
}

def standardize_loan_status(val):
    if pd.isna(val): return None
    v = str(val).strip().lower()
    for pattern, label in STATUS_MAP.items():
        if re.search(pattern, v):
            return label
    return str(val).strip()

loans["loan_status_clean"] = loans["loan_status"].apply(standardize_loan_status)
print(loans["loan_status_clean"].value_counts())
```

### Exercise 11 — Validate Null Foreign Keys
```python
# Accounts with no valid customer_id
orphan_accounts = accounts[~accounts["customer_id"].isin(customers["customer_id"])]
print(f"Orphan accounts (no valid customer): {len(orphan_accounts)}")

# Loans with no valid customer_id
orphan_loans = loans[~loans["customer_id"].isin(customers["customer_id"])]
print(f"Orphan loans (no valid customer): {len(orphan_loans)}")
```

### Exercise 12 — Build a Complete Cleaning Pipeline
```python
def full_clean_customers(df):
    df = df.copy()
    df = df.drop_duplicates(subset=["customer_id"])
    df["first_name"]         = df["first_name"].str.strip().str.title()
    df["last_name"]          = df["last_name"].str.strip().str.title()
    df["email"]              = df["email"].apply(lambda x:
        x.strip().lower() if isinstance(x, str) and "@" in x else None)
    df["phone_clean"]        = df["phone"].apply(normalize_phone)
    df["credit_score_clean"] = df["credit_score"].apply(clean_credit_score)
    df["dob_clean"]          = df["date_of_birth"].apply(safe_parse_date)
    df["annual_income_clean"]= df["annual_income"].apply(clean_amount)
    df["state_clean"]        = df["state"].apply(
        lambda x: x.strip().upper() if isinstance(x, str) and len(x.strip()) == 2 else None)
    df["kyc_clean"]          = df["kyc_status"].str.strip().str.title()
    return df

customers_final = full_clean_customers(customers)
print(customers_final.dtypes)
print(f"\nRows after cleaning: {len(customers_final)}")
```

### Exercise 13 — Email Validation with Regex
```python
EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")

def validate_email(val):
    if pd.isna(val) or str(val).strip() in ["", "N/A", "none", "NULL"]:
        return None
    val = str(val).strip()
    return val if EMAIL_RE.match(val) else None

customers["email_clean"] = customers["email"].apply(validate_email)
invalid_emails = customers["email"].notna() & customers["email_clean"].isna()
print(f"Invalid emails found: {invalid_emails.sum()}")
```

### Exercise 14 — Feature Engineering: Customer Risk Score
```python
def build_risk_features(customers, accounts, loans):
    # Aggregate account balances
    acc_agg = accounts.copy()
    acc_agg["balance_clean"] = acc_agg["balance"].apply(clean_amount)
    acc_summary = acc_agg.groupby("customer_id")["balance_clean"].agg(
        total_balance="sum", num_accounts="count").reset_index()

    # Loan defaults
    loans_clean = loans.copy()
    loans_clean["is_bad"] = loans_clean["loan_status"].str.lower().str.contains(
        "default|delinquent|past due|bad debt", na=False).astype(int)
    loan_summary = loans_clean.groupby("customer_id").agg(
        num_loans=("loan_id","count"),
        num_bad_loans=("is_bad","sum")).reset_index()

    # Merge
    features = customers[["customer_id","credit_score_clean"]].merge(
        acc_summary, on="customer_id", how="left").merge(
        loan_summary, on="customer_id", how="left")

    features["risk_score"] = (
        (features["num_bad_loans"].fillna(0) * 3) +
        (features["total_balance"].fillna(0) < 0).astype(int) * 2 +
        (features["credit_score_clean"].fillna(700) < 600).astype(int) * 2
    )
    return features

# risk_df = build_risk_features(customers_final, accounts, loans)
```

### Exercise 15 — Data Quality Report
```python
def data_quality_report(df, name):
    print(f"\n{'='*50}")
    print(f"  Data Quality Report: {name}")
    print(f"  Rows: {len(df):,}  |  Columns: {len(df.columns)}")
    print(f"{'='*50}")
    report = []
    for col in df.columns:
        null_count = df[col].isna().sum()
        null_pct   = round(100 * null_count / len(df), 1)
        unique     = df[col].nunique()
        dtype      = str(df[col].dtype)
        report.append({"column": col, "nulls": null_count,
                        "null_%": null_pct, "unique_vals": unique, "dtype": dtype})
    print(pd.DataFrame(report).to_string(index=False))

# data_quality_report(customers, "customers")
# data_quality_report(transactions, "transactions")
```

---

## 4. DATA VALIDATION CHECKS

```python
# ── CHECK 1: No negative balances on Savings accounts ──────────────────
savings_neg = accounts[
    accounts["account_type"].str.lower().str.contains("sav", na=False) &
    (accounts["balance"].apply(clean_amount).fillna(0) < 0)
]
print(f"CHECK 1 FAIL — Savings with negative balance: {len(savings_neg)}")

# ── CHECK 2: Transactions before account open date ─────────────────────
# (see Exercise 8 above)
print(f"CHECK 2 FAIL — Temporal paradoxes: {len(time_paradox)}")

# ── CHECK 3: Duplicate transaction IDs ────────────────────────────────
dup_tx = transactions[transactions.duplicated(subset=["transaction_id"])]
print(f"CHECK 3 FAIL — Duplicate transaction_ids: {len(dup_tx)}")

# ── CHECK 4: Invalid credit scores ────────────────────────────────────
cs = pd.to_numeric(customers["credit_score"], errors="coerce")
invalid_cs = cs[(cs < 300) | (cs > 850)].count()
print(f"CHECK 4 FAIL — Credit scores out of range [300,850]: {invalid_cs}")

# ── CHECK 5: Orphan transactions (no valid account_id) ────────────────
orphan_tx = transactions[~transactions["account_id"].isin(accounts["account_id"])]
print(f"CHECK 5 FAIL — Transactions with no valid account: {len(orphan_tx)}")

# ── CHECK 6: Loans with amount > 10x customer income ──────────────────
loans_inc = loans.merge(customers[["customer_id","annual_income"]], on="customer_id")
loans_inc["loan_amt_c"] = loans_inc["loan_amount"].apply(clean_amount)
loans_inc["income_c"]   = loans_inc["annual_income"].apply(clean_amount)
excessive = loans_inc[(loans_inc["loan_amt_c"] > loans_inc["income_c"] * 10)]
print(f"CHECK 6 WARN — Loans > 10x annual income: {len(excessive)}")

# ── CHECK 7: Emails without @ symbol ─────────────────────────────────
bad_emails = customers[
    customers["email"].notna() &
    ~customers["email"].astype(str).str.contains("@", na=False) &
    ~customers["email"].isin(["N/A","","none","NULL"])
]
print(f"CHECK 7 FAIL — Malformed emails: {len(bad_emails)}")

# ── CHECK 8: Invalid state codes ──────────────────────────────────────
valid_states = {"AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID",
                "IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS",
                "MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK",
                "OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC"}
bad_states = customers[~customers["state"].isin(valid_states)]
print(f"CHECK 8 FAIL — Invalid state codes: {len(bad_states)}")

# ── CHECK 9: Duplicate customer records ───────────────────────────────
cust_dupes = customers[customers.duplicated(subset=["customer_id"], keep=False)]
print(f"CHECK 9 FAIL — Duplicate customer rows: {len(cust_dupes)}")

# ── CHECK 10: Impossible ages (born in future or age > 110) ──────────
customers["dob_parsed"] = pd.to_datetime(customers["date_of_birth"], errors="coerce")
today = pd.Timestamp("2024-01-01")
customers["age_check"] = ((today - customers["dob_parsed"]).dt.days / 365.25)
bad_ages = customers[(customers["age_check"] < 0) | (customers["age_check"] > 110)]
print(f"CHECK 10 FAIL — Impossible ages: {len(bad_ages)}")
```

---

## 5. BUSINESS ANALYTICS SCENARIOS

**Scenario 1 — Customer Lifetime Value (CLV)**
> "The marketing team wants to rank customers by estimated CLV to target the top 20% for a premium rewards program."

*Approach:* Join customers → accounts → transactions. Calculate total transaction volume per customer, account tenure in years, average monthly balance, and number of products held. Normalize and weight these into a CLV score. Segment into quintiles.

---

**Scenario 2 — Branch Profitability Report**
> "The CFO needs a quarterly profitability summary per branch, factoring in deposit volumes, loan interest income, fee revenue, and estimated credit losses from defaults."

*Approach:* Aggregate total deposits and withdrawals per branch (via accounts → transactions). Calculate estimated interest income from active loans. Subtract estimated losses from defaulted/delinquent loans. Factor in monthly fees across accounts.

---

**Scenario 3 — Early Warning: Loan Default Prediction**
> "The risk team wants to flag customers who show early signs of default — rising days-past-due, multiple missed payments, and declining account balances."

*Approach:* Join loans + customers + accounts. Create features: `days_past_due`, `num_missed_payments`, `balance_trend` (requires time-series), `credit_score_band`. Apply a rule-based scoring model. Flag customers crossing threshold for review.

---

**Scenario 4 — Fraud Pattern Analysis**
> "The fraud team has noticed unusual transaction spikes from certain accounts. Build a monitor that flags accounts with: > 5 transactions in 1 hour, transactions in 3+ different cities in 1 day, or amounts > 5x the account's 90-day average."

*Approach:* Use `transaction_timestamp` (after cleaning) for velocity checks. Join with customer location for geo-anomaly detection. Compute rolling 90-day average per account and z-score each transaction.

---

**Scenario 5 — Product Cross-Sell Opportunity**
> "The retail banking director wants to identify customers who only have a checking account and no savings, loan, or investment product — the highest-potential cross-sell segment."

*Approach:* Aggregate account types per customer. Filter for customers with exactly one product (Checking only). Join with credit score and income to score their eligibility for savings, CD, or loan products. Rank by branch for targeted outreach.

---

*Generated with Python + Faker | Seed = 42 | Reproducible*
