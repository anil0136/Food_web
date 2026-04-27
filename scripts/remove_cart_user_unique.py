#!/usr/bin/env python3
"""
Drops any UNIQUE index on cart_cart.user_id in db.sqlite3.

Usage:
  1. Backup db.sqlite3 first: copy the file somewhere safe.
     e.g. PowerShell: Copy-Item db.sqlite3 db.sqlite3.bak
  2. From project root run: python scripts\remove_cart_user_unique.py
  3. Then run: python manage.py migrate

This script only drops indexes that are unique and only reference the column 'user_id'.
"""
import sqlite3
import os
import sys

DB = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite3')

if not os.path.exists(DB):
    print('Database not found at', DB)
    sys.exit(1)

conn = sqlite3.connect(DB)
cur = conn.cursor()

print('Listing indexes on cart_cart:')
idxs = list(cur.execute("PRAGMA index_list('cart_cart')"))
if not idxs:
    print('No indexes found.')
    conn.close()
    sys.exit(0)

to_drop = []
for idx in idxs:
    # idx format: (seq, name, unique, origin, partial)
    name = idx[1]
    unique = idx[2]
    info = list(cur.execute(f"PRAGMA index_info('{name}')"))
    cols = [row[2] for row in info]
    print(f" - {name}: unique={unique}, columns={cols}")
    if unique == 1 and cols == ['user_id']:
        to_drop.append(name)

if not to_drop:
    print('\nNo unique index on cart_cart.user_id found to drop.')
    conn.close()
    sys.exit(0)

print('\nThe following indexes will be dropped:')
for n in to_drop:
    print(' -', n)

confirm = input('\nDrop these indexes? Type YES to continue: ')
if confirm != 'YES':
    print('Aborted.')
    conn.close()
    sys.exit(0)

for n in to_drop:
    print('Dropping', n)
    cur.execute(f"DROP INDEX IF EXISTS '{n}'")

conn.commit()
conn.close()
print('Done. Run: python manage.py migrate')
