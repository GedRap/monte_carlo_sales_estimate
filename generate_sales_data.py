"""
Generate dummy sales data following the normal distribution and save it to daily_sales_data.csv.
Will overwrite existing file.

Example: python generate_sales_data.py "2016-01-01" 182 1000 400
Will generate dummy sales data from 2016-01-01 to 2016-06-30 with mean of $1000/day and
standard deviation of $400.
"""

import argparse

import arrow
import numpy.random
import pandas as pd

arguments_parser = argparse.ArgumentParser()
arguments_parser.add_argument("starting_date", help="Simulation starting date")
arguments_parser.add_argument("days", help="Number of days to simulate", type=int)
arguments_parser.add_argument("mean", help="Mean of daily sales", type=float)
arguments_parser.add_argument("stddev", help="Standard deviation of daily sales", type=float)

args = arguments_parser.parse_args()

starting_date = arrow.get(args.starting_date)

generated_data = {
    "date": list(),
    "day_of_the_week": list(),
    "sales": list()
}

for current_day in range(args.days):
    current_date = starting_date.replace(days=current_day)
    daily_sales = numpy.random.normal(args.mean, args.stddev)

    if daily_sales < 0:
        # this is highly unlikely but negative sales do not make much sense
        daily_sales = 0

    generated_data["date"].append(current_date.format("YYYY-MM-DD"))
    generated_data["day_of_the_week"].append(current_date.format("d"))
    generated_data["sales"].append(daily_sales)

df = pd.DataFrame(generated_data)
df.to_csv("daily_sales_data.csv", index=False, float_format='%.2f')