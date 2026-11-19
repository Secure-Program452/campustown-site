#!/usr/bin/env python3
"""Writes data/city_medians.json: the median sale price for each city.

Rule: sales under $10,000 are left out (they are impossible prices; see the
data description sheet, "Some prices are impossible"). Every other sale counts.

Run from the repository root:
    python3 scripts/make_city_medians.py
"""
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "college_town_home_sales.csv"
OUTPUT = ROOT / "data" / "city_medians.json"
MIN_PRICE = 10_000

prices = defaultdict(list)
places = {}
total_rows = 0
excluded_rows = 0

with SOURCE.open(newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        total_rows += 1
        city, state = row["city"], row["state"]
        price = int(row["sale_price"])
        if price < MIN_PRICE:
            excluded_rows += 1
            continue
        key = (city, state)
        prices[key].append(price)
        places[key] = True

cities = []
for (city, state), values in prices.items():
    cities.append({
        "city": city,
        "state": state,
        "label": f"{city}, {state}",
        "sales": len(values),
        # The median of an even number of sales can end in .5, so keep it exact.
        "median_sale_price": statistics.median(values),
    })

cities.sort(key=lambda c: c["median_sale_price"], reverse=True)

output = {
    "source": "data/college_town_home_sales.csv",
    "rule": "Sales under $10,000 are left out. All other sales are counted.",
    "min_sale_price": MIN_PRICE,
    "rows_in_source": total_rows,
    "rows_excluded": excluded_rows,
    "cities": cities,
}

OUTPUT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {OUTPUT.relative_to(ROOT)}: {len(cities)} cities, "
      f"{total_rows - excluded_rows} sales used, {excluded_rows} excluded.")
