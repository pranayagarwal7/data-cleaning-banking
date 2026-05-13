# Data Cleaning — Retail Banking

Synthetic retail banking dataset with intentionally messy data for SQL, Python, and data quality practice.

## Structure

```
.
├── data/         # Raw messy CSVs (branches, customers, accounts, transactions, loans)
├── scripts/      # Python scripts (generator, future cleaning utils)
├── notebooks/    # Jupyter notebooks for exploration / cleaning
├── sql/          # SQL queries and cleaning scripts
└── docs/         # Practice guide and schema docs
```

## Dataset

- `data/branches.csv` — 50 rows
- `data/customers.csv` — ~5,150 rows (includes duplicates)
- `data/accounts.csv`
- `data/loans.csv`
- `data/transactions.csv`

See [`docs/PRACTICE_GUIDE.md`](docs/PRACTICE_GUIDE.md) for schemas, known issues, and practice exercises.

## Known data quality issues

Mixed casing, inconsistent date formats, invalid state abbreviations, mixed boolean encodings (Yes/No/1/0/TRUE), duplicate customer rows, impossible future birthdates, blank/N/A emails, mixed phone formats. Full list in practice guide.

## Regenerate dataset

```bash
pip install pandas numpy
python scripts/generate_banking.py
```

Writes CSVs into `data/`.

## License

MIT
