"""
========================================================
 SYNTHETIC RETAIL BANKING DATASET GENERATOR
 Senior Data Engineer: Intentionally Messy Data
 For SQL, Python, and Data Quality Practice
========================================================
"""

import pandas as pd
import numpy as np
import random
import re
import os
from datetime import datetime, timedelta
from faker import Faker

fake = Faker("en_US")
Faker.seed(42)
np.random.seed(42)
random.seed(42)

OUTPUT_DIR = "/mnt/user-data/outputs/banking_dataset"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────
# UTILITY HELPERS
# ─────────────────────────────────────────────

def rand_date(start, end):
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

def corrupt_phone(phone):
    """INTENTIONAL: Mixed phone formats"""
    digits = re.sub(r"\D", "", phone)[:10].ljust(10, "0")
    fmt = random.choice([
        f"{digits[:3]}-{digits[3:6]}-{digits[6:]}",
        f"({digits[:3]}) {digits[3:6]}-{digits[6:]}",
        f"+1{digits}",
        f"{digits[:3]}.{digits[3:6]}.{digits[6:]}",
        digits,
        f"+1-{digits[:3]}-{digits[3:6]}-{digits[6:]}",
        "N/A", "", "000-000-0000",
    ])
    return fmt

def corrupt_email(email):
    """INTENTIONAL: Email formatting issues"""
    choice = random.random()
    if choice < 0.05:  return ""
    if choice < 0.08:  return "N/A"
    if choice < 0.10:  return email.replace("@", "AT")
    if choice < 0.12:  return email.upper()
    if choice < 0.14:  return "  " + email + "  "   # trailing spaces
    return email

def corrupt_date(dt, fmt_pool=None):
    """INTENTIONAL: Mixed date formats + invalid dates"""
    if dt is None: return None
    if random.random() < 0.04: return "99/99/9999"       # impossible date
    if random.random() < 0.03: return ""                  # blank
    if random.random() < 0.02: return "NULL"
    formats = fmt_pool or [
        "%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y",
        "%B %d, %Y", "%y-%m-%d", "%d/%m/%Y",
    ]
    return dt.strftime(random.choice(formats))

def corrupt_amount(amount, allow_currency=True):
    """INTENTIONAL: Currency symbols, commas, wrong units, None"""
    if amount is None: return None
    if random.random() < 0.06: return None
    if random.random() < 0.04: return f"${amount:,.2f}"
    if random.random() < 0.03: return f"USD {amount:.2f}"
    if random.random() < 0.02: return str(amount).replace(".", ",")  # European
    if random.random() < 0.015: return amount * 100                  # cents error
    return round(amount, 2)

def corrupt_name(name):
    """INTENTIONAL: Inconsistent casing, spacing, extra tokens"""
    styles = [
        name.upper(), name.lower(), name.title(),
        name + "  ",                          # trailing space
        "  " + name,                          # leading space
        name.replace(" ", "  "),              # double space
        " ".join(reversed(name.split())),     # reversed
    ]
    return random.choice(styles) if random.random() < 0.35 else name

def corrupt_state(state):
    """INTENTIONAL: Wrong/invalid state abbreviations"""
    if random.random() < 0.06:
        return random.choice(["ZZ", "XX", "US", "00", "N/A", state.lower(), state + " "])
    return state

def corrupt_account_type(atype):
    """INTENTIONAL: Inconsistent account type spellings"""
    variants = {
        "Checking":  ["checking","CHECKING","Chequing","chk","CHK","Current Acct","Checkng","check"],
        "Savings":   ["savings","SAVINGS","Saving","SAV","sav","svgs","Savngs","Saving Acct"],
        "Business":  ["business","BUSINESS","Biz","BUS","business acct","Buisness"],
        "Money Market": ["money market","Money Mkt","MM","money mkt","MoneyMarket","MONEY MARKET"],
    }
    return random.choice(variants.get(atype, [atype])) if random.random() < 0.45 else atype

def corrupt_loan_status(status):
    """INTENTIONAL: Inconsistent loan status labels"""
    variants = {
        "Active":    ["active","ACTIVE","Open","open","Current","In Progress"],
        "Paid Off":  ["paid off","PAID OFF","Closed","closed","Paid","paid","Completed"],
        "Defaulted": ["defaulted","DEFAULTED","Default","DEFAULT","Bad Debt","charged off","Charged Off"],
        "Delinquent":["delinquent","DELINQUENT","Late","late","Past Due","PAST DUE","past due"],
    }
    return random.choice(variants.get(status, [status])) if random.random() < 0.40 else status

def corrupt_gender(g):
    variants = {"M": ["M","Male","male","MALE","m","1"],
                "F": ["F","Female","female","FEMALE","f","0"]}
    return random.choice(variants.get(g, [g]))

# ─────────────────────────────────────────────
# 1. BRANCHES  (50 rows)
# ─────────────────────────────────────────────
print("Generating branches...")

CITIES = [
    ("New York","NY"),("Los Angeles","CA"),("Chicago","IL"),("Houston","TX"),
    ("Phoenix","AZ"),("Philadelphia","PA"),("San Antonio","TX"),("San Diego","CA"),
    ("Dallas","TX"),("San Jose","CA"),("Austin","TX"),("Jacksonville","FL"),
    ("Fort Worth","TX"),("Columbus","OH"),("Charlotte","NC"),("Indianapolis","IN"),
    ("San Francisco","CA"),("Seattle","WA"),("Denver","CO"),("Nashville","TN"),
    ("Oklahoma City","OK"),("El Paso","TX"),("Washington","DC"),("Las Vegas","NV"),
    ("Louisville","KY"),("Memphis","TN"),("Portland","OR"),("Baltimore","MD"),
    ("Milwaukee","WI"),("Albuquerque","NM"),("Tucson","AZ"),("Fresno","CA"),
    ("Sacramento","CA"),("Mesa","AZ"),("Kansas City","MO"),("Atlanta","GA"),
    ("Omaha","NE"),("Colorado Springs","CO"),("Raleigh","NC"),("Long Beach","CA"),
    ("Virginia Beach","VA"),("Minneapolis","MN"),("Tampa","FL"),("New Orleans","LA"),
    ("Arlington","TX"),("Wichita","KS"),("Aurora","CO"),("Bakersfield","CA"),
    ("Anaheim","CA"),("Santa Ana","CA"),
]

REGIONS = {
    "NY":"Northeast","PA":"Northeast","MD":"Northeast","DC":"Northeast",
    "CA":"West","WA":"West","OR":"West","NV":"West","AZ":"West",
    "TX":"South","FL":"South","GA":"South","NC":"South","TN":"South",
    "VA":"South","LA":"South","OK":"South",
    "IL":"Midwest","OH":"Midwest","MO":"Midwest","IN":"Midwest",
    "WI":"Midwest","MN":"Midwest","NE":"Midwest","KS":"Midwest",
    "CO":"Mountain","NM":"Mountain","KY":"South",
}

branch_rows = []
for i, (city, state) in enumerate(CITIES):
    bid = f"BR{str(i+1).zfill(3)}"
    row = {
        "branch_id":       bid,
        "branch_name":     f"{city} {random.choice(['Main','Downtown','Uptown','North','South','East','West','Central'])} Branch",
        "city":            city if random.random() > 0.05 else city.lower(),      # INTENTIONAL: casing
        "state":           corrupt_state(state),
        "region":          REGIONS.get(state, "Other"),
        "zip_code":        fake.zipcode(),
        "phone":           corrupt_phone(fake.phone_number()),
        "manager_name":    corrupt_name(fake.name()),
        "open_since":      corrupt_date(rand_date(datetime(1985,1,1), datetime(2020,12,31))),
        "num_employees":   random.choice([None if random.random()<0.05 else random.randint(5,120)]),
        "is_active":       random.choice(["Yes","No","TRUE","FALSE","1","0","Active","Inactive",True,False]),  # INTENTIONAL: mixed bool
    }
    branch_rows.append(row)

branches_df = pd.DataFrame(branch_rows)
branch_ids = branches_df["branch_id"].tolist()

# ─────────────────────────────────────────────
# 2. CUSTOMERS  (5,000 rows)
# ─────────────────────────────────────────────
print("Generating customers...")

OCCUPATIONS = ["Engineer","Teacher","Doctor","Nurse","Lawyer","Accountant","Manager",
               "Sales Rep","Analyst","Developer","Designer","Driver","Chef","Consultant",
               "Retired","Student","Self-Employed","Contractor","Clerk","Officer"]

customer_rows = []
used_ids = set()
for i in range(5000):
    cid = f"CUST{str(i+1).zfill(6)}"
    dob = rand_date(datetime(1940,1,1), datetime(2005,12,31))
    age = (datetime(2024,1,1) - dob).days // 365
    gender = random.choice(["M","F"])
    income = max(0, np.random.normal(70000, 35000))

    # INTENTIONAL: Impossible ages (negative or >120)
    if random.random() < 0.02:
        dob = rand_date(datetime(2010,1,1), datetime(2025,1,1))  # future/child dob

    row = {
        "customer_id":    cid,
        "first_name":     corrupt_name(fake.first_name()),
        "last_name":      corrupt_name(fake.last_name()),
        "date_of_birth":  corrupt_date(dob),
        "gender":         corrupt_gender(gender) if random.random() < 0.3 else gender,
        "email":          corrupt_email(fake.email()),
        "phone":          corrupt_phone(fake.phone_number()),
        "address":        fake.street_address() if random.random() > 0.05 else None,
        "city":           fake.city() if random.random() > 0.04 else None,
        "state":          corrupt_state(fake.state_abbr()),
        "zip_code":       fake.zipcode() if random.random() > 0.03 else "00000",
        "annual_income":  corrupt_amount(round(income, 2)),
        "occupation":     random.choice(OCCUPATIONS) if random.random() > 0.05 else None,
        "credit_score":   (
            random.choice([None, 9999, -1, 0]) if random.random() < 0.06
            else (str(random.randint(300,850)) + " pts" if random.random() < 0.04
                  else random.randint(300, 850))
        ),                                                           # INTENTIONAL: invalid + mixed type
        "customer_since": corrupt_date(rand_date(datetime(2000,1,1), datetime(2023,12,31))),
        "branch_id":      (random.choice(branch_ids) if random.random() > 0.04
                           else None),                               # INTENTIONAL: null FK
        "is_high_risk":   random.choice(["Yes","No","TRUE","FALSE","1","0",True,False,None]),
        "kyc_status":     random.choice(["Verified","Not Verified","Pending","VERIFIED",
                                          "verified","N/A","","pending"]),
        "nationality":    fake.country() if random.random() > 0.06 else None,
        "referral_source":random.choice(["Online","Branch","Referral","Marketing","Walk-in",
                                          "online","ONLINE","branch","N/A",None]),
    }
    customer_rows.append(row)

customers_df = pd.DataFrame(customer_rows)
customer_ids = customers_df["customer_id"].tolist()

# INTENTIONAL: Inject ~3% duplicate customer records (same person, slightly different data)
dup_count = int(0.03 * len(customers_df))
dupes = customers_df.sample(dup_count).copy()
dupes["customer_id"] = dupes["customer_id"]  # same ID — true duplicate
dupes["email"] = dupes["email"].apply(lambda x: str(x).upper() if isinstance(x, str) else x)
dupes["phone"] = dupes["phone"].apply(lambda _: corrupt_phone(fake.phone_number()))
customers_df = pd.concat([customers_df, dupes]).reset_index(drop=True)

# ─────────────────────────────────────────────
# 3. ACCOUNTS  (8,000 rows)
# ─────────────────────────────────────────────
print("Generating accounts...")

ACCOUNT_TYPES = ["Checking","Savings","Business","Money Market"]

account_rows = []
used_acc_ids = set()
for i in range(8000):
    aid = f"ACC{str(random.randint(1000000,9999999))}"
    while aid in used_acc_ids:
        aid = f"ACC{str(random.randint(1000000,9999999))}"
    used_acc_ids.add(aid)

    atype_clean = random.choice(ACCOUNT_TYPES)
    open_dt = rand_date(datetime(2000,1,1), datetime(2023,12,31))
    balance = np.random.exponential(scale=4000)

    # INTENTIONAL: Negative balances on Savings (should be impossible)
    if atype_clean == "Savings" and random.random() < 0.04:
        balance = -abs(balance)

    row = {
        "account_id":      aid,
        "customer_id":     (random.choice(customer_ids) if random.random() > 0.03
                            else None),                              # INTENTIONAL: null FK
        "branch_id":       (random.choice(branch_ids) if random.random() > 0.04
                            else None),
        "account_type":    corrupt_account_type(atype_clean),
        "account_status":  random.choice(["Active","Inactive","Closed","Frozen",
                                           "active","ACTIVE","closed","CLOSED",
                                           "Open","open","Suspended","N/A"]),
        "open_date":       corrupt_date(open_dt),
        "close_date":      (corrupt_date(rand_date(open_dt, datetime(2024,1,1)))
                            if random.random() < 0.15 else None),
        "balance":         corrupt_amount(round(balance, 2)),
        "currency":        random.choice(["USD","usd","US Dollar","$","USD ","EUR","GBP",None]),
        "interest_rate":   (round(random.uniform(0.01, 5.5), 4)
                            if random.random() > 0.06 else None),
        "overdraft_limit": (corrupt_amount(round(random.choice([0,100,250,500,1000]),2))
                            if random.random() > 0.1 else None),
        "monthly_fee":     round(random.choice([0,5,10,12,15,25]), 2),
        "account_number":  f"{''.join([str(random.randint(0,9)) for _ in range(12)])}",
    }
    account_rows.append(row)

accounts_df = pd.DataFrame(account_rows)
account_ids = accounts_df["account_id"].tolist()

# ─────────────────────────────────────────────
# 4. TRANSACTIONS  (100,000 rows)
# ─────────────────────────────────────────────
print("Generating transactions... (this may take a moment)")

TX_TYPES = ["Deposit","Withdrawal","Transfer","Fee","Purchase","Refund","Interest","ATM Withdrawal"]
MERCHANTS = [
    "Amazon","Walmart","Target","Costco","Starbucks","McDonald's","Shell Gas","CVS Pharmacy",
    "Home Depot","Best Buy","Uber","Netflix","Spotify","Apple Store","Whole Foods",
    "Trader Joe's","7-Eleven","Walgreens","Dollar Tree","IKEA","Nike","Zara","H&M",
    "Airbnb","Delta Airlines","Marriott Hotels","Lyft","DoorDash","Grubhub","PayPal",
    "Venmo","Stripe","Square","Chase ATM","Wells Fargo ATM","Bank of America ATM",
]

def corrupt_tx_type(t):
    """INTENTIONAL: Typos in transaction type"""
    typos = {
        "Withdrawal": ["Withdrawl","withdrawl","WITHDRAWAL","Withdraawl","WithDrawal"],
        "Deposit":    ["Deposite","deposite","DEPOSIT","Depoist","dposit"],
        "Transfer":   ["Tranfer","TRANSFER","Trasfer","Transfr"],
        "Purchase":   ["Purchse","PURCHASE","Purhcase","purchse"],
        "Fee":        ["fee","FEE","Fees","FEES"],
    }
    if t in typos and random.random() < 0.07:
        return random.choice(typos[t])
    return t

tx_rows = []
for i in range(100000):
    tid = f"TXN{str(i+1).zfill(8)}"
    acc = random.choice(account_ids)
    tx_type_clean = random.choice(TX_TYPES)
    amount = abs(np.random.exponential(scale=200))

    # INTENTIONAL: Outlier transaction amounts
    if random.random() < 0.01:
        amount = random.uniform(50000, 500000)

    # INTENTIONAL: Negative amounts on deposits (should be positive)
    if tx_type_clean == "Deposit" and random.random() < 0.03:
        amount = -abs(amount)

    tx_dt = rand_date(datetime(2018,1,1), datetime(2024,6,30))

    # INTENTIONAL: Transactions before account open date (time paradox)
    if random.random() < 0.025:
        tx_dt = rand_date(datetime(2000,1,1), datetime(2005,12,31))

    row = {
        "transaction_id":    tid,
        "account_id":        acc if random.random() > 0.02 else None,  # INTENTIONAL: null FK
        "transaction_type":  corrupt_tx_type(tx_type_clean),
        "amount":            corrupt_amount(round(amount, 2)),
        "currency":          random.choice(["USD","USD","USD","USD","EUR","GBP","usd"]),
        "transaction_date":  corrupt_date(tx_dt, ["%Y-%m-%d","%m/%d/%Y","%d-%m-%Y","%Y/%m/%d"]),
        "transaction_timestamp": (
            tx_dt.strftime("%Y-%m-%d %H:%M:%S") if random.random() > 0.06
            else None
        ),
        "merchant_name":     (
            random.choice(MERCHANTS) if tx_type_clean in ["Purchase","Fee"]
            else (random.choice(MERCHANTS) if random.random() < 0.3 else None)
        ),
        "merchant_category": random.choice(["Retail","Food & Beverage","Travel","Healthcare",
                                             "Entertainment","Utilities","Finance","Other",
                                             "retail","RETAIL",None]),
        "description":       random.choice([
            "Online purchase","POS transaction","ATM","Direct deposit","Wire transfer",
            "Bill payment","Subscription","Refund","Interest credit","Overdraft fee",
            "Monthly maintenance fee","Peer transfer","Check deposit",None,"",
        ]),
        "balance_after":     corrupt_amount(round(random.uniform(-500, 50000), 2)),
        "channel":           random.choice(["Online","Mobile","Branch","ATM","Phone",
                                            "online","ONLINE","mobile","N/A",None]),
        "status":            random.choice(["Completed","Pending","Failed","Reversed",
                                            "completed","COMPLETED","pending","failed","NULL"]),
        "ip_address":        fake.ipv4() if random.random() > 0.2 else None,
        "device_type":       random.choice(["Mobile","Desktop","Tablet","ATM",None,"mobile","MOBILE"]),
    }
    tx_rows.append(row)

transactions_df = pd.DataFrame(tx_rows)

# INTENTIONAL: ~2% duplicate transactions (processing error)
dup_tx = transactions_df.sample(int(0.02 * len(transactions_df))).copy()
dup_tx["transaction_id"] = dup_tx["transaction_id"]
transactions_df = pd.concat([transactions_df, dup_tx]).reset_index(drop=True)

# ─────────────────────────────────────────────
# 5. LOANS  (2,000 rows)
# ─────────────────────────────────────────────
print("Generating loans...")

LOAN_TYPES = ["Personal","Mortgage","Auto","Student","Business","Home Equity"]

loan_rows = []
for i in range(2000):
    lid = f"LOAN{str(i+1).zfill(6)}"
    cid = random.choice(customer_ids)
    ltype = random.choice(LOAN_TYPES)
    loan_amount = abs(np.random.normal(loc=35000, scale=25000))
    loan_amount = max(1000, round(loan_amount, 2))

    start_dt = rand_date(datetime(2010,1,1), datetime(2023,6,30))
    term_months = random.choice([12,24,36,48,60,84,120,180,240,360])
    end_dt = start_dt + timedelta(days=term_months * 30)

    status_clean = random.choice(["Active","Paid Off","Defaulted","Delinquent"])

    row = {
        "loan_id":              lid,
        "customer_id":          cid if random.random() > 0.03 else None,   # INTENTIONAL: null FK
        "branch_id":            random.choice(branch_ids) if random.random() > 0.05 else None,
        "loan_type":            ltype if random.random() > 0.1 else ltype.lower(),
        "loan_amount":          corrupt_amount(loan_amount),
        "approved_amount":      corrupt_amount(loan_amount * random.uniform(0.8, 1.0)),
        "outstanding_balance":  corrupt_amount(round(loan_amount * random.uniform(0, 1), 2)),
        "interest_rate":        (round(random.uniform(2.5, 18.0), 3)
                                 if random.random() > 0.05 else None),
        "term_months":          term_months if random.random() > 0.04 else None,
        "start_date":           corrupt_date(start_dt),
        "end_date":             corrupt_date(end_dt),
        "monthly_payment":      corrupt_amount(round(loan_amount / term_months, 2)),
        "loan_status":          corrupt_loan_status(status_clean),
        "collateral_type":      random.choice(["None","Property","Vehicle","Stocks","Savings",
                                                "none","N/A",None,"property","PROPERTY"]),
        "purpose":              random.choice(["Home improvement","Debt consolidation","Education",
                                               "Medical","Travel","Business expansion","Vehicle purchase",
                                               "Wedding","Emergency",None]),
        "days_past_due":        (random.randint(0, 365) if status_clean in ["Defaulted","Delinquent"]
                                 else random.choice([0, None])),
        "num_missed_payments":  (random.randint(1, 24) if status_clean in ["Defaulted","Delinquent"]
                                 else random.choice([0, None])),
        "credit_score_at_origination": (random.randint(300, 850)
                                         if random.random() > 0.08 else None),
        "approved_by":          fake.name() if random.random() > 0.1 else None,
    }
    loan_rows.append(row)

loans_df = pd.DataFrame(loan_rows)

# ─────────────────────────────────────────────
# EXPORT TO CSV
# ─────────────────────────────────────────────
print("\nExporting CSVs...")

branches_df.to_csv(f"{OUTPUT_DIR}/branches.csv", index=False)
customers_df.to_csv(f"{OUTPUT_DIR}/customers.csv", index=False)
accounts_df.to_csv(f"{OUTPUT_DIR}/accounts.csv", index=False)
transactions_df.to_csv(f"{OUTPUT_DIR}/transactions.csv", index=False)
loans_df.to_csv(f"{OUTPUT_DIR}/loans.csv", index=False)

print(f"""
╔══════════════════════════════════════════════════╗
║        DATASET GENERATION COMPLETE               ║
╠══════════════════════════════════════════════════╣
║  branches.csv       → {len(branches_df):>7,} rows               ║
║  customers.csv      → {len(customers_df):>7,} rows               ║
║  accounts.csv       → {len(accounts_df):>7,} rows               ║
║  transactions.csv   → {len(transactions_df):>7,} rows               ║
║  loans.csv          → {len(loans_df):>7,} rows               ║
╚══════════════════════════════════════════════════╝
""")
