# Data Cleaning — Retail Banking

Synthetic retail banking dataset with intentionally messy data for SQL, Python, and data quality practice.

## Contents

- `branches.csv` — 50 rows
- `customers.csv` — ~5,150 rows (includes duplicates)
- `accounts.csv`
- `loans.csv`
- `transactions.csv`
- `generate_banking.py` — generator script
- `PRACTICE_GUIDE.md` — schema, known issues, practice exercises

## Known data quality issues

Mixed casing, inconsistent date formats, invalid state abbreviations, mixed boolean encodings (Yes/No/1/0/TRUE), duplicate customer rows, impossible future birthdates, blank/N/A emails, mixed phone formats. See `PRACTICE_GUIDE.md` for full list.

## Regenerate

```bash
pip install pandas numpy
python generate_banking.py
```

## License

MIT
