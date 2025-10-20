# Python Generators 0x00 — Seeding DB

This step seeds a MySQL database for later generator tasks.

## Files
- `seed.py` — connects to MySQL, creates **ALX_prodev**, creates `user_data` table, and inserts CSV data.
- `0-main.py` — (provided by checker) calls functions from `seed.py`.

## Requirements
- MySQL server running locally
- Python 3.8+
- `pip install mysql-connector-python`
- CSV file: `user_data.csv` with headers:
  `user_id,name,email,age`

## Environment (optional)
You can override defaults with env vars:
